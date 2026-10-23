# BAAJA: Who pays for the grid?

A buildless HTML dashboard and one-page brief for the transmission AND-pricing provision in section 2107(a) of the September 2026 BAAJA discussion draft.

**[Open dashboard](https://dashboardamerican.github.io/baaja-and-pricing/)** · **[One-page PDF](baaja-one-pager.pdf)**

Exactly three sliders: annual DC growth **after 2030**, attributable incremental network capital per MW, and the assumed NITS-equivalent rate. The data-center load factor is fixed at **80%**. No installation, account, analytics, external script or API is required. Serve this folder or open `index.html` locally.

## Central case

All 30-year figures are **constant 2026 dollars**, undiscounted, over **2027-2056**. Charges begin in 2030. The results are conditional planning scenarios, not forecasts or official bill scores.

| Measure | 30-year central result |
| --- | ---: |
| A: Additional AND payments versus higher-of | **$62.7bn** |
| B: AND payments above incremental transmission cost | **$125.1bn** |
| BBB transmission ITC, repeated-program illustration | **$31.7bn** |

**A is part of B. Never add them.** Existing ordinary transmission payments already contribute toward inherited grid costs. A isolates the additional money caused by AND pricing; B is the entire contribution above incremental transmission cost. Neither measure is a federal receipt. ITC budget cost is not an estimate of equivalent customer-bill savings.

## Assumptions

| Item | Central assumption |
| --- | --- |
| Near-term DC facility demand | 300 TWh in 2026 to 600 TWh in 2030, geometric interpolation |
| DC growth slider | 2.0% annually after 2030; gives 1,004 TWh in 2056 |
| Capital slider | $0.65m/MW attributable incremental transmission network investment |
| NITS slider | $95.1/kW-year = $95,100/MW-year, constant real |
| DC load factor | 80% |
| Effective chargeable share of new DC load | 75%, unchanged with sliders |
| Incumbent billing-demand proxy | 829 GW, held flat; derived from 2025 utility planning peaks |
| First charge year | 2030; new 2027-2029 entrants are charged prospectively from 2030 |
| Capital recovery | 40 years, 5% real financing, 1.5% annual O&M: annual factor 7.3278% |
| Existing AND pricing | Zero; no overlap haircut |
| Horizon | 2027-2056; no post-horizon terminal value |

The growth slider changes only 2031 onward, preserving the evidence-anchored near-term expansion. The 2056 path is a scenario, not a published forecast. Capital excludes unrelated work and requires project-specific attribution; dedicated facilities, contributions and credits must be reconciled in real tariff comparisons. The model holds construction and demand fixed between pricing cases. It does not estimate demand response, relocation, generation or distribution costs, discretionary retail surcharges, or departures from the grid. Summing regional higher-of calculations can give less relief than applying higher-of once to a homogeneous national pool.

## A national rate proxy, with PUDL reviewed

We did **not** identify an observed, tariff-billing-demand-weighted national NITS average. NITS is not a uniform nationwide tariff. The default is explicitly a **national transmission cost-to-peak proxy**:

1. EIA AEO2026 Table 54, cells C81 and C136: 4,069.278 TWh of 2025 sales × 1.8850884 cents/kWh = **$76.709bn** of modeled transmission-service expenditure.
2. Divide by **829 GW**, the national 2025 summer planning-peak total from Grid Strategies' original FERC Form 714 aggregation, p.33.
3. Apply EIA's implied 2026/2025 price deflator **1.02753958** (D140/D136): **$95,080.87/MW-year** in 2026 dollars. Slider rounds to **$95,100**.

This uses national expenditure and peak totals, rather than an unweighted mean of selected tariff rates. Planning peaks differ from 1CP/12CP billing determinants; national geographic scopes differ slightly. Future DC location weights are unknown. The 829 GW pool is the same planning denominator, not a measured incumbent tariff-billing pool. A useful rate sensitivity is $60-$150/kW-year.

**PUDL review:** local release v2026.10.0, relevant data year 2025. We reviewed FERC Form 1 Schedules 204, 219, 300, 320, 326 and 336, detailed income/rate-base tables, EIA-861 revenue and peak records, and FERC-714 metadata. PUDL contains assets, annual functional depreciation, operating costs and some transmission revenues. It lacks an assembled national transmission tariff revenue requirement matched to billing demand. Schedule 326 demand is purchased-power-contract demand. EIA-861 utility peak sums overlap; transmission revenue excludes much bundled-retail recovery. Transmission expenses include purchased transmission and cannot be added to owners' revenue. Book additions cannot identify data-center-attributable capital per MW. [Full queries/results](data/pudl-review.json), [national rate arithmetic](data/national-rate.json).

## Credited annual ledger

Let `B0` be inherited revenue requirement, `I` annual incremental cost, and `s` new covered load's share of total billing demand:

```text
ordinary tariff payment = s * (B0 + I)
higher-of baseline       = max(ordinary tariff payment, I)
credited AND payment     = s * B0 + I
A: additional receipts  = AND - higher-of = min(s * B0, (1 - s) * I)
B: above incremental CoS= AND - I = s * B0
other-customer relief   = A
```

Direct incremental receipts are removed from the shared revenue requirement before calculating embedded charges. Both cases collect exactly `B0 + I`. New eligible MW is growth beyond the 2026 DC baseline, divided by 8,760 hours and 80% load factor, multiplied by 75% coverage. Each year's payments count only inside the horizon. At the central cost, A is relatively insensitive to NITS because incremental capital cost is the smaller obligation. B rises with the NITS assumption.

## Honest 30-year ITC comparison

JCT's **official historical** estimate is **$11.279bn nominal over FY2022-2031** for the transmission ITC in the House-passed Build Back Better Act. The $3.024bn direct-pay outlay component is already included.

For a common 30-year illustration, use the actual annual JCT budget amounts, positive federal-cost convention:

```text
FY:          2022 2023 2024 2025  2026  2027  2028  2029  2030  2031
$bn nominal: 0    0    0    .788  1.213 1.213 1.213 2.001 2.426 2.425
```

Normalize each amount to 2026 dollars using the **assumed common 2.5% inflation convention**, `cost[y]/1.025**(y-2026)`. The real ten-year total is $10.558bn. Repeat that real ten-year profile three times across 2027-2056: **$31.674bn**. This is our own **repeated-program illustration**. It is not an official 30-year JCT score, a forecast of the 2026 ITC proposal, a permanent-program score, or 30-year benefits from one ten-year credit. Resetting the historical ramp each decade is an illustrative scaling convention. No additional assumption about transmission investment growth is embedded in this comparison.

The reference AND additional payment is about **2.0×** this ITC illustration: comparable as tens of billions of dollars, with different payers and fiscal treatment. This is a magnitude comparison, not a budget offset or welfare comparison.

## Reproduce and verify

```bash
node checks.cjs
python3 analysis/build_data.py
python3 analysis/build_brief.py  # requires reportlab
python3 -m http.server 8767
```

`model.js` runs the dashboard. `analysis/reference.py` is an independently written Python reference. `checks.cjs` compares both languages against independent annual golden cases, checks budget conservation, zero-cost/zero-rate boundaries, rate-cap behavior, A/B distinction and ITC arithmetic. The PDF draws its numbers from `data/central-case.json`. The dashboard's annual CSV export reflects the current sliders. No build step is needed for GitHub Pages; publish `main` / root.

## Sources

- [BAAJA September 2026 draft, section 2107(a), pp.229-230](https://www.energy.senate.gov/wp-content/uploads/2026/09/Bipartisan-American-Affordability-and-Jobs-Act.pdf#page=229).
- [JCT JCX-46-21, Nov.19,2021, p.2](https://www.govinfo.gov/content/pkg/GOVPUB-Y4_T19_4-PURL-gpo172711/pdf/GOVPUB-Y4_T19_4-PURL-gpo172711.pdf#page=2).
- [EIA AEO2026 Table54](https://www.eia.gov/outlooks/aeo/supplement/excel/suptab_54.xlsx); [Electricity Market Module methodology, printed pp.160-163](https://www.eia.gov/outlooks/aeo/nems/documentation/electricity/pdf/EMM_AEO2025.pdf).
- [Grid Strategies, Nov.2025 original FERC714 aggregation, p.33](https://gridstrategiesllc.com/wp-content/uploads/Grid-Strategies-National-Load-Growth-Report-2025.pdf#page=33).
- [EPRI 2026 demand scenarios](https://powering-intelligence.epri.com/executive-summary.html); [LBNL 2025 Update, published2026](https://escholarship.org/content/qt33m6w3x0/qt33m6w3x0.pdf).
- [AEP Piketon planned transmission](https://www.aep.com/news/stories/view/10823/); [Wisconsin PSC Ozaukee application](https://psc.wi.gov/Pages/CommissionActions/CasePages/OzaukeeDIP.aspx).
- [PUDL FERC1 documentation](https://docs.catalyst.coop/pudl/en/latest/data_sources/ferc1.html); [PUDL data](https://data.catalyst.coop/search).

As of October23,2026. Source-year estimates and scenarios retain their stated limitations.
