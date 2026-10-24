"""Independent reference arithmetic for the three-control BAAJA comparison.

No import from the shared model or dashboard. All BAAJA amounts are 2026 USD.
Historical JCT amounts are nominal FY2022–31 cash flows, NOT 2021 dollars.
"""
from dataclasses import dataclass, asdict, replace
from math import isclose
from pathlib import Path
import argparse
import json


HISTORICAL_ITC_ANNUAL_BILLION = {
    2022: 0.0, 2023: 0.0, 2024: 0.0, 2025: .788, 2026: 1.213,
    2027: 1.213, 2028: 1.213, 2029: 2.001, 2030: 2.426, 2031: 2.425,
}
ITC_SOURCE = "https://www.govinfo.gov/content/pkg/GOVPUB-Y4_T19_4-PURL-gpo172711/pdf/GOVPUB-Y4_T19_4-PURL-gpo172711.pdf"
CURRENT_BILL = "https://www.govinfo.gov/content/pkg/BILLS-119s5453is/html/BILLS-119s5453is.htm"
SPONSOR = "https://www.energy.senate.gov/press/dem/heinrich-introduces-legislation-to-supports-investments-to-build-a-more-resilient-reliable-grid/"


@dataclass(frozen=True)
class Assumptions:
    growth_scenario: str = 'medium'
    baseline: str = 'embedded'
    capex_per_mw: float = 650_000.
    nits_per_mw_year: float = 95_100.
    load_factor: float = .80
    effective_chargeable_fraction: float = .75
    incumbent_pool_mw: float = 829_000.
    asset_life: int = 40
    real_financing_rate: float = .05
    real_om_fraction: float = .015
    charging_start: int = 2030
    start: int = 2027
    end: int = 2056
    inflation: float = .025
    real_discount: float = .03


def facility_twh(year, p):
    # Independently specified scenario arithmetic, not imported from model.js.
    anchors = {'low': (383, 942 / 833, .005),
               'medium': (596, 1193 / 945, .015),
               'high': (793, 1637 / 1008, .025)}
    endpoint, five_year_multiplier, terminal_rate = anchors[p.growth_scenario]
    if year <= 2030:
        return 300 * (endpoint / 300) ** ((year - 2026) / 4)
    bridge_rate = five_year_multiplier ** .2 - 1
    result = endpoint * five_year_multiplier ** ((min(year, 2035) - 2030) / 5)
    for step in range(1, min(max(year - 2035, 0), 5) + 1):
        result *= 1 + bridge_rate * (1 - step / 5) + terminal_rate * step / 5
    if year > 2040:
        result *= (1 + terminal_rate) ** (year - 2040)
    return result


