# BAAJA: who pays for transmission?

*October 26, 2026. All figures from the current transfer analysis.*

[Download the report](baaja-ratepayer-transfer.pdf)

A scenario analysis of additional data-center payments | October 26, 2026

**Working reference: about $50 billion of additional data-center payments, reducing other customers' transmission charges by the same amount.** The calculated result is $46.8 billion in constant 2026 dollars over 2027-2056, with policy charges starting in 2030.

The comparison is against embedded, or rolled-in, pricing. It counts all additional payments: both closing any shortfall in recovery of data-center-related costs and adding a contribution toward the rest of the grid. It does not assume that a utility switches to higher-of pricing when upgrades become expensive.

| Residual network capital per MW | Additional DC payments / other-payer relief |
| --- | --- |
| $0.15 million | $18 billion |
| $0.40 million | $47 billion |
| $0.80 million | $94 billion |
| $1.30 million | $152 billion |
| $2.00 million | $234 billion |

Selected capital scenarios, holding central growth and other assumptions fixed. These imply about $20-235 billion; they are not a confidence interval or exhaustive bounds. The $1.3m and $2m cases are high-cost stresses, not measured national averages.

### Why higher incremental costs increase the policy effect

Under an embedded tariff, other customers share the added network cost. BAAJA shifts that remaining shared obligation to data centers while retaining their contribution toward existing grid costs. At high incremental costs, the payment increase includes correction of a preexisting shortfall. A higher-of comparison excludes that correction and therefore produces a smaller number.

### What can be said with confidence

The accounting mechanism is clear. The national dollar result is conditional, chiefly on the amount of attributable network cost that existing contracts do not already recover directly. Primary project and contract records establish large differences in both costs and customer funding; they do not establish a representative national residual cost per MW.

**Suggested public description:** "Our reference scenario estimates roughly $50 billion in additional data-center transmission payments under BAAJA, with approximately $20-235 billion across selected network-cost scenarios. These payments reduce other customers' charges relative to embedded pricing; the results are conditional on growth, cost allocation and existing payment obligations."

Scope: the transmission pricing provision in introduced S.5653, section 2107(a), modeled with revenue-requirement credits. This is not an official fiscal score, a score of the entire bill, or a finding of overpayment above fully allocated cost of service. Sources and reproducible model are on page 7.

## Two cost regimes, two baselines

The tariff baseline and the size of incremental costs are separate choices.

Let **B** be the annual inherited network revenue requirement, **I** the annual incremental recovery still embedded in shared rates after existing direct funding, and **s** the new eligible data centers' billing share. Already-direct payments common to both worlds cancel. All amounts below are annual.

