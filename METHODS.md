# Methods for estimating data center transmission bill impacts

Updated October 25, 2026. This is the current interpretation and empirical research method for the AND-pricing dashboard. It supersedes earlier use of gross project totals as customer harm, a national capital default as a measured mean, and “above cost of service” when only incremental transmission cost was measured. Existing calculator outputs remain conditional scenarios.

**Current planning assessment:** [The central estimate](CENTRAL_ESTIMATE.md) is approximately $50bn of new contributions above incremental transmission cost over 2027–2056 ($46.8bn calculated). It uses an updated LBNL demand anchor and an explicitly judgmental residual-cost input. This is a conditional working estimate, not completion of the national empirical validation requirements below. The interactive calculator retains its earlier defaults.

The question is **how much existing customers pay because data centers connect, and how BAAJA changes that amount**. More investment, higher published rates, and higher data-center payments answer different parts of this question. The analysis must connect them through the same projects, customers, billing zones and years.

## Compare three worlds

| World | Data center growth | Pricing | Purpose |
| --- | --- | --- | --- |
| 0 | Target new DC cohort absent | Applicable baseline rules | Establish bills and construction without that cohort |
| 1 | Target cohort connects | Actual tariffs and contracts, including existing protections | Measure the effect of DC growth under ordinary practice |
| 2 | Same cohort and physical construction as World 1 | Specified BAAJA implementation, with credits | Isolate the policy's change in who pays |

Keep weather, other customer demand, reliability criteria, generation assumptions and unrelated replacement needs consistent between Worlds 0 and 1. Restudy which transmission projects are needed, their timing and size. A project triggered by a DC can also replace aging equipment or serve other loads; its entire cost is not automatically the difference between the worlds. An accelerated replacement may create a timing cost rather than an entirely new asset cost.

Hold construction and DC demand fixed between Worlds 1 and 2 for the initial pricing comparison. A later behavioral analysis can allow relocation, curtailment, cancellation and changes in investment. Report that analysis separately.

## Report distinct outcomes

For the same specified group of existing customers, let `O0`, `O1` and `O2` be annual transmission bills in the three worlds:

```text
Effect of DC growth under ordinary pricing: H = O1 - O0
Additional bill relief from BAAJA:          R = O1 - O2
Remaining effect with BAAJA:                O2 - O0 = H - R
```

Positive `H` means those customers pay more because the cohort connects. Negative `H` means they benefit under the baseline. Positive `R` measures an additional reduction under BAAJA. It does not by itself show that ordinary pricing undercharged data centers.

Also report the DC cohort's actual payments in Worlds 1 and 2 and its incremental cost of service, using a stated engineering and cost-recovery definition. Payments above incremental cost are a contribution toward other grid costs. They are not automatically an overcharge above fully allocated cost of service, which also assigns shared costs.

To isolate **new positive contributions above incremental cost**, calculate `max(P2 − C, 0) − max(P1 − C, 0)` for each relevant billing group and year, then aggregate. This excludes additional payments that merely repair a preexisting deficit. Under fixed physical costs, the signed contribution change is simply `P2 − P1`; the positive-surplus measure equals it only when baseline incremental cost is already covered. A national pooled positive-part calculation can hide regional deficits, so report regional tests or retain that limitation explicitly.

Identify customer groups before calculating changes: existing households, existing businesses, existing DCs, later noneligible loads and policy-eligible DC cohorts. Eligibility and grandfathering are explicit implementation assumptions. Extra payments by eligible DCs equal relief to **all other payers together** only if total required recovery is unchanged and receipts are fully credited. They need not equal relief to households or to the 2026 incumbent cohort alone.

## A simple annual example

Assume a single pool initially has $100m of annual transmission cost and 1,000MW of billing demand. A new DC adds 100MW and $15m of annual cost. There are no upfront contributions, other revenue sources or demand changes.

| World | Total annual requirement | New DC pays | Existing customers pay |
| --- | ---: | ---: | ---: |
| 0 Without DC | $100.00m | $0 | $100.00m |
| 1 Embedded pricing | $115.00m | $10.45m | $104.55m |
| 2 Credited AND | $115.00m | $24.09m | $90.91m |

