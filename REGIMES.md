# Two cost regimes, two tariff baselines

October 26, 2026. The model now explicitly reports embedded-only and higher-of payments, AND payments, the increase above each baseline, and the share of modeled billing exposure in each cost regime. These are conditional scenarios, not measured U.S. regime frequencies.

Two separate questions determine the result: whether incremental cost is above or below the ordinary embedded charge, and whether the actual baseline tariff is embedded-only or higher-of. An embedded-only tariff can remain in effect even when incremental costs exceed its charge. That creates a baseline cost-recovery shortfall; it does not automatically make the tariff higher-of.

## Definitions and credit

Let `E` be the ordinary embedded transmission charge before BAAJA's new direct-payment credit; `I` the attributable annual incremental recovery not already directly funded; and `E_after` the embedded charge after the credit. Common existing direct payments are included equally in both worlds and omitted here for clarity. Then:

```text
Embedded-only baseline: E
Higher-of baseline:     max(E, I)
Credited AND payment:   I + E_after
```

For inherited revenue requirement `B` and the new customer's billing share `s`, the single-pool implementation is:

```text
E       = s × (B + I)
E_after = s × B = E − s × I
```

This applies incremental-payment credits to the shared requirement before calculating everyone's embedded charge. [BAAJA section 2107(a)(3)](https://www.govinfo.gov/content/pkg/BILLS-119s5653is/xhtml/BILLS-119s5653is.html) requires both charges and revenue credits; it does not prescribe every implementation detail. The model is one consistent interpretation.

## What happens in each regime?

| Cost regime | Higher-of baseline pays | AND adds above higher-of |
| --- | --- | --- |
| Embedded charge exceeds incremental cost: `E ≥ I` | `E` | Incremental cost less the customer's own credit: `(1−s)I` |
| Incremental cost exceeds embedded charge: `I > E` | `I` | **The full remaining embedded charge: `E_after`** |

Thus the intuition that AND puts an embedded/NITS charge on top of incremental cost is correct in the second regime. The charge is the **post-credit** embedded amount, not necessarily today's unchanged published NITS bill.

With an embedded-only baseline, additional payments are `(1−s)I` in either regime. In the second regime, part covers `I−E`, the baseline shortfall; only the remainder is above the higher-of benchmark. The resulting identities are:

```text
Above embedded-only = (1−s)I
Above higher-of     = min((1−s)I, sB)
Difference         = max(I−E, 0)
```

These calculations do not establish which cost allocation is normatively correct for shared upgrades. Higher-of is an explicit benchmark, not an independently verified fully allocated cost of service.

## Annual example

Inherited annual network recovery is $100m and the data center's billing share is 10%.

| Annual amount | Embedded-dominant case | Incremental-dominant case |
| --- | ---: | ---: |
| Incremental cost | $5m | $20m |
| Ordinary embedded charge | $10.5m | $12m |
| Higher-of payment | $10.5m | $20m |
| Embedded charge after AND credit | $10m | $10m |
| AND payment | $15m | $30m |
| Additional versus embedded-only | $4.5m | $18m |
| **Additional versus higher-of** | **$4.5m** | **$10m** |

In the right column, $8m of the increase from an embedded-only baseline closes a shortfall, while $10m is the embedded contribution stacked on top of incremental recovery.

## National scenario results

The earlier approximately $50bn central planning case selects $0.40m/MW of residual capital. At its 7.3278% annual recovery factor, that is approximately $29,311/MW-year. Its inherited rate proxy is $95,100/MW-year. Those assumptions place the homogeneous national model in the embedded-dominant regime in every charged year. **The model selected that regime; it did not observe that it applies nationally.**

Under otherwise unchanged single-pool assumptions, the crossover is approximately $1.30m/MW. A $2m/MW residual-capital stress case is incremental-dominant. Regional rates, cost profiles, existing direct funding and billing determinants change the crossover.

| 2027–2056 scenario, constant 2026 dollars | Above embedded-only | Above higher-of |
| --- | ---: | ---: |
| Selected low residual cost, $0.40m/MW | $46.8bn | $46.8bn |
| Selected high residual cost, $2.00m/MW | $234.1bn | $151.9bn |

For illustration, split both inherited demand and new load among separate proportional pools, assigning some billing exposure to each cost case. This preserves the same total growth, inherited costs and participation. It changes the cost mix, not merely the tariff label:

| Selected share in the high-cost case | Additional AND payments above higher-of |
| --- | ---: |
| 0% | $46.8bn |
| 25% | $73.1bn |
| 50% | $99.3bn |
| 75% | $125.6bn |
| 100% | $151.9bn |

**Approximately $100bn is mathematically consistent with a selected 50/50 mixture of these two cases. There is no evidence here establishing that mixture—or the $2m/MW residual cost—as a national central assumption.** The weights represent billing exposure across proportional pools, not counts of sites. Different locations, rates and costs require a regional sum, not blindly applying this interpolation.

The actual-PJM-zone sensitivity with $0.40m/MW places approximately 2.1% of its combined modeled billing exposure in the incremental-dominant regime. That also is a result of assumed costs and location weights, not an observation of actual customer costs. At $0.80m/MW the corresponding modeled share rises to 14.7%.

## Evidence and next measurement

Rolled-in treatment is documented. [Commissioner Chang's February 2026 ComEd concurrence](https://www.ferc.gov/news-events/news/commissioner-changs-concurrence-transmission-security-agreement-between) describes commitments to pay a load-ratio share and upgrades being rolled into shared rates; it discusses higher-of as an alternative protection. This is evidence for that arrangement, not a census proving a national majority. Actual direct-funding and contract obligations remain important in either regime.

The empirical objective is now explicit: for each cohort and zone, estimate the ordinary embedded bill and attributable incremental recovery on the same annual basis, reconcile existing funding, identify the actual tariff baseline, and weight the results by billed demand and time. Shared-project attribution remains part of that work.

[Regime calculations](analysis/central-estimate/regime-results.json) · [Reproducible regime script](analysis/central-estimate/regimes.py) · [Full model](analysis/central-estimate/score.py). Run `python3 analysis/central-estimate/score.py` and then `python3 analysis/central-estimate/regimes.py`. The new regime outputs supplement the October 25 central assessment; they do not replace its selected inputs with an observed national mix.
