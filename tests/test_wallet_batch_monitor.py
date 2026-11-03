"""Offline M01 adversarial tests: no Solana network, wallet, signing or swap calls."""
import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from solana_meme_os.wallet_batch_monitor import analyze

UTC = timezone.utc
BASE = datetime(2026, 10, 31, 0, 0, tzinfo=UTC)
MINT = 'M' * 44
QUOTE = 'So11111111111111111111111111111111111111112'
ROOT = Path(__file__).resolve().parents[1]


def addr(ch):
    return ch * 44


def iso(dt):
    return dt.isoformat().replace('+00:00', 'Z')


def fixture():
    return {
        'schema_version': 'm01.v1', 'mode': 'fixture', 'chain': 'sol',
        'mint': MINT, 'quote_mint': QUOTE, 'quote_decimals': 9,
        'source': {'tool': 'offline_unit_test', 'ref': 'fixture://m01-test'},
        'coverage': {'start': iso(BASE), 'end': iso(BASE + timedelta(minutes=30)),
                     'complete': True, 'gaps': []},
        'as_of': iso(BASE + timedelta(minutes=35)), 'events': []
    }


def event(i, minute, owner='A', kind='BUY', amount=1_000_000_000, token='Z', status='SUCCESS', available_minute=None):
    return {
        'event_id': f'fixture-signature-{i}:0', 'signature': f'fixture-signature-{i}',
        'slot': 1000 + i, 'event_time': iso(BASE + timedelta(minutes=minute)),
        'available_at': iso(BASE + timedelta(minutes=available_minute if available_minute is not None else minute)),
        'source_ref': f'fixture://m01/{i}', 'wallet_owner': addr(owner),
        'token_account': addr(token), 'kind': kind, 'tx_status': status,
        'quote_amount_raw': amount if kind in ('BUY', 'SELL') else 0,
        **({'quote_mint': QUOTE} if kind in ('BUY', 'SELL') else {}),
    }