DC growth raises existing bills by $4.55m under the baseline. BAAJA reduces those bills by $13.64m relative to that baseline: it offsets the $4.55m increase and provides another $9.09m contribution toward inherited costs. Thus additional policy relief can exceed the harm being corrected.

If the same DC adds only $5m of annual cost, ordinary pricing already reduces existing bills by $4.55m. AND produces a further $4.55m reduction. This is a different outcome from correcting a subsidy. These are selected illustrations, not utility observations. [Exact example calculations](data/evidence/methods-examples.json).

## Build the evidence from primary records

| Evidence | What it can establish | What it cannot establish alone |
| --- | --- | --- |
| Utility financial reports and FERC accounts accessed through PUDL | Historical spending, plant additions, balances, functional expenses and some revenues | The DC-caused share or a customer-specific subsidy |
| Utility studies and ISO project records | Scope, need, estimated costs, project IDs and reported status | Actual expenditure or actual load solely because an asset is marked in service |
| Filed formula rates, NITS, TEC and retail schedules | Recoverable costs, billing determinants, charges and credits | Realized customer payments from announced capacity alone |
| Executed service agreements and public contract exhibits | Contributions, refunds, minimum bills, security and exit terms | Revenue equal to the face amount of collateral or guaranteed demand |
| Metered customer demand and billing records | Realized energy, peak contribution, payments and ramp | A no-DC engineering counterfactual |
| Studies, complaints and advocacy reports | Claims, mechanisms and source leads to investigate | A substitute for verifying the underlying quantitative inputs |

Record source date and data vintage separately. Classify values as observed, filed, estimated, modeled or missing. Preserve units, project IDs, source locators and hashes. Unknown customer identity or undisclosed funding remains unknown. Neither becomes zero.

The UCS audit found material accounting and classification defects in its September 2025 transmission inventory, including a Nucor steel-mill project. Its remaining reconciled capital is not a verified DC-only total. Use the [audit findings](data/evidence/ucs-audit-findings.json), [numeric bridge](data/evidence/ucs-audit-bridge.csv) and [scope](data/evidence/ucs-audit-summary.json) as a record of corrections, not as calibration for national capital per MW.

## Match projects and customer cohorts

Use the customer request or need as the starting unit, then join every associated direct facility, network upgrade and shared mitigation by project ID. Count each physical component once. Preserve temporary service, permanent phases, earlier investments and multi-customer work. Match the numerator to the same demand cohort and service horizon.

Separate explicit DC identities, confirmed other industries and unverified large customers. A selected disclosure sample is not nationally representative. Publish scope completeness and exclusions alongside any cost intensity. Do not divide total utility transmission investment by only the DC capacity connected that year.

Estimate incremental costs using studies with and without the cohort where available. Shared regional investments require a stated attribution method and benefits analysis. Distinguish engineering necessity, legal allocation, private funding and customer incidence; none uniquely determines all the others.

## Reconstruct annual recovery and actual payments

Convert attributable investment into the approved annual revenue requirement by asset and utility: service date, depreciation, capital returns, taxes, accumulated deferred taxes, incremental operating costs and relevant credits. Include construction-period recovery where applicable. Keep the initial financing model in nominal dollars, then convert outputs consistently for comparison.

Track funding and payments in a cash-flow ledger:

- Upfront customer contributions reduce the capital subsequently recoverable from shared rates, subject to actual refund, tax and credit terms. Record their cash timing separately.
- Annual direct recovery must be credited against shared recovery where the policy or contract requires it. Count the receipt and its credit once each.
- Minimum bills affect collections when they bind. A demand guarantee that merely secures ordinary tariff payments is not automatically extra revenue.
- Collateral is security until drawn or otherwise recognized as a payment. Exit obligations require a realized or explicitly modeled event.

Calculate World 1 using the actual contract, including direct recovery already required. Do not assume the absence of a tariff called AND means all incremental payments under BAAJA would be additional. A selected prior-recovery percentage is a sensitivity, not a replacement for the contract ledger.

