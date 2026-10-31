# Fresh central planning estimate — October 31, 2026

The recommended point estimates are **about $55bn additional data-center transmission payments** and **about $55bn above the chosen higher-of service-cost benchmark**. Exact calculations are $56.0196bn and $55.5793bn. Both round to the same headline because embedded charges exceed residual incremental recovery in most modeled pools. Numerical separation is not an objective; the definitions govern the result.

This is a reasoned conditional planning projection. It is not a statistical expected value, nationally observed tariff replay, enactment-weighted score, or official fiscal estimate. It holds load, physical investment and required revenue identical between payment rules. Other-ratepayer relief includes business and existing data-center customers, not only households. No household allocation is inferred.

## What the two numbers measure

For each pool/year, let K be inherited network revenue requirement, s new eligible data centers’ billing share, C their allocated incremental transmission service cost, D the annual service-cost equivalent of preexisting direct funding, and U=C−D the cost left to shared recovery in the baseline.

```
Ordinary embedded component E = s(K+U)
Total baseline payment P0     = D+E
Credited AND payment P1       = C+sK
Higher-of benchmark H         = max(P0,C) = D+max(E,U)

A: additional payments        = P1−P0 = (1−s)U
B: above defined benchmark    = P1−H  = min((1−s)U,sK)
A−B: baseline shortfall       = max(C−P0,0)
```

The full higher-of comparison is apples-to-apples: both branches retain common existing direct obligations. It is not necessary to drop those obligations to compare full incremental cost C with total embedded-tariff obligation P0. Taking maxima within each pool/year, before summation, is essential. Across the central horizon the sum of local maxima is $177.396bn, whereas taking max after national aggregation would incorrectly give $176.955bn and erase local shortfalls.

If higher-of rather than embedded pricing were already the national baseline, incremental AND revenue would be B=$55.579bn. Thus the unknown baseline tariff mix changes the central result only between $55.579bn and $56.020bn **under this central cost and geography scenario**. This narrow difference is not a claim that tariff choice is immaterial under high-cost scenarios.

The amount above incremental cost alone is P1−C=sK=$144.928bn. This inherited-network contribution is not the headline above-higher-of amount. Under the expressly selected fully allocated benchmark C+sK, above-benchmark payment is zero by construction. The choice between higher-of and incremental-plus-inherited cost allocations is not settled by the arithmetic or these project records.

For completeness the results also calculate a pure gross rolled-in tariff benchmark max(s(K+C),C), which removes existing direct funding from the baseline treatment. Its comparison is $75.877bn; it is a different counterfactual and should not be used as new revenue over existing direct obligations. No interpretation of the bill’s full retail or generation provisions is attempted.

## Central choices and why

