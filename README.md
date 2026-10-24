# BAAJA: Who pays for the grid?

A buildless HTML dashboard and one-page brief for the transmission AND-pricing provision in section 2107(a) of the September 2026 BAAJA discussion draft.

**[Open dashboard](https://dashboardamerican.github.io/baaja-and-pricing/)** · **[One-page PDF](baaja-one-pager.pdf)**

Choose **Low, Medium, or High** data-center growth through 2056. EPRI supplies the U.S. 2030 endpoints; later years use an explicit, tapered extrapolation. Medium is the default. Two sliders control attributable incremental network capital per MW and the assumed NITS-equivalent rate. The data-center load factor is fixed at **80%**. No installation, account, analytics, external script or API is required. Serve this folder or open `index.html` locally.

## Central case

All 30-year figures are **constant 2026 dollars**, undiscounted, over **2027-2056**. Charges begin in 2030. The results are conditional planning scenarios, not forecasts or official bill scores.

| Measure | 30-year central result |
| --- | ---: |
| A: Additional AND payments versus embedded | **$74.6bn** |
| B: AND payments above incremental transmission cost | **$148.9bn** |
| BBB transmission ITC, repeated-program illustration | **$31.7bn** |

**A and B overlap; never add them. In the central case A is part of B. With embedded pricing, A can exceed B when the baseline shifts incremental costs to other customers.** Existing ordinary transmission payments already contribute toward inherited grid costs. A isolates additional money versus the selected baseline; B is the entire contribution above incremental transmission cost. Neither measure is a federal receipt. ITC budget cost is not an estimate of equivalent customer-bill savings.

## Assumptions

| Item | Central assumption |
| --- | --- |
| Near-term DC facility demand | Selected 300 TWh baseline in 2026 to EPRI Medium 596 TWh in 2030, geometric interpolation |
| DC growth presets | EPRI U.S. 2030 Low / Medium / High; IEA global multipliers through 2035; selected taper thereafter. Medium reaches 1,096 TWh in 2056 |
| Capital slider | $0.65m/MW attributable incremental transmission network investment |
| NITS slider | $95.1/kW-year = $95,100/MW-year, constant real |
| DC load factor | 80% |
| Effective modeled-grid share of new DC load | 75%, unchanged with sliders; other demand excluded from costs and billing pool |
| Incumbent billing-demand proxy | 829 GW, held flat; derived from 2025 utility planning peaks |
| First charge year | 2030; new 2027-2029 entrants are charged prospectively from 2030 |
| Capital recovery | 40 years, 5% real financing, 1.5% annual O&M: annual factor 7.3278% |
| Prior cost-recovery obligations | No offset in the illustrative central case; actual direct funding and special-contract payments must be reconciled |
| Horizon | 2027-2056; no post-horizon terminal value |

Low, Medium and High are illustrative scenarios, not forecast confidence bounds. All post-2030 U.S. paths are analyst extrapolations. Capital excludes unrelated work and requires project-specific attribution; dedicated facilities, contributions and credits must be reconciled in real tariff comparisons. The model holds construction and demand fixed between pricing cases. It does not estimate demand response, relocation, generation or distribution costs, discretionary retail surcharges, or departures from the grid. Summing regional higher-of calculations can give less relief than applying higher-of once to a homogeneous national pool.

## Demand basis and extrapolation

[EPRI, Powering Intelligence 2026, Figure 5](https://powering-intelligence.epri.com/annual-peak-use.html) provides U.S. 2030 facility demand of **383 / 596 / 793 TWh**. It includes cryptocurrency and small and large data centers. The selected common 2026 baseline is **300 TWh**, not an observed annual total; new covered demand is measured above it. We interpolate geometrically to each EPRI endpoint.

For 2031-2035, we transfer the growth multipliers from the **global** Headwinds / Base / Lift-Off scenarios in [IEA, Key Questions on Energy and AI, Table A.1, p.108](https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf#page=108). Global 2030/2035 TWh are **833/942, 945/1,193, 1,008/1,637**, implying about **2.5% / 4.8% / 10.2% annual growth**. This is an explicit geographic and scope transfer assumption, not an IEA U.S. forecast. IEA itself calls its 2035 figures exploratory. EPRI and IEA absolute levels are not averaged.

During 2036-2040, the annual rates fall in five equal steps to selected mature growth rates of **0.5% / 1.5% / 2.5%**. Those rates hold through 2056. This allows a strong initial buildout to slow as the sector matures and efficiency improves, while preserving a broad high-growth case. The taper date and mature rates are judgment calls, not published EPRI or IEA projections. The long-run results are conditional on these choices.

| Annual U.S. facility demand, TWh | Low | Medium | High |
| --- | ---: | ---: | ---: |
| 2030: EPRI | 383 | 596 | 793 |
| 2035: extrapolated | 433 | 752 | 1,288 |
| 2040: extrapolated | 462 | 864 | 1,687 |
| 2050: extrapolated | 486 | 1,003 | 2,160 |
| 2056: extrapolated | 500 | 1,096 | 2,505 |

[Machine-readable annual paths and source notes](data/growth-scenarios.json) include every year and all scenario parameters. Holding the cost and rate sliders at their defaults, the three paths give approximately **$22bn / $75bn / $166bn** additional payments. This is a scenario range, not a statistical confidence interval.

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
embedded baseline       = ordinary tariff payment
higher-of alternative   = max(ordinary tariff payment, I)
credited AND payment     = s * B0 + I
A versus embedded      = AND - ordinary = (1 - s) * I
A versus higher-of     = min(s * B0, (1 - s) * I)
B: above incremental CoS= AND - I = s * B0
other-customer relief   = A
```

Direct incremental receipts are removed from the shared revenue requirement before calculating embedded charges. Both cases collect exactly `B0 + I`. New eligible MW is growth beyond the 2026 DC baseline, divided by 8,760 hours and 80% load factor, multiplied by 75% coverage. The remaining 25% is outside this modeled grid, not an exemption for connected customers: an exemption would require modeling its ordinary payments, investment and billing share separately. Each year's payments count only inside the horizon. With an embedded baseline and fixed physical investment/billing shares, A is independent of the inherited NITS rate: it is the incremental cost no longer shared with incumbent customers. B rises with NITS. Under higher-of, A is capped by the inherited-grid contribution. The baseline selector is under Details; embedded is the default.

## Honest 30-year ITC comparison

JCT's **official historical** estimate is **$11.279bn nominal over FY2022-2031** for the transmission ITC in the House-passed Build Back Better Act. The $3.024bn direct-pay outlay component is already included.

For a common 30-year illustration, use the actual annual JCT budget amounts, positive federal-cost convention:

```text
FY:          2022 2023 2024 2025  2026  2027  2028  2029  2030  2031
$bn nominal: 0    0    0    .788  1.213 1.213 1.213 2.001 2.426 2.425
```

Normalize each amount to 2026 dollars using the **assumed common 2.5% inflation convention**, `cost[y]/1.025**(y-2026)`. The real ten-year total is $10.558bn. Repeat that real ten-year profile three times across 2027-2056: **$31.674bn**. This is our own **repeated-program illustration**. It is not an official 30-year JCT score, a forecast of the 2026 ITC proposal, a permanent-program score, or 30-year benefits from one ten-year credit. Resetting the historical ramp each decade is an illustrative scaling convention. No additional assumption about transmission investment growth is embedded in this comparison.

The reference AND additional payment is about **2.4×** this ITC illustration: comparable as tens of billions of dollars, with different payers and fiscal treatment. This is a magnitude comparison, not a budget offset or welfare comparison.

## Empirical review and regional model (October 23, 2026)

[Read the evidence report](evidence.html). The review screened all **15,838 PJM export records**, the **432-project MTEP25 Appendix A workbook**, and **27 MTEP26 expedited-review PDFs**, extracting **90 unique project cost cards**. A reviewed, nonrandom sample matches **11 packages / 5,011 MW**, including their identified CAP upgrades. Its cost intensity is a description of disclosed packages, not a national mean or a net newly-assignable capital estimate. Four packages have computational-load identification; seven remain generic large-load benchmarks.

Measured PJM rates weighted by published 2026 NSPL average **$82.8/kW-year**. Weighting by positive net new large-load forecast demand through 2030 gives **$94.7/kW-year**. This supports the order of magnitude of the dashboard proxy in PJM; it does not validate a national tariff average.

The conditional PJM zonal model produces **$44.2bn** above embedded pricing versus **$50.3bn** if the same inputs are pooled nationally within PJM. This approximately **14% pooling overstatement** is an illustration using fixed real rates, $0.65m/MW, 75% coverage, published load through 2046 and a selected 1.5% tail to 2056. It is not a PJM forecast of BAAJA receipts.

Newly identified existing funding and contractual obligations mean that zero use of an AND tariff does not imply zero prior incremental-cost recovery. [Existing-obligation evidence](data/evidence/existing-obligations.json). The national central benchmark remains $74.6bn at selected inputs; assuming 25% or 50% of that uplift is already collected beyond embedded charges leaves $55.9bn or $37.3bn of policy-additional receipts. Those percentages are sensitivities, not measured national shares.

[Inventory audit](data/evidence/inventory-audit.json) · [Matched MISO packages](data/evidence/miso26-matched-packages.csv) · [PJM rates and load](data/evidence/pjm-zonal-rates-and-load.csv) · [Regional and national results](data/evidence/regional-model-results.json) · [Source hashes](data/evidence/source-manifest.json).

To reproduce the evidence extraction, with openpyxl and pypdf installed:

```bash
python3 analysis/fetch_empirical_sources.py  # ~220 MB; verifies source SHA-256
python3 analysis/build_empirical_evidence.py
python3 analysis/extract_miso_epr.py
python3 analysis/build_matched_cases.py
python3 analysis/regional_model.py
python3 analysis/build_evidence_report.py
```

The raw archives are retained locally under `research/` and excluded from Git. If a mutable public file changes, the fetcher rejects it rather than silently treating a new vintage as the audited snapshot. The JSON/CSV extracts and source locators remain available without those downloads.

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
- [EPRI 2026 U.S. demand scenarios](https://powering-intelligence.epri.com/annual-peak-use.html); [IEA 2026 global scenario multipliers, Table A.1](https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf#page=108).
- [AEP Piketon planned transmission](https://www.aep.com/news/stories/view/10823/); [Wisconsin PSC Ozaukee application](https://psc.wi.gov/Pages/CommissionActions/CasePages/OzaukeeDIP.aspx).
- [PUDL FERC1 documentation](https://docs.catalyst.coop/pudl/en/latest/data_sources/ferc1.html); [PUDL data](https://data.catalyst.coop/search).

As of October23,2026. Source-year estimates and scenarios retain their stated limitations.