def reference_ledger(p=Assumptions()):
    assert p.growth_scenario in ('low', 'medium', 'high')
    assert p.baseline in ('embedded', 'higher_of')
    assert 0 < p.load_factor <= 1 and 0 <= p.effective_chargeable_fraction <= 1
    assert p.capex_per_mw >= 0 and p.nits_per_mw_year >= 0
    r = p.real_financing_rate
    crf = (1 / p.asset_life) if r == 0 else r / (1 - (1 + r) ** -p.asset_life)
    annual_increment_per_mw = p.capex_per_mw * (crf + p.real_om_fraction)
    base = p.incumbent_pool_mw * p.nits_per_mw_year
    cohorts = []
    rows = []
    for year in range(p.start, p.end + 1):
        new_mw = max(0, facility_twh(year, p) - facility_twh(year - 1, p)) / 8.76 / p.load_factor * 1000 * p.effective_chargeable_fraction
        cohorts.append((year, new_mw))
        mw = sum(q for entry, q in cohorts if entry <= year)
        incremental = sum(q * annual_increment_per_mw for entry, q in cohorts if 0 <= year - entry < p.asset_life)
        share = mw / (p.incumbent_pool_mw + mw)
        ordinary = share * (base + incremental)
        higher_of = max(ordinary, incremental)
        and_payment = share * base + incremental
        baseline_payment = ordinary if p.baseline == 'embedded' else higher_of
        extra = and_payment - baseline_payment
        above_incremental = and_payment - incremental
        old_higher = base + incremental - baseline_payment
        old_and = base + incremental - and_payment
        assert isclose(extra, old_higher - old_and, abs_tol=.0001)
        expected_extra = (1-share)*incremental if p.baseline == 'embedded' else min(share*base,(1-share)*incremental)
        assert isclose(extra, expected_extra, abs_tol=.0001)
        assert isclose(above_incremental, share * base, abs_tol=.0001)
        if year < p.charging_start:
            extra = above_incremental = 0
        rows.append({
            "year": year, "total_facility_twh": facility_twh(year, p),
            "effective_new_billing_gw": mw / 1000,
            "share": share, "incremental_cost_usd": incremental,
            "ordinary_payment_usd": ordinary, "higher_of_payment_usd": higher_of,
            "AND_payment_usd_if_in_force": and_payment,
            "baseline_payment_usd": baseline_payment,
            "A_extra_AND_vs_baseline_usd": extra,
            "A_extra_AND_vs_higher_of_usd": and_payment-higher_of if year>=p.charging_start else 0,
            "B_above_incremental_transmission_cost_usd": above_incremental,
        })
    summary = {}
    for key in ("A_extra_AND_vs_baseline_usd", "A_extra_AND_vs_higher_of_usd", "B_above_incremental_transmission_cost_usd"):
        summary[key] = {
            "constant_2026_billion": sum(row[key] for row in rows) / 1e9,
            "nominal_billion": sum(row[key] * (1 + p.inflation) ** (row["year"] - 2026) for row in rows) / 1e9,
            "pv_2026_billion": sum(row[key] / (1 + p.real_discount) ** (row["year"] - 2026) for row in rows) / 1e9,
        }
    return {
        "assumptions": asdict(p), "annual_incremental_cost_per_mw": annual_increment_per_mw,
        "endpoint_2056_twh": rows[-1]["total_facility_twh"],
        "effective_new_billing_gw_2056": rows[-1]["effective_new_billing_gw"],
        "metrics": summary, "annual": rows,
    }


def normalized_itc(p=Assumptions()):
    # Positive cost convention; JCT presents the same main-row budget effects negative.
    assert isclose(sum(HISTORICAL_ITC_ANNUAL_BILLION.values()), 11.279, abs_tol=1e-12)
    block = [
        {"historical_fiscal_year": year,
         "historical_nominal_cost_billion": cost,
         "constant_2026_cost_billion": cost / (1 + p.inflation) ** (year - 2026)}
        for year, cost in HISTORICAL_ITC_ANNUAL_BILLION.items()
    ]
    rows = []
    for offset, year in enumerate(range(2027, 2057)):
        amount = block[offset % 10]["constant_2026_cost_billion"]
        rows.append({
            "illustrative_model_year": year,
            "repeated_block": offset // 10 + 1,
            "mapped_historical_fiscal_year": block[offset % 10]["historical_fiscal_year"],
            "constant_2026_cost_billion": amount,
            "nominal_cost_billion": amount * (1 + p.inflation) ** (year - 2026),
            "pv_2026_cost_billion": amount / (1 + p.real_discount) ** (year - 2026),
        })
    real_sum = sum(row["constant_2026_cost_billion"] for row in rows)
    assert isclose(real_sum, 3 * sum(row["constant_2026_cost_billion"] for row in block), abs_tol=1e-12)
    return {
        "status": "Own repeated-program illustration; not official30-year score or forecast of S.5453",
        "normalization": "For each historical FY y, divide JCT nominal positive cost by1.025^(y−2026). Reset this ten-year REAL profile three times over modelyears2027–2036,2037–2046,2047–2056.",
        "inflation_assumption": p.inflation,
        "historical_nominal_10yr_billion": 11.279,
        "mechanical_3x_unharmonized_score_billion": 33.837,
        "historical_10yr_profile_in_constant_2026_billion": sum(row["constant_2026_cost_billion"] for row in block),
        "repeated_30yr_constant_2026_billion": real_sum,
        "repeated_30yr_nominal_billion": sum(row["nominal_cost_billion"] for row in rows),
        "repeated_30yr_pv_2026_billion": sum(row["pv_2026_cost_billion"] for row in rows),
        "historical_block": block, "illustrative_repeated_annual": rows,
    }