| Input | Selection and rationale |
|---|---|
| Period | New growth in 2027–2056; charges in 2030–2056, including prospective charges on 2027–2029 entrants. Three-year implementation is a planning assumption. No retroactive pre-2030 collections or after-2056 recovery. |
| Demand | LBNL June 2026 facility-electricity reference: 192 TWh in 2024, 464 in 2028, 649 in 2030. 2026 is geometrically interpolated at 298.476 TWh. Selected 3% growth in 2031–2040 and 1.5% thereafter yields 1,106.811 TWh in 2056. The extension is analyst judgment, not an LBNL forecast. It slows the near-term boom without assuming a permanent stop. |
| Participation | 75% of new national load. Effective jurisdiction/eligibility/connection assumption, not a measured statutory coverage fraction. Texas is approximately 15.7% of EPRI’s medium 2030 state energy; Texas is not identical to ERCOT, and off-grid supply is a separate issue. |
| Capacity | 80% physical load factor, the user’s modeling convention; no additional billing discount in central. A separate 90% physical load-factor sensitivity changes both capital and billing; a billing-only 90% sensitivity leaves capital fixed. |
| Assigned gross capital | $0.65m/MW in 2026 dollars. Includes local facilities plus an allocated portion of wider shared upgrades. Primary local packages often imply $0.29–0.47m/MW; the conditional Entergy full-package example is around $0.77m/MW. $0.65m is a rounded, nonstatistical network-scope judgment above local packages, not the sum of incompatible regional and local ratios. No entire shared regional line is attributed to data centers. |
| Existing direct funding | 35% of assigned capital already funded, central judgment; sensitivities 0% and 70%. Material direct funding exists in AEP/Piketon and Entergy/Meta records, but no national prior-funding average is observed. We assume no direct O&M recovery in central, avoiding the false inference that CIAC automatically pays operating costs. D annualizes funded capital at the same financing/life convention used for C. |
| Real escalation | Cohort construction cost rises 1% annually above general inflation; test 0% and 2%. Equipment, labor and siting constraints justify a modest pressure scenario, not a claim that a published 30-year real escalation forecast exists. A 2056 entrant costs $0.876m/MW in 2026 purchasing power. Existing cohorts’ real capital recovery remains fixed. |
| Recovery | 40 years, 5% real financing, annual O&M 1.5% of escalated original capital. Capital recovery factor 5.8278%; all-in 7.3278%. Real 5% is an explicit levelization judgment, not a filed nominal WACC. This includes principal, financing and O&M; it does not reproduce taxes, ADIT or utility depreciation schedules. Each cohort enters service in its entry year; no replacements within the 30-year horizon. |
| NITS and geography | National starting proxy $95,100/MW-year, checked against actual PJM 2030 growth-weighted NITS ~$94,746. Half of covered new load is assigned to PJM, with actual zonal rates and 2026 NSPLs, distributed using positive 2035-minus-2026 large-load forecast growth. The remaining half uses the residual pool after subtracting PJM inherited recovery and demand from the national totals. Half is an analyst location assumption, not a measured forecast share. |
| Future embedded charges | Other load and inherited revenue requirement each grow 1% annually, holding the ordinary rate before new covered load flat in real dollars. With 2.5% general inflation, that ordinary nominal rate still rises about 2.5%/year. Covered DC growth dilutes inherited rates; separately assigned upgrades increase gross recovery needs. An extra 1% real NITS-growth sensitivity does not materially change A and slightly increases B. Construction escalation and NITS escalation are distinct inputs. |
| Incumbent pool | 829 GW initial national planning-peak proxy, not a measured national tariff billing determinant. Actual PJM zoning improves geography but does not make the remainder an audited national tariff model. |

The central gross capital is not claimed to be a representative empirical mean. It is independently selected using the existing primary-record audit; UCS headlines are not calibration inputs. The 35% deduction is likewise a visible judgment. The most honest response to missing national averages is to show the judgment and sensitivity, not to present a synthetic average as a measured fact.

## Annualization and accounting

All headline dollars are an undiscounted sum of constant-2026-dollar annual service/payment equivalents during 2030–2056. Existing upfront CIAC is represented as an annual avoided capital-recovery equivalent D, not as literal annual receipts. CIAC remains permanently funded; it does not expire at an arbitrary contract date. Time-limited contract expiry is not modeled centrally. Recovery after 2056 is excluded even though assets continue to exist. The central annual service factor is 7.3278%, and capital-only prior funding removes 35% of the 5.8278% capital factor, leaving all 1.5% O&M. The residual initial annual factor is approximately 5.2881% of gross capital.

| Central ledger, $bn | Value |
|---|---:|
| Allocated incremental transmission service cost C | 88.047 |
| Existing capital funding equivalent D | 24.508 |
| Residual incremental cost U | 63.538 |
| Baseline total transmission obligation P0 | 176.955 |
| Higher-of benchmark H, summed within pools | 177.396 |
| Credited AND payment P1 | 232.975 |
| A: added payments / other-ratepayer relief | 56.020 |
| B: payment above chosen higher-of benchmark | 55.579 |
| Baseline shortfall corrected, A−B | 0.440 |
| Inherited contribution above incremental cost, P1−C | 144.928 |

