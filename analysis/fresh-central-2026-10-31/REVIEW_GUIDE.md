# Reviewer guide: BAAJA transmission payment projection

This package supports independent review of the [one-page brief](ONE_PAGER.md). The result is a conditional policy scenario, not an empirically estimated national tariff forecast. A reviewer can reproduce the numbers and assess the evidence without access to the original chat, paid tools, or an AI service.

The [second-page methodology](METHODOLOGY_PAGE.md) prints all 15 source URLs and the core equations. The downloadable package includes the original one-page brief and the combined two-page PDF.

## Start here

Download [the review package](../../baaja-review-package.zip), unzip it, and run the following inside its folder with Python 3.9 or later. The check uses the Python standard library, requires no network, and does not alter the model or expected results.

```sh
python3 verify_review.py
```

Expected: PASS for file integrity, growth reconstruction, all 594 central region-year payment rows, all published sensitivity cases, the brief's additional scenarios, and the ITC calculation. A pass establishes reproducibility and arithmetic consistency, not legal applicability or empirical accuracy of selected assumptions. The checker reconstructs payments without importing or calling `calculate.py` or `brief_scenarios.py`.

To run the production model separately, preferably in a copy because it regenerates outputs:

```sh
python3 calculate.py
python3 brief_scenarios.py
```

[Claim register](review/claims.csv) maps each substantive one-pager claim to source IDs, model inputs, calculations, output fields and review questions. [Source register](review/sources.json) gives original URLs, exact pages/cells, archived-file hashes where available, and what each source does and does not establish. [Source values](review/source-values.csv) contains numeric transcriptions with original cell addresses. [Validation result](review/validation-result.json) records the checks actually completed.

To check original-file hashes and workbook cells as well, download the original files under the filenames in `review/sources.json`, then run `python3 verify_sources.py /path/to/original/files`. Missing originals or changed vintages are reported. PDFs and unarchived web sources still require manual review; exact locators are supplied. The downloadable package includes the numeric source extracts, not all original third-party documents.

## Bill text to model

