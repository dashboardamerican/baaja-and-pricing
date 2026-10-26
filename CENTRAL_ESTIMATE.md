# BAAJA transmission payments: central planning estimate

> **October 26 update:** The [current ratepayer-transfer report](RATEPAYER_TRANSFER.md) uses all additional payments above embedded pricing as its primary outcome, including shortfall correction. This earlier assessment focuses on new positive contributions; its reference value coincides, but its high-cost interpretation differs.

October 25, 2026. **Use approximately $50 billion in additional contributions above incremental transmission cost over 2027–2056, in constant 2026 dollars.** The modeled result is $46.8bn, using levelized cost recovery and charges beginning in 2030. This is a conditional planning estimate for new data-center growth, not a measured national expectation or a finding of payments exceeding fully allocated cost of service.

**October 26 clarification:** [The regime analysis](REGIMES.md) models both embedded-dominant and incremental-dominant costs, crossed with embedded-only and higher-of tariff baselines. The $50bn case selects the first cost regime through its inputs. When incremental cost is higher and the baseline is higher-of, the additional AND payment is the post-credit embedded charge. The national regime mix has not been measured.

The estimate counts the contribution newly created by BAAJA. It excludes amounts data centers would contribute under their existing obligations and excludes payments that merely close an existing incremental-cost deficit. It covers transmission; it does not score generation, distribution, cryptocurrency, or the entire bill's other provisions.

