# Methodology and full source links

## Load and annual network costs

Interpolate LBNL's 192 TWh (2024) and 464 TWh (2028) to a 298.476 TWh baseline in 2026; reach 649 TWh in 2030. Later growth is our assumption. Cumulative new eligible MW = (annual TWh - 298.476) x 1,000,000 / (8,760 x 0.80) x 0.75. Price year-to-year MW additions at $650,000/MW, escalating 1% per year from 2026. [2, 3] Faster case: 649 x EIA server-use[y]/server-use[2030]; extend 2049-2050 growth after 2050. [6]

Annual capital recovery = capital x 0.05 / (1 - 1.05^(-40)); add 1.5% of capital for O&M. Existing direct funding offsets 35% of capital recovery, not O&M. These financial and funding choices are assumptions. Inherited load and K grow 1% annually. Half of covered growth uses PJM pools; the rest uses the residual national pool. [3, 4, 7-15]

## Payments, credits and additional relief

For each region/year, K is inherited annual network cost; C is assigned incremental annual cost; D is prior direct-funding equivalent; s is new DCs' share of billing demand. Baseline payments retain D and share C-D. AND recovers C directly and credits it out of the shared requirement. [1, 3]

Baseline = D + s(K + C - D).  AND = C + sK.  Additional payments = (1-s)(C-D).

Above higher-of = AND - max(baseline, C). Sum region/year results during 2030-2056.

## Reconciliation and ITC comparison

In $bn: AND 232.975 - baseline 176.955 = 56.020 additional; AND - higher-of 177.396 = 55.579. The latter is a chosen benchmark, not a universal cost-of-service finding. JCT annual nominal costs for 2022-2031 are 0, 0, 0, .788, 1.213, 1.213, 1.213, 2.001, 2.426, 2.425. Our 30-year ITC illustration = 3 x sum(cost[y] / 1.025^(y-2026)) = $31.674bn; 56.020 / 31.674 = 1.77. Repetition is not an official score or a comparison of equivalent benefits. [3, 5]

## Sources

[1] S.5653 IS: section 2107(a)(3)-(4), pp.229-231; separate FPA 228(f), p.240.  
https://www.govinfo.gov/content/pkg/BILLS-119s5653is/pdf/BILLS-119s5653is.pdf

[2] LBNL 2025 Update (June 2026): printed pp.8-9, physical PDF pp.10-11.  
https://www.energy.gov/documents/united-states-data-center-energy-usage-report-2025-update

[3] Reviewer guide: input files, source-cell extracts, equations and independent checks.  
https://github.com/dashboardamerican/baaja-and-pricing/blob/main/analysis/fresh-central-2026-10-31/REVIEW_GUIDE.md

[4] AEP Piketon (March 2026): $4.2bn, 10GW and prospective customer-funding commitment.  
https://www.aep.com/news/stories/view/10823/

[5] JCT JCX-46-21: p.2, item F.1.5; p.8, note7. Direct pay is already included.  
https://www.govinfo.gov/content/pkg/GOVPUB-Y4_T19_4-PURL-gpo172711/pdf/GOVPUB-Y4_T19_4-PURL-gpo172711.pdf

[6] EIA AEO2026 Table5: cb2026.d021826b, years C10:AB10; server energy C33:AB33.  
https://www.eia.gov/outlooks/aeo/excel/aeotab5.xlsx

[7] PJM August2026 NITS: column E; exact zonal cells in [3].  
https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-integration-trans-service-august-2026-xls.xlsx

[8] PJM 2026 network service peak loads: p.1, Zonal Peak (MW).  
https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-service-peak-loads-2026.pdf

[9] PJM 2026 forecast: Table B9b, years B7:V7; zone rows8-31.  
https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-report-tables.xlsx

[10] EIA AEO2026 Table54: C81, C136, D136, D140 (national expenditure proxy).  
https://www.eia.gov/outlooks/aeo/supplement/excel/suptab_54.xlsx

[11] Grid Strategies 2025 load-growth report: p.33, 829GW planning-peak proxy.  
https://gridstrategiesllc.com/wp-content/uploads/Grid-Strategies-National-Load-Growth-Report-2025.pdf

[12] Dominion October2024 local plan: selected needs/project pages indexed in [3].  
https://www.pjm.com/-/media/DotCom/committees-groups/committees/teac/2024/20241008/20241008-informational-only---dom-local-plan-submission-of-supplemental-projects-2024.pdf

[13] MISO MTEP25: Appendix A New Local Reliability Projects, IDs50208 and50628.  
https://cdn.misoenergy.org/MTEP25731615.zip

[14] MISO MTEP26 draft: network-package context; matched cases and limitations in [3].  
https://cdn.misoenergy.org/MTEP26%20-%20Draft784746.zip

[15] Entergy Kline testimony: printed pp.33-34 (PDF pp.35-36), customer funding and term.  
https://lpscpubvalence.lpsc.louisiana.gov/portal/PSC/ViewFile?fileId=AUl4qI5mSHA%3D