The controlling version is **S.5653, introduced September 30, 2026**, not enacted law. Use [GovInfo's HTML](https://www.govinfo.gov/content/pkg/BILLS-119s5653is/xhtml/BILLS-119s5653is.html) or [official PDF](https://www.govinfo.gov/content/pkg/BILLS-119s5653is/pdf/BILLS-119s5653is.pdf). The package includes [the relevant statutory text](review/bill-section-2107.txt), with original physical page markers. The original PDF has matching printed and physical page numbers.

| Provision and original PDF location | Model treatment | What remains an interpretation or assumption |
| --- | --- | --- |
| 2107(a)(3)(A)(i), p.229 lines 19-25: embedded and incremental charges | AND payment `C + sK` | Defining which upgrades and shares are incremental; translating transmission-provider charges into DC payments |
| 2107(a)(3)(A)(ii), p.230 lines 1-6: incremental receipts credited to annual transmission revenue requirement | Remove recovered incremental costs before computing shared embedded charges | The algebra is an implementation of crediting, not an equation stated in the bill |
| 2107(a)(3)(B), p.230 lines 7-14: lower-cost non-firm service | No separate non-firm discount modeled | A 75% effective coverage assumption is not a measured substitute for a non-firm tariff model |
| 2107(a)(4), pp.230-231: rulemaking deadlines | Collections begin in 2030 | Actual enactment date, tariff implementation and treatment of 2027-2029 entrants are uncertain |
| 2107(a)(2)(E)-(G), pp.228-229: computational sites and utility definitions | Transmission-only scenario; 75% of new LBNL DC load | Jurisdiction, contracting, pass-through and eligibility require legal/tariff review. Crypto is excluded from the LBNL anchor although present in the bill |
| 2107(b), new FPA 228(a)-(c), pp.231-236 | Context for incremental-cost floor, prior contributions and optional additional retail collections | This retail provision is distinct from 2107(a)'s AND instruction. Do not combine the two to infer universal national AND coverage |
| New FPA 228(f), p.240 lines 1-8 | Timing sensitivity separately excludes pre-2030 entrants | The prospective language expressly refers to new section 228(b) and (c); it does not expressly fix the implementation date or grandfathering rule for 2107(a) |

The 20 MW threshold belongs to new FPA 228(a), not the definition in 2107(a). Neither the 75% national coverage share nor the 2027/2030 dates is prescribed by the bill. No legal opinion is claimed.

## Evidence versus judgment

The central demand anchors are LBNL's modeled historical 192 TWh in 2024 and projected 464 TWh in 2028 and 649 TWh in 2030, printed p.8 (physical PDF p.10). The 521-843 TWh uncertainty cases are on printed p.9 (physical p.11). These are facility-electricity estimates, not billing peaks. The 2026 baseline, later annual growth and 80% load factor are our transformations or assumptions.

The faster case uses EIA AEO2026 Table 5, sheet `cb2026.d021826b`, year headers row 10 and server-energy row 33. It applies server-use growth ratios to LBNL facility demand from 2030 and repeats the 2049-2050 rate through 2056. It is an analyst splice, not an EIA facility-energy forecast. The central forecast is never replaced by a simple average of heterogeneous forecasts.

PJM rates come from the archived **August 2026** workbook, with 2026 network-service peak loads and Table B9b large-load projections. The source-values file maps all 21 zones and all forecast years. PSEG's $183,352.99/MW-year is in `August 2026!E57`; it matches this source vintage. A different filing or month may show a different rate. This resolves the earlier review's suspicion of a January/August transcription error, not whether August is the best future rate assumption.

The $95,100 national rate is a rounded EIA modeled expenditure/planning-peak proxy. [Its derivation](review/national-rate-proxy.json) identifies exact EIA cells and the secondary source for the 829 GW planning peak. It is not an observed national billing-weighted NITS rate. The source's numerator and denominator have scope and timing differences. Setting half of covered DC growth in PJM is another judgment.

The package includes the [Dominion need-level records](review/explicit-dc-needs.csv), [linked project components](review/explicit-dc-project-components.csv), [MISO 2025 packages](review/miso25-matched-components.csv), and [MISO 2026 packages](review/miso26-matched-packages.csv), retaining their source-page references and missing-data qualifications. These document case checks; they do not derive a national mean.

The $0.65m/MW gross capital assumption and 35% prior capital funding are **not estimated national means**. [Capital evidence](capital-evidence.json) documents selected project packages and their limits. AEP's $4.2bn/10GW announcement supports $0.42m/MW for that announced package and a prospective funding commitment; it does not establish nationwide funding at 35%. Dominion and MISO packages are incomplete local/network examples. The Entergy testimony distinguishes permanent CIAC from service-agreement recovery during its term. Review the scope of the same assets and obligations before applying any funding deduction. The central model's permanent 35% capital deduction is an abstraction; it does not model contract-specific expiry.

Inputs requiring explicit reviewer judgment: coverage and entry dates; gross capital; existing direct funding; demand after 2030; physical-to-billing demand conversion; geographic shares; national billing pool; future inherited revenue requirements; real construction escalation; financing, life and O&M. Evidence can make them plausible without uniquely identifying them.

## Equations and units

For year `t`, national eligible cumulative capacity in MW is:

```text
Q[t] = (facility_TWh[t] - facility_TWh[2026]) * 1,000,000 / (8,760 * 0.80) * 0.75
new_MW[t] = Q[t] - Q[t-1]
capital[t] = sum(new_MW[v] * 650,000 * 1.01^(v-2026), for active vintages v)
capital_recovery_factor = 0.05 / (1 - 1.05^(-40)) = 0.05827816...
all_in_recovery_factor = capital_recovery_factor + 0.015 = 0.07327816...
```

The model separately assigns each cohort to billing pools. A pool's inherited load and inherited revenue requirement both grow 1% annually. Its new billing share is `s = new_DC_MW / (inherited_MW + new_DC_MW)`. All money below is an annual amount, not the original capital investment.

```text
K = inherited network revenue requirement
C = assigned incremental capital * all_in_recovery_factor
D = assigned incremental capital * 35% * capital_recovery_factor
U = C - D                            # incremental recovery left in the shared pool
E = s * (K + U)                      # baseline shared transmission charge
P0 = D + E                           # baseline, retaining common direct obligations
P1 = C + s*K                         # credited AND
H = max(P0, C)                       # selected higher-of payment benchmark
A = P1 - P0 = (1-s)*U               # additional payments / other-customer relief
B = P1 - H = min(A, s*K)            # above selected higher-of benchmark
```

`D` includes capital funding only; central O&M stays in `U`. CIAC is represented as an annualized avoided-recovery equivalent, not recurring cash receipts. Sum each year's dollars only during 2030-2056. Do not multiply annual charges by 30 again, include recovery after 2056, add A and B together, or take the maximum after aggregating regions and years.

The model holds demand, investment and total required revenue fixed between tariff worlds. Other customers pay `(1-s)*(K+U)` before and `(1-s)*K` after. Both worlds recover `K+C` in total. This proves the transfer identity; it does not establish that all customers are households, or estimate behavioral responses, federal revenue, utility profits, or net economic benefits.

## Worked example and national reconciliation

Suppose DCs are 10% of billing demand, inherited annual costs are $90m, assigned incremental costs $8m, and existing direct obligations $2m. Residual shared cost is $6m. Baseline DC payments are `$2m + 10% * $96m = $11.6m`; credited AND payments are `$8m + 10% * $90m = $17m`. Additional payments are $5.4m; other customers' bill falls from $86.4m to $81m. Their combined payments remain $98m.

If incremental cost is instead $20m, retaining $2m prior direct funding, baseline is $12.8m and AND is $29m. Additional payments are $16.2m, while payments above the higher-of benchmark are $9m. The remaining $7.2m corrects the baseline's shortfall against that benchmark. This is why the two measures need not be equal.

| National central ledger, billion constant-2026 dollars | Value |
| --- | ---: |
| Assigned incremental recovery C | 88.046554 |
| Existing capital funding equivalent D | 24.508215 |
| Residual recovery U | 63.538339 |
| Baseline DC payments P0 | 176.955356 |
| Credited AND payments P1 | 232.974938 |
| Higher-of benchmark, summed by pool and year | 177.395631 |
| Additional payments A | 56.019582 |
| Above higher-of B | 55.579307 |
| AND above incremental cost alone | 144.928385 |
| Baseline above incremental cost alone | 88.908802 |

The final two rows differ by A. They explain why roughly $145bn is not all new money. Against the alternative allocation `C+sK`, the excess is zero by construction. No benchmark is established as the uniquely correct legal or economic cost of service by this arithmetic.

## The $50-100bn range and ITC comparison

The presentation range is selected and rounded, not an estimated statistical interval. The lower scenario changes funding to 50% and gives $46.759bn. The higher scenario combines the EIA growth shape and $0.75m/MW and gives $103.435bn. These were selected for the requested scenario presentation; they do not replace the $56.020bn central case or exhaust uncertainty. The published brief explicitly includes $35.354bn for only post-2029 entrants and $25.855bn for $0.30m/MW costs. Wider joint scenarios remain in `sensitivity.csv`.

JCT JCX-46-21, p.2, item F.1.5, reports the House-passed 2021 BBB transmission ITC's **$11.279bn nominal FY2022-2031** budget cost. The direct-pay component in note 7 is included, not additional. [Annual source amounts and calculation](review/itc-calculation.csv) show each step:

```text
Historical fiscal-year cost, $bn: 0, 0, 0, .788, 1.213, 1.213, 1.213, 2.001, 2.426, 2.425
Real annual amount = historical_nominal_amount / 1.025^(historical_year - 2026)
Illustrative 30-year ITC = 3 * sum(real annual amounts) = $31.673927bn
Central BAAJA / ITC = 56.019582 / 31.673927 = 1.768634
Rounded band / ITC = 50 / 31.673927 to 100 / 31.673927 = 1.578585 to 3.157171
```

The assumed 2.5% inflation convention is not actual historical CPI. Repetition resets the historical startup ramp each decade. This is a deliberately mechanical scale comparison over the 2027-2056 horizon, not a scored permanent credit, current proposal score, or investment-growth forecast. BAAJA collects for 27 years within that horizon. Private bill transfers and federal budget costs are different quantities; the ratio does not establish equivalent customer savings or benefits.

## What the checks do and do not validate

The independent checker validates input integrity, source-value transcription into model JSON, reconstructed growth, regional weights, annualization, the full central ledger, scenario results and JCT arithmetic. Source-value files are extracted data, not substitutes for opening the original document; inspect the URLs and cells in the source register. Original source hashes identify the archived vintages, not the truth of their forecasts.

The earlier Fable review checked the accounting and identified the prior-funding and timing uncertainties. Its unsupported suspicion about the PJM source vintage was resolved against the original workbook in this package's source check. No external human expert has signed off. The outcome of the remaining substantive review is **open**, even if every arithmetic test passes.

Before endorsing the headline, a reviewer should record a separate conclusion on legal coverage/timing, representativeness of capital and funding assumptions, demand extrapolation, billing determinants and rate geography, the chosen cost benchmark, and the suitability of the ITC scaling convention. [Review questions and response form](review/reviewer-response.md) provides spaces for citations, corrections and sign-off without pre-populating an approval.
