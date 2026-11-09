# Financing one million public housing units in Spain

**A reproducible financial modelling exercise for a proposed programme of one million housing units in Spain.**

This repository implements a linear-programming model of construction, unit sales, public rental receipts, sovereign-bond issuance, refinancing and contributions from the Spanish State Budget (*Presupuestos Generales del Estado*, PGE). It compares **33 debt-repayment deadlines (years 30–62)** and analyses the trade-off between the peak annual PGE transfer and nominal coupon interest. The **50-year debt-repayment deadline is a reporting reference, not a demonstrated optimum**.

> **Scope:** This is a scenario-based financial simulation, not an official government programme, a forecast, a fiscal affordability assessment, or a comprehensive social cost–benefit analysis. Its results depend on explicit modelling assumptions.

## Programme assumptions

| Input | Baseline |
| --- | ---: |
| Homes | 1,000,000 |
| Construction starts | 100,000 per year in years 1–10 |
| Deliveries | 100,000 per year in years 3–12 |
| Unit construction **and land** cost | €180,000 |
| Total construction and land investment | €180 billion |
| Units sold / retained for public rental | 60% / 40% |
| Sale price per unit | €200,000 |
| Monthly rent / rent collection | €600 / 95% |
| Management / maintenance provision | 15% / 5% of rent collected |
| Rental modelling period | 50 full years per delivered cohort |
| Illustrative unrestricted liquidity buffer | €3 billion, years 1–11 |
| Bond tenors | 3, 5, 10, 15, 20, 30 years |
| Repayment deadlines compared | 30–62 years |

The programme retains 400,000 units for rental under the model's ownership assumptions, while 600,000 units are sold; the phrase *one million public housing units* describes the modelled programme, **not one million permanently publicly owned rental homes**. A reference dwelling of 75 m² usable area (approximately 100 m² built area) was specified in the project design, but the financial optimiser uses a unit-cost input rather than deriving costs from floor area.

Rental cash in the delivery year is calculated as a full year's rent, which is favourable to the programme. The management and maintenance shares are **restricted provisions**, not observed spending; actual withdrawals, major rehabilitation and replacement costs are not simulated. Rental income stops after 50 modelled years per delivered cohort. Cash and housing flows are reported through project year 62.

## Interest rates and debt safeguards

The model uses the Banco de España yield-curve reference dated **28 October 2026**, with the 20-year yield linearly interpolated:

| Original tenor | Reference yield |
| --- | ---: |
| 3 years | 3.37% |
| 5 years | 3.53% |
| 10 years | 4.03% |
| 15 years | 4.31% |
| 20 years | 4.3633% (interpolated) |
| 30 years | 4.47% |

Fixed-by-tenor rates are used as **par-coupon proxies** throughout each simulation; these are neither guaranteed future borrowing rates nor dynamic yield forecasts.

The Treasury benchmark comprises **66 outstanding Treasury bond/obligation references on 31 October 2026**, excluding Treasury bills. Its observed share of debt maturing within three years (approximately **28.10%**) informs a model-imposed concentration limit during the stable phase. A separate **8-year minimum weighted-average remaining maturity (WAM)** is a modelling choice. Both rules relax appropriately near the final repayment deadline; they are **not statutory issuance restrictions**.

## Optimisation

For each deadline the model uses **lexicographic linear programming**:

1. Minimise the **maximum annual PGE contribution**.
2. Holding that optimum within numerical tolerance, minimise **total PGE transfers**.
3. Holding both previous priorities within tolerance, minimise **nominal bond coupon interest**.

There is **no exogenous PGE ceiling in the baseline**. A separate interest-first sensitivity compares illustrative annual PGE ceilings at the 50-year deadline. Primary issuance, refinancing, annual cash balances, maturity concentration and debt cancellation are jointly constrained. Refinancing issuance cannot exceed principal due during the same year.

## Selected reference results: debt paid by year 50

| Indicator | Approximate value |
| --- | ---: |
| Maximum annual PGE transfer | **€954 million** |
| Cumulative PGE transfers | **€47.699 billion** |
| Nominal coupon interest | **€82.912 billion** |
| Peak outstanding debt | **€76.397 billion** |

These are **not annual flat payments**, fiscal spending capacity estimates or discounted present values. All figures are nominal and undiscounted. Alternative deadlines generate different combinations of annual budget pressure and debt-servicing costs.

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── notebooks/
│   ├── Spain_Public_Housing_Financing_Model_v27.ipynb
│   └── 01_Official_Data_BdE_Treasury_v4.ipynb
├── data/
│   ├── spanish_yield_curve_2026_10_28.csv
│   └── tesoro_outstanding_bonds_2026_10_31_by_reference.csv
└── results/
    └── 11 reported output CSVs from v27
```

## Reproduce the analysis

Requires **Python 3.10+**. From a terminal:

```bash
git clone https://github.com/jaimeeroodrigueez/Spain-Public-Housing-Financing.git
cd Spain-Public-Housing-Financing
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab notebooks/Spain_Public_Housing_Financing_Model_v27.ipynb
```

**Important:** Launch Jupyter **from the repository root**, so that the model reads `data/` and writes `results/`. Running it from `notebooks/` also works because it searches the parent `data/` folder. In Colab, clone the repository and use `%cd /content/Spain-Public-Housing-Financing` before running the notebook. Opening the notebook directly from GitHub in Colab without cloning its data files will not suffice.

The GitHub notebook retains the model's calculations while using repository-relative paths for input and output files. Its saved visual outputs are provided for inspection; temporary Colab execution metadata has been removed. It does not change the programme inputs, optimisation objective, constraints or financial results.

The **official-data preparation notebook** documents the extraction of the historical yield curve and Treasury portfolio. Since the original official websites may change, reproducing extraction for the historical snapshot may require archived official source pages; the fixed input CSVs needed for the financing model are included under `data/`.

## Main outputs

`results/` contains 11 CSVs, including the full horizon comparison, the interest–budget frontier, the bond-issuance portfolio, annual financial ledger, refinancing risk, residual maturity comparisons, rental provisions and post-repayment cash. Their precise filenames are generated and documented by the last code cell of the model notebook.

## Limitations

The exercise does not establish whether the Spanish budget has room to fund these transfers. It does not model inflation, yield changes over time, endogenous costs or rents, construction-sector and land capacity, demand for new bonds, uncertainty distributions, discounting, opportunity costs, major rehabilitation withdrawals or broader macroeconomic/social effects. No claim of fiscal affordability follows solely from the optimisation's mathematical feasibility.

## Source data and provenance

- Banco de España, sovereign yield series dated 28 October 2026 (series IDs and interpolation recorded in `data/spanish_yield_curve_2026_10_28.csv`).
- Tesoro Público, 66 bond and obligation references outstanding on 31 October 2026 (see `data/tesoro_outstanding_bonds_2026_10_31_by_reference.csv`).
- The methodology for preparing each input is included in the official-data notebook.

## License

The project's original software code and accompanying software documentation are available under the [MIT License](LICENSE) (copyright © 2026 Jaime Rodríguez Almendros). Third-party data and source material, including Banco de España and Tesoro Público datasets, remain subject to their respective terms and are not relicensed by this notice.