def notes_array(p, itc):
    return [
        {
            "id": "official_historical_itc_score", "kind": "official_historical_federal_score",
            "display": "$11.279bn nominal over FY2022–2031",
            "value_billion": 11.279, "unit": "nominal fiscal-year USD, positive federal cost",
            "window": "FY2022–2031", "bill_version": "H.R.5376 Build Back Better Act as passed by House, November19,2021",
            "source": ITC_SOURCE, "locator": "JCT JCX-46-21 page2, SubtitleF, Part1 item5; page8 footnote7",
            "warning": "$3.024bn direct-pay outlay component is included, not additional. Publication in2021 does not make these2021constant dollars.",
        },
        {
            "id": "repeated_30yr_itc_illustration", "kind": "analyst_normalized_repetition",
            "display": "About$32bn over30years, in2026dollars",
            "value_billion": itc["repeated_30yr_constant_2026_billion"],
            "unit": "constant2026USD, undiscounted", "window": "modelyears2027–2056",
            "formula": "3×Σ(y=2022…2031)[JCTcost(y)/(1.025^(y−2026))]",
            "warning": "Three identical real ten-year profiles. Not an official30-year score, not permanent-program steady-state estimate, and not a score of the2026bill. HistoricalFYtiming is shifted to modelyears solely to illustrate common-horizon magnitudes.",
        },
        {
            "id": "current_bill_score_missing", "kind": "unobserved_current_official_score",
            "bill_version": "S.5453 Grid Resiliency Tax Credit Act, introducedSeptember22,2026",
            "value_billion": None, "source": CURRENT_BILL,
            "warning": "No publicJCT/CBOscore located as ofOctober23,2026.30%credit has different eligibility and construction-start sunsetDecember31,2036; historical11.279bn must not be labeled its score.",
        },
        {
            "id": "sponsor_economic_benefits", "kind": "economic_benefit_claim_not_fiscal_score",
            "source": SPONSOR, "value_billion_per_year": 27.7,
            "warning": "Sponsor-cited transmission expansion electricity-bill savings claim, attributed toGridStrategies/ACEG. NotJCT/CBOcost and not ITCfunding.",
        },
        {
            "id": "comparison_scope", "kind": "interpretation",
            "warning": "BAAJAtransfers are private transmission-bill transfers, notTreasuryreceipts or a fiscalpay-for. ITCcost is federalbudgeteffect, not guaranteed ratepayerbenefit. LabelB aboveincremental TRANSMISSIONcost of service; much ofB is already collected through ordinarytariffs. Do not addAandB.",
        },
        {
            "id": "inflation_and_credit_basis", "kind": "normalization_limitation",
            "warning": "The uniform2.5%inflation adjustment is a common model convention, not actual observed/projected CPI for each historical andfutureyear. NetJCTbudgetcost is not an estimate ofgrosseligiblecapital or customer-bill pass-through.30-year utility benefits require separate investment,tax,rate-base,asset-life and pass-through assumptions.",
        },
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nits", type=float, default=95_100.)
    parser.add_argument("--baseline", choices=("embedded", "higher_of"), default="embedded")
    parser.add_argument("--capex", type=float, default=650_000.)
    parser.add_argument("--growth", choices=('low', 'medium', 'high'), default='medium')
    args = parser.parse_args()
    p = Assumptions(growth_scenario=args.growth, baseline=args.baseline, capex_per_mw=args.capex, nits_per_mw_year=args.nits)
    ledger = reference_ledger(p)
    itc = normalized_itc(p)
    # Boundary checks distinguish additional policy payments from embedded contribution.
    assert isclose(reference_ledger(replace(p, capex_per_mw=0))["metrics"]["A_extra_AND_vs_higher_of_usd"]["constant_2026_billion"], 0, abs_tol=1e-10)
    zero_rate = reference_ledger(replace(p, nits_per_mw_year=0))
    assert isclose(zero_rate['metrics']['B_above_incremental_transmission_cost_usd']['constant_2026_billion'],0,abs_tol=1e-10)
    assert isclose(zero_rate['metrics']['A_extra_AND_vs_higher_of_usd']['constant_2026_billion'],0,abs_tol=1e-10)
    target = Path(__file__).resolve().parent
    (target / "itc_comparison_reference_2026_10_23.json").write_text(json.dumps({"BAAJA": ledger, "ITC": itc}, indent=2) + "\n")
    (target / "itc_comparison_notes_2026_10_23.json").write_text(json.dumps(notes_array(p, itc), indent=2) + "\n")
    print(json.dumps({"parameters": asdict(p), "BAAJA": ledger["metrics"], "ITC": {k:v for k,v in itc.items() if k not in ["historical_block", "illustrative_repeated_annual"]}}, indent=2))


if __name__ == "__main__":
    main()