Reconcile shared bills, annual direct receipts and other credited revenues to the applicable recoverable annual requirement. Reconcile upfront funding to the asset cost and rate base separately. This prevents counting a customer contribution once as a rate-base reduction and again as an extra annual deduction. Retain negative credits and unresolved accounting residuals visibly.

## Follow costs and credits across zones

Assign each project's annual recovery to responsible zones under the applicable project-specific allocation. Then apply state retail allocation to identify the customers charged. Use each zone's actual billing determinants and reconcile separate TEC charges and credits, riders and bundled recovery.

A DC's host zone may gain revenue while another zone receives costs without new load. Report both outcomes. Check that BAAJA credits reach the customers whose shared charges fall; a national total does not establish that every zone benefits. Host-only and pooled models are alternative assumptions, not general upper or lower bounds.

For a single pool without other revenues or direct funding, inherited cost `B0`, inherited billing demand `N`, new demand `Q`, and added annual cost `I` give:

```text
Before rate = B0 / N
After rate  = (B0 + I) / (N + Q)
Rate falls when I / Q < B0 / N
```

This is a useful screening condition. It does not establish the sign nationally. A financing-based capital threshold is conditional on that pool's rates, costs and recovery profile.

## Treat growth and costs as connected assumptions

Near-term demand should distinguish energized load, executed agreements, study requests and announcements. Reconcile IT power, facility demand, contracted capacity, annual energy and coincident billing peak. The dashboard's fixed 80% load factor converts energy into a facility peak-equivalent proxy; it does not prove 80% coincidence, flexibility or an actual transmission billing peak.

Apply capital to new or expanded capacity by cohort, with construction and revenue ramps. Do not charge the entire accumulated load stock a new capital cost each year. Do not add temporary and ultimate MW as separate customers. Include departures and equipment life if they fall inside the modeled horizon.

Beyond the supported forecast horizon, use explicit scenarios for demand growth, location, capacity constraints, capital intensity, delays and tariff changes. A high-growth path may also change marginal network costs. Low, Medium and High are scenarios rather than confidence limits. Present capital per MW as a regional or project assumption until a representative, consistently scoped empirical estimate exists.

## Aggregate and compare only after reconciliation

First report annual outcomes by cohort, zone and customer class. Aggregate to a national result using stated coverage and location weights; disclose how uncovered regions and missing contracts are treated. Historical actuals, near-term committed projects and long-run extrapolations remain separate in the output.

Report nominal annual cash flows, a common constant-dollar cumulative total and present value with a stated base year and discount rate. Document treatment of assets still recovering costs after the horizon. Do not infer lifetime relief from a partial recovery window.

For the transmission ITC comparison, retain the official JCT score's original policy and scoring window. Any 30-year extension is an analyst scenario. Compare it with **additional BAAJA payments**, using consistent dollar conventions and clearly different payers. A federal budget cost, private bill transfer and net economic benefit are distinct measures; none automatically equals the others. Tax-credit pass-through, project additionality and financing benefits require their own analysis.

## Current status and next empirical work

The calculator's approximately $75bn central additional-payment result remains a conditional benchmark. The $0.65m/MW capital default, 75% participation, national billing pool, absence of prior-recovery offsets and long-run growth are not jointly calibrated to observed customer outcomes. Changing the method does not turn those existing inputs into evidence.

The next useful calculation is a matched regional case: independently identified DC cohort; complete direct and shared project scope; annual approved recovery; actual ramp and contract payments; zonal allocation; and existing-customer bills in all three worlds. Show which inputs are measured and which remain scenarios. Expand the same ledger across regions before attaching a national point estimate or statistical range.

A publishable national estimate requires traceable identities and scope, consistent demand and cost vintages, a defensible without-DC comparison, reconciliation of existing obligations, credit allocation and customer bills, and an explicit method for weighting missing regions. Until those conditions hold, publish conditional scenario surfaces rather than a validated national subsidy or fiscal score.