class M01Tests(unittest.TestCase):
    def test_window_counts_enters_retains_returns_and_quote_divergence(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A', amount=5_000_000_000), event(2, 0, 'B', token='Y', amount=5_000_000_000),
                          event(3, 1, 'B', token='Y', amount=1_000_000_000), event(4, 1, 'C', token='X', amount=1_000_000_000),
                          event(5, 2, 'A', amount=1_000_000_000)]
        result = analyze(data)
        w = result['timeframes']['1m']['windows']
        self.assertEqual([(w[i]['active_wallet_count'], w[i]['first_observed_count'], w[i]['returning_count']) for i in range(3)],
                         [(2, 2, 0), (2, 1, 0), (1, 0, 1)])
        self.assertEqual(result['timeframes']['1m']['comparisons'][0]['retained_count'], 1)
        self.assertEqual(result['timeframes']['1m']['comparisons'][0]['entered_count'], 1)
        self.assertEqual(w[0]['buy_quote_raw'], 10_000_000_000)
        self.assertEqual(w[1]['buy_quote_raw'], 2_000_000_000)

    def test_volume_divergence_when_buyers_increase(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A', amount=10_000_000_000),
                          event(2, 1, 'A', amount=1_000_000_000),
                          event(3, 1, 'B', token='Y', amount=1_000_000_000)]
        candidate = analyze(data)['timeframes']['1m']['candidates'][0]
        self.assertIn('BUYERS_UP_QUOTE_VOLUME_DOWN', candidate['types'])
        self.assertEqual(len(candidate['source_refs']), 3)
        self.assertEqual(candidate['after']['buy_quote_raw'], 2_000_000_000)

    def test_same_count_all_members_replaced(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A'), event(2, 0, 'B', token='Y'),
                          event(3, 1, 'C', token='X'), event(4, 1, 'D', token='W')]
        c = analyze(data)['timeframes']['1m']['candidates'][0]
        self.assertIn('SAME_COUNT_FULL_MEMBER_REPLACEMENT', c['types'])
        self.assertEqual(c['comparison']['jaccard'], 0.0)

    def test_distinct_token_accounts_same_owner_and_repeat_transactions(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A', token='Z'), event(2, 0, 'A', token='Y')]
        data['events'].append(copy.deepcopy(data['events'][0]))
        result = analyze(data)
        self.assertEqual(result['ignored_duplicate_events'], 1)
        self.assertEqual(result['timeframes']['1m']['windows'][0]['active_wallet_count'], 1)
        self.assertEqual(result['timeframes']['1m']['windows'][0]['buy_quote_raw'], 2_000_000_000)

    def test_token_owner_conflict_fails_closed(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A'), event(2, 1, 'B')]
        with self.assertRaisesRegex(ValueError, 'owner conflict'):
            analyze(data)

    def test_failed_transactions_excluded_and_successful_transfer_not_swap(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A', status='FAILED'),
                          event(2, 0, 'B', kind='TRANSFER', token='Y')]
        w = analyze(data)['timeframes']['1m']['windows'][0]
        self.assertEqual(w['active_wallet_count'], 1)
        self.assertEqual(w['buy_quote_raw'], 0)
        self.assertEqual(w['failed_event_count'], 1)

    def test_gap_prevents_false_stop_and_comparison(self):
        data = fixture()
        data['coverage']['gaps'] = [{'start': iso(BASE + timedelta(minutes=1)), 'end': iso(BASE + timedelta(minutes=2))}]
        data['events'] = [event(1, 0, 'A'), event(2, 2, 'B', token='Y')]
        r = analyze(data)['timeframes']['1m']
        self.assertEqual(r['windows'][1]['data_status'], 'INCOMPLETE')
        self.assertIsNone(r['windows'][1]['active_wallet_count'])
        self.assertFalse(any(c['current_start'] in (iso(BASE + timedelta(minutes=1)), iso(BASE + timedelta(minutes=2))) for c in r['comparisons']))
        self.assertFalse(any(c['window_start'] in (iso(BASE + timedelta(minutes=1)), iso(BASE + timedelta(minutes=2))) for c in r['candidates']))
        self.assertEqual(analyze(data)['timeframes']['5m']['windows'][0]['data_status'], 'INCOMPLETE')

    def test_unresolved_or_late_event_marks_window_incomplete(self):
        for e in (event(1, 0, 'A', status='UNRESOLVED'), event(2, 0, 'A', available_minute=36)):
            data = fixture()
            data['events'] = [e]
            w = analyze(data)['timeframes']['1m']['windows'][0]
            self.assertEqual(w['data_status'], 'INCOMPLETE')
            self.assertIsNone(w['buy_quote_raw'])

    def test_complete_empty_window_is_real_zero_and_may_stop(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A'), event(2, 0, 'B', token='Y'), event(3, 0, 'C', token='X'),
                          event(4, 1, 'A'), event(5, 1, 'B', token='Y'), event(6, 1, 'C', token='X')]
        r = analyze(data)['timeframes']['1m']
        self.assertEqual(r['windows'][2]['active_wallet_count'], 0)
        self.assertIn('SUSTAINED_ACTIVITY_THEN_STOPPED', r['candidates'][0]['types'])

    def test_multiple_timeframes_and_end_boundary(self):
        data = fixture()
        data['events'] = [event(1, 0, 'A'), event(2, 5, 'B', token='Y'), event(3, 15, 'C', token='X')]
        r = analyze(data)
        self.assertEqual([len(r['timeframes'][k]['windows']) for k in ('1m', '5m', '15m')], [30, 6, 2])
        self.assertEqual(r['timeframes']['15m']['windows'][0]['active_wallet_count'], 2)
        self.assertEqual(r['timeframes']['15m']['windows'][1]['active_wallet_count'], 1)

    def test_reject_bad_quote_and_unresolved_owner(self):
        data = fixture()
        bad = event(1, 0, 'A')
        bad['quote_mint'] = addr('Q')
        data['events'] = [bad]
        with self.assertRaisesRegex(ValueError, 'quote mint'):
            analyze(data)
        data['events'][0] = event(2, 0, 'A')
        del data['events'][0]['wallet_owner']
        with self.assertRaisesRegex(ValueError, 'wallet_owner'):
            analyze(data)

    def test_duplicate_conflict_rejected(self):
        data = fixture()
        e = event(1, 0, 'A')
        other = copy.deepcopy(e)
        other['quote_amount_raw'] = 12
        data['events'] = [e, other]
        with self.assertRaisesRegex(ValueError, 'conflicting evidence'):
            analyze(data)

    def test_fixture_only_and_truthful_time_cutoff(self):
        data = fixture()
        data['mode'] = 'live'
        with self.assertRaisesRegex(ValueError, 'fixture'):
            analyze(data)
        data = fixture()
        data['as_of'] = iso(BASE + timedelta(minutes=10))
        with self.assertRaisesRegex(ValueError, 'as_of'):
            analyze(data)

    def test_cli_fixture_output(self):
        with TemporaryDirectory() as d:
            report = Path(d) / 'report.json'
            p = subprocess.run([sys.executable, '-m', 'solana_meme_os.wallet_batch_monitor',
                                '--input', str(ROOT / 'fixtures/wallet-batches-demo.json'),
                                '--output', str(report)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            obj = json.loads(report.read_text(encoding='utf-8'))
            self.assertEqual(obj['status'], 'FIXTURE_RESEARCH_ONLY')
            self.assertTrue(obj['no_trading'])
            self.assertEqual(obj['timeframes']['1m']['windows'][0]['buy_wallet_count'], 2)


if __name__ == '__main__':
    unittest.main()