The policy scenario implements the embedded-plus-incremental transmission charges and credits in [introduced S.5653, section 2107(a)](https://www.govinfo.gov/content/pkg/BILLS-119s5653is/xhtml/BILLS-119s5653is.html). Separate retail provisions do not supply a uniform national surcharge. The modeled start date and eligibility convention are assumptions about implementation.

## What the number means

Keep the physical grid and data-center growth identical with and without the policy. Compare payments after existing direct-funding obligations and shared-rate credits. For each modeled billing group and year:

```text
New above-cost contribution = max(BAAJA payment − incremental cost, 0)
                            − max(baseline payment − incremental cost, 0)
```

The central calculation has no baseline deficit, so the new above-cost contribution equals the total increase in payments. This equality is a model result, not a national empirical finding. The larger gross post-policy contribution includes money already contributed without the bill:

| Contribution above incremental transmission cost | 2027–2056, 2026 dollars |
| --- | ---: |
| Without BAAJA | $105.1bn |
| With credited AND pricing | $151.9bn |
| **Increase caused by BAAJA** | **$46.8bn** |

The three figures reconcile; they must not be added. Under fixed total required recovery and full credits, the additional payments reduce other customers' transmission bills by the same amount in this simplified pool. This does not establish household-only savings or the result in every zone.

**“Cost” here means incremental transmission service cost, including capital recovery, financing and operating costs.** Fully allocated cost also assigns shared grid costs. The evidence does not support calling $50bn an overcharge above fully allocated cost of service.

## Central assumptions and evidence

| Input | Selected value | Evidence status |
| --- | --- | --- |
| U.S. DC electricity in 2030 | 649 TWh | LBNL reference projection, not actual consumption |
| 2026 baseline | 298.5 TWh | Geometric interpolation between LBNL's 2024 estimate and 2028 projection |
| Growth after 2030 | 3% annually through 2040; 1.5% thereafter | Explicit author judgment; 1,107 TWh in 2056 |
| Effective participating share of new load | 75% | Scope assumption; not a measured FERC-jurisdiction or onsite-power share |
| Facility peak-equivalent conversion | 80% load factor | Requested modeling convention; actual billing peaks remain unmeasured |
| **Residual capital available for new assignment** | **$0.40m/MW** | **Author judgment informed by primary project and funding evidence; not an observed national mean** |
| Recovery | 40 years; 5% real financing; 1.5% annual O&M | Levelized screening convention; annual recovery factor 7.3278% |
| Inherited network charge | $95,100/MW-year | National expenditure/peak proxy; actual PJM growth-weighted NITS is about $94,746 |
| Inherited billing pool | 829 GW | Planning-peak proxy, not audited national tariff billing demand |
| Eligibility and timing | New 2027–2056 cohort; charges from 2030 | Implementation scenario; pre-2030 new entrants are charged prospectively |

[LBNL's June 2026 report](https://www.energy.gov/documents/united-states-data-center-energy-usage-report-2025-update) provides 192 TWh for 2024, 464 TWh for 2028 and 649 TWh for 2030. Its compounded 2030 sensitivities are 521–843 TWh. The report does not forecast 2056. The central extension deliberately slows growth; separate tests use the growth shapes in U.S. EIA server-energy and BNEF installed-capacity projections, with their scope conversions disclosed in the [growth inputs](analysis/central-estimate/growth-audit.json).

EPRI's state data place Texas at about 15.7% of medium-case 2030 U.S. DC energy. Texas is not exactly ERCOT, and onsite supply and statutory eligibility are separate questions. This supports treating 75% as an effective scope assumption rather than claiming it is measured coverage. See [EPRI's dashboard](https://powering-intelligence.epri.com/dashboard/).

## Why use $0.40m/MW?

This is the weakest central input. The available records establish neither a nationally representative gross cost nor a national fraction already paid directly. A point estimate therefore requires a judgment. I select $0.40m/MW of residual newly assignable capital, informed by these primary-record checks:

| Primary evidence | What it shows | Limitation |
| --- | --- | --- |
| Independently identified Dominion DC needs | About $0.34m/MW in selected local projects after excluding one clear existing-load expansion | Site forecasts are not consistently net-new load; wider regional projects and funding are incomplete |
| MISO Hannover and Cannoli packages | About $0.29m/MW across 1,430 MW | Local/study packages; some shared scope remains uncertain |
| MISO LEAP, two phases | $567.2m for 1,200 MW: about $0.47m/MW | Package estimate, not measured national marginal cost or verified net funding |
| AEP/SB Energy Piketon | $4.2bn for a planned 10 GW: $0.42m/MW | Customer funding commitment is prospective; cannot count it all as new BAAJA revenue |
| Entergy/Meta Evest | Major components have CIAC funding; another is recovered through the service agreement | Company testimony, with redactions and post-contract residual risk |

The local packages support costs on the order of several hundred thousand dollars per MW. Wider network needs can increase them. Existing customer funding reduces the amount BAAJA can newly assign. The selected $0.40m/MW balances those considerations; **it is not a calculated average of this sample**. Compared with the prior $0.65m/MW assumption, it leaves about 62% as residual available for new assignment. That equivalent fraction is a modeling judgment, not a measured national funding percentage.

The funding evidence is substantive. [AEP's announcement](https://www.aep.com/news/stories/view/10823/) says SB Energy is committed to paying for the $4.2bn transmission investment. [Entergy's March 2026 testimony](https://lpscpubvalence.lpsc.louisiana.gov/portal/PSC/ViewFile?fileId=AUl4qI5mSHA%3D), especially printed pages 13–18 and 33–34, describes customer-funded components and expected recovery during the agreement. These records prevent treating every proposed transmission dollar as new policy revenue. They do not establish how often those arrangements occur nationally. [Capital audit and limitations](analysis/central-estimate/capital-audit.txt).

UCS's project list and national claims supply **no calibration input** to this estimate. The Dominion selection began with the original utility plan; MISO quantities come from its project records. [Capital calculations](analysis/central-estimate/capital-evidence.json).

Primary project sources: [Dominion's 2024 local plan](https://www.pjm.com/-/media/DotCom/committees-groups/committees/teac/2024/20241008/20241008-informational-only---dom-local-plan-submission-of-supplemental-projects-2024.pdf), [PJM's 2024 RTEP report](https://www.pjm.com/-/media/DotCom/library/reports-notices/2024-rtep/2024-rtep-report.pdf), [MISO MTEP25 archive](https://cdn.misoenergy.org/MTEP25731615.zip), and [MISO MTEP26 draft archive](https://cdn.misoenergy.org/MTEP26%20-%20Draft784746.zip). Cost estimates span source vintages and scopes; they are context for a rounded judgment, not an inflation-harmonized statistical sample.

## How sensitive is $50bn?

The central result survives several distinct accounting and implementation checks at roughly the same scale:

| Change from central, one at a time | New above-cost contribution |
| --- | ---: |
| Central | $46.8bn |
| Actual PJM zonal pools, with half covered growth assigned to PJM | $43.6bn |
| Same regional test, with 70% assigned to PJM | $39.9bn |
| Synthetic nominal utility rate-base recovery profile | $52.6bn |
| Physical demand equivalent to a 90% facility load factor | $42.0bn |
| Construction costs grow 2% annually above inflation | $53.8bn |
| Only post-2029 entrants eligible | $28.0bn |
| No further DC energy growth after 2030 | $28.4bn |
| Faster EIA U.S. server-growth shape, rebased to LBNL facility energy | $74.9bn |
| Residual capital $0.15m/MW | $17.6bn |
| Residual capital $0.80m/MW | $93.6bn |

**$20–100bn is a rounded residual-capital scenario span, not a confidence interval or a bound on all outcomes.** Combining adverse assumptions gives approximately $4.6–151.3bn in the selected joint tests. If all relevant incremental costs are already directly recovered with equivalent credits, additional payments are zero. The 30-year bill outcome also depends on enactment and implementation; no enactment probability is applied.

The regional tests use observed PJM rates and billing pools, but the national share assigned to PJM, future location weights and uniform residual cost remain assumptions. The remaining U.S. is pooled. These are sensitivity tests, not a completed national tariff replay. National pooling can conceal a deficit in one region with a surplus in another; the positive-surplus calculation is therefore also tested within individual PJM zones.

Reducing only coincidence with the billing peak holds physical capital fixed and gives $47.2bn at a 90% multiplier. Changing the physical capacity inferred from energy is a different experiment. An independent reviewer caught and corrected an initial sensitivity that conflated those changes; the central result was unaffected.

## Accounting and reproduction

Let `B` be inherited annual transmission recovery, `U` incremental annual recovery still charged through shared rates after existing direct funding, and `s` the new cohort's billing share. Common already-direct recovery cancels from both payments and cost:

```text
Additional payments = (1 − s) × U
Total post-policy contribution above incremental cost = s × B
New positive contribution = min((1 − s) × U, s × B)
```

The last expression excludes correction of baseline under-recovery. It is evaluated by group in regional tests. Upfront contributions must reduce recoverable capital once; annual contract receipts are credited once. A contract-expiry stress applies only to time-limited annual recovery, not irrevocable CIAC.

The central annual factor converts the selected residual capital into a levelized service-cost equivalent. It includes recovery of principal, financing and O&M, but is not a reproduction of a filed formula rate, tax allowance or ADIT schedule. Its inflation-indexed nominal equivalent is $75.4bn; present value at 3% real is $27.7bn. These are alternate dollar conventions for the same modeled stream, not independent receipt estimates. No recovery after 2056 is counted.

Run `python3 analysis/central-estimate/score.py` using the included JSON inputs. The script uses only Python's standard library, regenerates annual results and sensitivity files, and checks conservation of required recovery, direct-payment credits, grandfathered-customer credits, zero-growth and fully funded cases, and hand-calculated examples. [Annual central ledger](analysis/central-estimate/central-annual.csv) · [All sensitivities](analysis/central-estimate/sensitivity.csv) · [Independent review](analysis/central-estimate/review.txt).

## What can be claimed

Suggested wording: **“Our central planning estimate is that BAAJA's transmission AND pricing would create about $50 billion of additional data-center contributions above incremental transmission service costs over 2027–2056, measured in 2026 dollars. The result depends principally on future growth and transmission costs not already recovered from those customers.”**

This is a defensible transparent scenario judgment. It does not meet the stronger empirical validation standard in [METHODS.md](METHODS.md): representative regional costs, actual contracts and payments, and engineering counterfactuals remain incomplete. A precise expected national value or an unqualified finding of payments above fully allocated cost of service would overstate the evidence. The existing interactive calculator retains its older scenario defaults; this assessment is the current written estimate.