| Payment or comparison | Calculation |
| --- | --- |
| Embedded baseline | E = s x (B + I) |
| Embedded charge after the credit | E' = s x B |
| Credited AND payment | I + E' |
| Additional payments above embedded | A = (1 - s) x I |
| Additional payments above higher-of | G = min(A, E') |
| Shortfall corrected under embedded | max(I - E, 0) = A - G |

The credit matters: removing incremental receipts from the shared revenue requirement also lowers the data center's embedded charge. Adding the full current NITS charge to incremental recovery without this credit would overstate payments. Total network recovery is unchanged.

### An annual example: $100m inherited cost; 10% DC billing share

| $ million per year | Lower-cost regime | Higher-cost regime |
| --- | --- | --- |
| Incremental cost I | 5.0 | 20.0 |
| Embedded payment E | 10.5 | 12.0 |
| Higher-of payment | 10.5 | 20.0 |
| Credited AND payment | 15.0 | 30.0 |
| Added payment vs embedded A | 4.5 | 18.0 |
| Of which: shortfall correction | 0.0 | 8.0 |
| Added payment vs higher-of G | 4.5 | 10.0 |

In the higher-cost example, AND raises payments by $18m above embedded pricing: $8m closes the shortfall and $10m contributes to inherited costs. If the baseline already required higher-of, only the latter $10m would be additional. Both regimes can occur under an embedded tariff.

This is a constructed example, not a utility observation. In both cases, all additional DC payments equal the reduction in other payers' charges. A share of inherited costs is an above-incremental contribution; it is not automatically above fully allocated cost of service.

## Growth and billing assumptions

Published near-term projections; explicit extrapolation after 2030.

LBNL's June 2026 update provides the reference facility demand of **649 TWh in 2030**, with sensitivity cases of 521-843 TWh. Its modeled historical estimate is 192 TWh for 2024. We interpolate a 2026 baseline of 298.5 TWh using its 2024 and 2028 reference values. [3]

| Year | U.S. facility demand | Basis |
| --- | --- | --- |
| 2026 | 298.5 TWh | Analyst interpolation |
| 2030 | 649 TWh | LBNL reference |
| 2040 | 872 TWh | 3% annual growth after 2030 |
| 2056 | 1,107 TWh | 1.5% annual growth after 2040 |

The post-2030 taper is a planning assumption. It is not a published LBNL forecast. EPRI's 2030 medium case is about 596 TWh, including cryptocurrency; IEA's U.S. reference is 426 TWh. Different scopes and methods make a simple average misleading. [4-5]

| Input | Reference assumption and interpretation |
| --- | --- |
| Facility load factor | 80%, converting energy to physical peak-equivalent MW. |
| Billing demand | Equal to that peak proxy; actual coincident peaks and minimum contract demand can differ. |
| Covered share of new growth | 75%; a selected modeled-grid share, not a measured jurisdictional or statutory coverage fraction. |
| Existing billing pool | 829 GW, a national planning-peak proxy held flat. |
| Inherited transmission rate | $95,100/MW-year in 2026 dollars, held flat in real terms. |
| Cohorts and timing | Growth above the 2026 baseline; entrants from 2027; charges from 2030 through 2056. |

The rate is a national expenditure/peak proxy, **not an observed weighted national NITS tariff**. Actual August 2026 PJM rates, weighted by projected 2030 large-load additions, average about $94,746/MW-year: a useful magnitude check, not national validation. [13]

For a fixed residual cost and billing share, the transfer above embedded pricing does not depend on the inherited NITS rate: A = (1 - s)I. NITS matters for which regime applies and for the additional contribution above a higher-of baseline.

This model excludes cryptocurrency, despite its inclusion in the bill. It does not separately score pre-2027 facilities, generation, distribution, retail bidding mechanisms or broader bill provisions. Covered new capacity grows to 37.5 GW in 2030 and 86.5 GW in 2056. The uncovered share is outside the modeled system, not an in-pool exemption.

## The critical input: residual network cost

Start with attributable infrastructure. Subtract obligations already paid directly.

**The $0.4m/MW reference is an explicit judgment.** It represents attributable network capital still supported through shared rates under the baseline, after existing direct funding. It is not a measured national average and is not a measured percentage of gross project cost.

| Primary-record cross-check | Capital / matched MW | What it establishes |
| --- | --- | --- |
| Dominion: 26 identified DC needs | $1.328bn / 3,891 MW<br>$0.341m/MW | Local plan scope; site forecasts mix years and are not all net-new load. |
| MISO: Hannover + Cannoli | $416.8m / 1,430 MW<br>$0.291m/MW | Selected study packages; not certified complete system scope. |
| MISO: LEAP phases | $567.2m / 1,200 MW<br>$0.473m/MW | Matched network package; funding still needs reconciliation. |
| AEP / SB Energy Piketon | $4.2bn / 10,000 MW<br>$0.420m/MW | Announced customer funding; prospective, not realized collections. |

These cross-checks support costs in the hundreds of thousands of dollars per MW for selected packages. They neither form a representative sample nor establish the amount BAAJA would newly assign. Local scope can omit upstream upgrades; adding broad regional totals can double count or assign unrelated costs. [7-10]

### Existing funding can sharply reduce the additional policy payment

Entergy's Meta/Evest testimony describes two customer-funded transmission projects plus annual recovery for another under a 20-year agreement, with expected full transmission revenue-requirement offsets during that term. Post-term exposure remains. Wisconsin's Ozaukee record identifies about $1.099bn of Oracle-funded equipment within a larger package. Neither package can be treated as entirely newly assignable. [11-12]

We retain $0.4m/MW as a transparent working reference between low local-package cases and more expensive full-network possibilities, while recognizing that direct funding could materially reduce it. The $0.15m and $0.8m cases test lower and higher residual costs. The $1.3m and $2m cases deliberately test expensive systems where incremental recovery approaches or exceeds embedded payments.

The audit does not establish $1.3m-$2m/MW as a typical national residual cost. These are regime stresses. If existing obligations already cover all relevant incremental costs directly, the modeled additional transfer is zero. UCS headline totals and Maryland OPC procurement-window totals are not used to calibrate residual capital. PUDL financial accounts cannot identify DC causation or existing contract recovery on their own.

## Results across both regimes

Billions of constant 2026 dollars; 2027-2056, with charges beginning in 2030.

| Residual capital<br>$m/MW | Added vs<br>embedded | Shortfall<br>correction | Added vs<br>higher-of |
| --- | --- | --- | --- |
| 0.15 | 17.6 | 0.0 | 17.6 |
| 0.40 | 46.8 | 0.0 | 46.8 |
| 0.80 | 93.6 | 0.0 | 93.6 |
| 1.30 | 152.1 | 0.3 | 151.9 |
| 2.00 | 234.1 | 82.2 | 151.9 |

Above the reference cost, the embedded-baseline transfer continues growing. The higher-of comparison eventually levels off because its baseline already requires recovery of incremental costs. In this pooled model, the crossover is approximately $1.30m/MW; this threshold depends on the assumed rate, financing and billing demand.

### A mixed system illustrates why the baseline changes the answer

If half the modeled load and billing pools use the $0.4m/MW case and half use the $2m/MW case, additional payments are **$140.4bn above embedded**, made up of $41.1bn of shortfall correction and $99.3bn above higher-of. This 50/50 mix is a constructed illustration, not an estimate of the national mix.

| Change from reference, one at a time | Added vs embedded |
| --- | --- |
| Reference | $46.8bn |
| No additional growth after 2030 | $28.4bn |
| EIA server-growth shape, rebased to facility demand | $74.9bn |
| 50% / 90% covered growth | $32.0bn / $55.3bn |
| Only post-2029 entrants eligible | $28.0bn |

EIA projects server energy, not total facility use; the rebased path is our conversion assumption. Joint lower/higher scenarios reach approximately $4.6bn/$392bn. These are selected combinations, not bounds or probability estimates. [6,13]

### Transmission ITC: a scale comparison only

JCT scored the House-passed 2021 BBB transmission ITC at $11.279bn nominal over FY2022-2031. Repeating its inflation-normalized ten-year profile three times gives an analyst illustration of $31.7bn in 2026 dollars. BAAJA is of comparable order, but a private bill transfer is not a federal budget cost or a measure of net economic benefits. [14]

## Implementation, accounting and limits

A reproducible conditional estimate, not a national observed subsidy.

The introduced bill requires embedded plus incremental transmission charges with credits to the applicable annual transmission revenue requirement. Our modeled implementation applies those credits before calculating the shared embedded charge. Non-firm service, eligibility, transition rules and project attribution would affect actual implementation. [1]

Embedded pricing is the selected baseline. A February 2026 FERC concurrence describes ComEd agreements with load-ratio-share payments and upgrades rolled into formula rates; it discusses higher-of as an alternative. This establishes an actual embedded example, not the percentage of U.S. data-center load on that structure. [2]

### How the annual calculation works

Each year adds only the new physical MW cohort. Capital is incurred once per cohort and converted to annual recovery with a 40-year life, 5% real financing and 1.5% annual operating cost: a 7.3278% annual factor. Recovery is a levelized approximation, not a filed utility formula rate. The model then calculates each eligible cohort's billing share and the credited transfer in each year; payments outside the horizon are excluded.

At the reference assumptions, $46.8bn of cumulative real transfer is equivalent to $75.4bn nominal using assumed 2.5% annual inflation, or $27.7bn discounted to 2026 at 3% real. These are different dollar conventions for the same modeled stream. No terminal asset value or later bill relief is added.

### Where shared upgrades enter

A project can serve data centers and other customers, replace aging assets or accelerate a previously planned line. The model must assign only the relevant residual share, with documented timing and existing funding. Triggering a project does not establish sole causation. Our capital input summarizes this unresolved allocation; it does not treat all projects labeled "data center" as entirely chargeable to that load.

### What the estimate does and does not measure

With physical investment and total recovery fixed, added eligible-DC payments equal credits to all other payers together. Those payers include households, businesses and any noneligible data centers; the result is not households-only relief. Regional allocation determines who receives it. National relief does not ensure every zone or customer benefits.

The calculation holds load and construction fixed between pricing cases. It does not estimate relocation, non-firm discounts, cancellation, evasion, demand response or induced investment. It assumes the stated prior-recovery offsets persist; expiring agreements can increase later exposure. The full bill could affect other costs and existing sites beyond this modeled cohort.

Payments above incremental cost also contribute to shared infrastructure. Calling the entire contribution an overcharge above fully allocated cost of service would require a separate allocation standard. The defensible headline here is **additional payments and corresponding other-payer relief above the selected tariff baseline**.

## Sources and reproducibility

Primary records and explicit model assumptions; accessed through October 26, 2026.

**[1]** [BAAJA, introduced S.5653, section 2107(a), September 30, 2026](https://www.govinfo.gov/content/pkg/BILLS-119s5653is/xhtml/BILLS-119s5653is.html)

**[2]** [FERC, Commissioner Chang concurrence on ComEd/Aligned, February 17, 2026](https://www.ferc.gov/news-events/news/commissioner-changs-concurrence-transmission-security-agreement-between)

**[3]** [LBNL, United States Data Center Energy Usage Report: 2025 Update, pp.8-9](https://www.energy.gov/documents/united-states-data-center-energy-usage-report-2025-update)

**[4]** [EPRI, Powering Intelligence 2026, annual energy and peak use](https://powering-intelligence.epri.com/annual-peak-use.html)

**[5]** [IEA, Key Questions on Energy and AI, Table A.4, p.110](https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf)

**[6]** [EIA, AEO2026 Table 5, server electricity series](https://www.eia.gov/outlooks/aeo/excel/aeotab5.xlsx)

**[7]** [Dominion, October 2024 local plan of supplemental projects](https://www.pjm.com/-/media/DotCom/committees-groups/committees/teac/2024/20241008/20241008-informational-only---dom-local-plan-submission-of-supplemental-projects-2024.pdf)

**[8]** [MISO MTEP26 package; component records and matching in repository](https://cdn.misoenergy.org/MTEP26%20-%20Draft784746.zip)

**[9]** [MISO MTEP25 package; LEAP phases and matching in repository](https://cdn.misoenergy.org/MTEP25731615.zip)

**[10]** [AEP, Piketon / SB Energy transmission announcement, March 20, 2026](https://www.aep.com/news/stories/view/10823/)

**[11]** [Entergy, Daniel Kline testimony on Evest, March 2026, pp.13-18,33-34](https://lpscpubvalence.lpsc.louisiana.gov/portal/PSC/ViewFile?fileId=AUl4qI5mSHA%3D)

**[12]** [Wisconsin PSC, Ozaukee data-center infrastructure project](https://psc.wi.gov/Pages/CommissionActions/CasePages/OzaukeeDIP.aspx)

**[13]** [Rate arithmetic, PJM inputs, growth and capital evidence with source locators](https://github.com/dashboardamerican/baaja-and-pricing/tree/main/analysis/central-estimate)

**[14]** [JCT JCX-46-21, November 19, 2021, p.2 and footnote 7 on p.8](https://www.govinfo.gov/content/pkg/GOVPUB-Y4_T19_4-PURL-gpo172711/pdf/GOVPUB-Y4_T19_4-PURL-gpo172711.pdf)

### Reproduce the analysis

The repository includes the Python model, annual reference ledger, selected scenarios, primary-source extracts and independent review. Run **score.py**, then **regimes.py**, then **transfer.py** from analysis/central-estimate. The report reads transfer-results.json. Accounting checks reconcile every scenario's extra DC payment to other-payer credits and to shortfall correction plus the gain above higher-of.

Model/report repository: [github.com/dashboardamerican/baaja-and-pricing](https://github.com/dashboardamerican/baaja-and-pricing). The legacy interactive calculator retains earlier assumptions and is not the source of this report. The new report and transfer-results.json govern the figures presented here.