The two headline numbers overlap. Do not sum them. Incremental-dominant pools account for 3.603% of charged billing-MW-years under the retained-direct-funding comparison. Under the different gross rolled-in comparison, 12.428% of exposure has gross incremental cost above gross embedded charges. These are modeled exposure shares, not observed national regime frequencies.

## Sensitivity and interpretation

One-at-a-time gross capital choices $0.30m/$1.00m produce A=$25.86/$86.18bn and B=$25.86/$83.36bn. At $2m, A=$172.37bn and B=$138.57bn: rising incremental cost eventually creates large benchmark shortfalls under embedded pricing, while the extra AND contribution above higher-of is limited by inherited network charges. Escalation does not automatically imply this crossing; the model evaluates it annually by pool.

Flat demand after 2030 gives A=$33.08bn/B=$32.86bn. An EIA U.S. server-growth shape rebased to LBNL facility demand gives A=$89.64bn/B=$88.89bn; this is an analyst splice, not EIA’s facility-energy forecast. LBNL 521/843 TWh endpoints yield A=$41.01/$77.28bn. Cost, demand, coverage and direct funding can combine: selected joint cases are $6.41bn and $222.27bn for A, so the narrower one-way ranges are not confidence intervals or joint bounds. If all capital and O&M are already directly recovered, A and B are zero. Capital-only funding of 100% would still leave O&M to assign.

## Primary evidence and reproduction

- Introduced S.5653 §2107(a)(3): https://www.govinfo.gov/content/pkg/BILLS-119s5653is/xhtml/BILLS-119s5653is.html — embedded plus incremental and credits. Model implementation details are assumptions.
- LBNL June 18, 2026: https://www.energy.gov/documents/united-states-data-center-energy-usage-report-2025-update — demand; original source re-opened October 31.
- PJM rates: https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-integration-trans-service-august-2026-xls.xlsx ; pools: https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-service-peak-loads-2026.pdf ; growth: https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-report-tables.xlsx . Source metadata preserved in copied JSON.
- MISO MTEP25: https://cdn.misoenergy.org/MTEP25731615.zip — LEAP two phases $567.2m/1,200MW=$0.4727m/MW. MTEP26: https://cdn.misoenergy.org/MTEP26%20-%20Draft784746.zip — Hannover/Cannoli local/study package cross-checks, not full national cost.
- Dominion local plan: https://www.pjm.com/-/media/DotCom/committees-groups/committees/teac/2024/20241008/20241008-informational-only---dom-local-plan-submission-of-supplemental-projects-2024.pdf — independently selected local packages imply approximately $0.34m/MW, with net-new-load and upstream-scope limitations.
- AEP March 20, 2026: https://www.aep.com/news/stories/view/10823/ — $4.2bn investment, planned 10GW, prospective customer commitment, re-opened October 31.
- Entergy testimony: https://lpscpubvalence.lpsc.louisiana.gov/portal/PSC/ViewFile?fileId=AUl4qI5mSHA%3D — components funded by CIAC, another via service-agreement revenue. Capital/funding audit retains redactions and load-denominator uncertainty.

Run `python3 calculate.py` in this directory. It regenerates `final-results.json`, `annual.csv`, `pool-ledger.csv`, and `sensitivity.csv`. No external packages or internet are required. Seven named checks and pool/year conservation identities validate accounting. Supporting copied JSON files retain source metadata and are hashed in the results. `calculate.py` is a fresh implementation rather than a change to the prior central-estimate files.

Independent semantic review found no essential accounting flaw; both suggested wording clarifications were incorporated. Parent verification independently reconstructed the national pooled case and checked all 594 central pool/year ledger rows and all 29 scenario ledgers. See `review.txt` and `parent-verification.json`.
