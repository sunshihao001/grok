#!/bin/sh
# Diagnostic original-Blix startup ONLY inside an air-gapped disposable Docker container.
# This is NOT a safe production startup method, market-feed test, or read-only certification.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SCRATCH=$(mktemp -d)
trap 'rm -rf "$SCRATCH"' EXIT
mkdir -p "$SCRATCH/data"

# Explicit isolation: no external network or Vault, no host credentials/home,
# original source mounted read-only, all writable database/state in throwaway /data.
docker run --rm --network none --read-only \
  --security-opt no-new-privileges --cap-drop ALL \
  --pids-limit 96 --memory 1g --cpus 1 \
  --tmpfs /tmp:rw,nosuid,nodev,size=32m,mode=1777 \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,source=$ROOT,target=/app,readonly" \
  --mount "type=bind,source=$SCRATCH/data,target=/data" \
  -e RADAR_DATA=/data -e HOME=/tmp -w /app \
  node:24-bookworm-slim sh -eu -c '
    # NEVER use the production startup-risk override in this script.
    # The legacy entry point is executed ONLY after Docker isolation is active.
    pid=""
    cleanup() {
      if [ -n "$pid" ]; then
        kill "$pid" 2>/dev/null || :
        wait "$pid" 2>/dev/null || :
      fi
    }
    trap cleanup EXIT INT TERM
    # A cold first boot followed by a restart using THE SAME disposable SQLite.
    # This exercises schema initialization and startup idempotence without a feed.
    for cycle in 1 2; do
      node --no-warnings server/server.js >/tmp/blix-server.log 2>&1 &
      pid=$!
      n=0
      healthy=0
      while [ "$n" -lt 25 ]; do
        if ! kill -0 "$pid" 2>/dev/null; then
          echo "BLIX_AIRGAP_BOOT_PROCESS_EXITED cycle=$cycle" >&2
          tail -n 50 /tmp/blix-server.log >&2 || :
          exit 1
        fi
        if node --input-type=module -e "
          const timeout = () => ({ signal: AbortSignal.timeout(1200) });
          const h = await fetch(\"http://127.0.0.1:4420/api/health\", timeout());
          if (!h.ok || typeof (await h.json()) !== \"object\") process.exit(2);
          const p = await fetch(\"http://127.0.0.1:4420/api/pulse\", timeout());
          if (!p.ok || typeof (await p.json()) !== \"object\") process.exit(3);
          const ui = await fetch(\"http://127.0.0.1:4421/\", timeout());
          if (!ui.ok || !(ui.headers.get(\"content-type\") || \"\").includes(\"text/html\")) process.exit(4);
          if (!/blix/i.test(await ui.text())) process.exit(5);
          console.log(\"BLIX_AIRGAP_BOOT_MARKET_API_AND_WEB_OK\");
        " >/tmp/blix-probe.log 2>&1; then
          cat /tmp/blix-probe.log
          healthy=1
          break
        fi
        n=$((n + 1))
        sleep 1
      done
      if [ "$healthy" -ne 1 ]; then
        echo "BLIX_AIRGAP_BOOT_TIMEOUT cycle=$cycle" >&2
        tail -n 50 /tmp/blix-server.log >&2 || :
        tail -n 20 /tmp/blix-probe.log >&2 || :
        exit 1
      fi
      test -f /data/radar.db || { echo "BLIX_AIRGAP_NO_DISPOSABLE_SQLITE" >&2; exit 1; }
      kill "$pid" 2>/dev/null || :
      wait "$pid" 2>/dev/null || :
      pid=""
      echo "BLIX_AIRGAP_BOOT_CYCLE_OK cycle=$cycle"
    done
    node --input-type=module -e "
      import { DatabaseSync } from \"node:sqlite\";
      const db = new DatabaseSync(\"/data/radar.db\", { readOnly: true });
      const result = db.prepare(\"PRAGMA integrity_check\").get();
      db.close();
      if (result?.integrity_check !== \"ok\") process.exit(2);
      console.log(\"BLIX_AIRGAP_RESTART_SQLITE_INTEGRITY_OK\");
    "
    echo "BLIX_AIRGAP_DB_CREATED_ONLY_IN_DISPOSABLE_CONTAINER_DATA"
  '
