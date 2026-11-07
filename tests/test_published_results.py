"""Lightweight consistency checks for the published v27 CSV snapshot."""
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

class PublishedResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.horizons = pd.read_csv(ROOT / 'results/housing_repayment_horizons_v27.csv')
        cls.curve = pd.read_csv(ROOT / 'data/spanish_yield_curve_2026_10_28.csv')
        cls.treasury = pd.read_csv(ROOT / 'data/tesoro_outstanding_bonds_2026_10_31_by_reference.csv')

    def test_horizons(self):
        self.assertEqual(sorted(self.horizons['Deadline'].astype(int)), list(range(30, 63)))

    def test_reference_50(self):
        row = self.horizons.loc[self.horizons['Deadline'].eq(50)].iloc[0]
        self.assertAlmostEqual(row['PGE annual']/1e6, 953.986, delta=0.1)
        self.assertAlmostEqual(row['PGE total']/1e9, 47.699, delta=0.002)
        self.assertAlmostEqual(row['Interest total']/1e9, 82.912, delta=0.002)
        self.assertAlmostEqual(row['Peak debt']/1e9, 76.397, delta=0.002)

    def test_curve_and_benchmark(self):
        self.assertEqual(set(self.curve['Years'].astype(int)), {3,5,10,15,20,30})
        self.assertTrue(self.curve['Date'].eq('2026-10-28').all())
        self.assertEqual(len(self.treasury), 66)
        nominal = self.treasury['nominal_outstanding_million_eur']
        share = nominal[self.treasury['years_remaining']<=3].sum()/nominal.sum()
        self.assertAlmostEqual(share, .28096146, delta=.0001)

    def test_ledger(self):
        ledger = pd.read_csv(ROOT / 'results/housing_annual_ledger_62_years_v27.csv')
        self.assertEqual(len(ledger), 62)
        self.assertEqual(list(ledger['Year'].astype(int)), list(range(1,63)))
        self.assertEqual(set(ledger['Year'].astype(int)), set(range(1,63)))

if __name__=='__main__':
    unittest.main()
