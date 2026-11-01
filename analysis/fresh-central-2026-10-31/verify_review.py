"""Independent, offline audit. Standard library only; never imports production code."""
from pathlib import Path
import csv
import hashlib
import json
import math
import sys

ROOT=Path(__file__).resolve().parent
def read(name): return json.loads((ROOT/name).read_text())
def close(a,b,label):
    if not math.isclose(float(a),float(b),rel_tol=2e-10,abs_tol=1e-7):
        raise AssertionError(f'{label}: {a} != {b}')

def audit():
    checks=[]
    hashes=read('review/file-hashes.json')
    for name,expected in hashes.items():
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual!=expected: raise AssertionError('File integrity: '+name)
    checks.append(f'File integrity: {len(hashes)} files')
    g=read('growth-audit.json'); pjm=read('pjm-regional-inputs.json')
    ref=read('results-summary.json'); brief=read('brief-scenarios.json')
    p=ref['central']['inputs']
    anchors={};rate_source={}
    source_rows=list(csv.DictReader((ROOT/'review/source-values.csv').open()))
    for row in source_rows:
        key=row['model_key'];value=float(row['value'])
        if row['source_id']=='LBNL': anchors[key]=value
        elif row['source_id']=='PJM_RATES': close(pjm['rates_USD_per_MW_year'][key],value,key)
        elif row['source_id']=='PJM_PEAKS': close(pjm['incumbent_MW'][key],value,key)
        elif row['source_id']=='PJM_GROWTH':
            zone,year=key.split(':');close(pjm['large_load_forecast_B9b_MW'][zone][year],value,key)
        elif row['source_id']=='EIA_GROWTH':
            close(g['source_anchors']['EIA_AEO2026']['server_TWh'][key],value/.003412,key)
        elif row['source_id']=='EIA_RATE':rate_source[key]=value
    checks.append(f'Source-value to input-JSON agreement: {len(source_rows)} numeric entries (original source review remains separate)')
    national=read('review/national-rate-proxy.json')['national_proxy']
    peak=national['aggregated_utility_forecast_2025_summer_peak_GW']
    proxy=rate_source['sales2025']*rate_source['tx2025']*1e7/(peak*1000)*rate_source['nominal2026']/rate_source['real2026']
    close(proxy,national['rate_2026_dollars_per_MW_year'],'national rate proxy')
    close(round(proxy/100)*100,p['national_initial_rate_per_MW'],'rounded rate')
    close(peak*1000,p['incumbent_MW'],'planning peak')
    checks.append('EIA cell-derived national rate proxy and explicit rounding; secondary planning-peak input identified')
    demand={y:anchors['2024']*(anchors['2028']/anchors['2024'])**((y-2024)/4) for y in range(2024,2029)}
    demand[2029]=math.sqrt(anchors['2028']*anchors['2030']); demand[2030]=anchors['2030']
    for y in range(2031,2057): demand[y]=demand[y-1]*(1.03 if y<=2040 else 1.015)
    for y,v in demand.items(): close(g['annual_paths_TWh']['central'][str(y)],v,str(y))
    eia=g['source_anchors']['EIA_AEO2026']['server_TWh']
    fast={y:(v if y<=2030 else 649*eia[str(y)]/eia['2030']) for y,v in demand.items() if y<=2050}
    for y in range(2051,2057): fast[y]=fast[y-1]*eia['2050']/eia['2049']
    for y,v in fast.items(): close(g['annual_paths_TWh']['eia_shape'][str(y)],v,'fast '+str(y))
    checks.append('Independent central and faster demand reconstruction')

    def reconstruct(overrides=None, first_entry=2027):
        v={**p,**(overrides or {})}
        path={int(y):q for y,q in g['annual_paths_TWh'][v['growth_path']].items()}
        if v['anchor2030'] is not None:
            ratio=v['anchor2030']/path[2030]
            for y in range(2027,2057): path[y]=path[2026]*(v['anchor2030']/path[2026])**((y-2026)/4) if y<=2030 else path[y]*ratio
        q={y:max(0,path[y]-path[2026])*1e6/(8760*v['physical_load_factor'])*v['coverage'] for y in range(2026,2057)}
        if v['regional']:
            weights={z:max(0,pjm['large_load_forecast_B9b_MW'][z]['2035']-pjm['large_load_forecast_B9b_MW'][z]['2026']) for z in pjm['incumbent_MW']}
            sw=sum(weights.values())
            pools={z:(n,n*pjm['rates_USD_per_MW_year'][z],v['pjm_new_load_share']*weights[z]/sw) for z,n in pjm['incumbent_MW'].items()}
            pools['Other_US']=(v['incumbent_MW']-sum(x[0] for x in pools.values()),v['incumbent_MW']*v['national_initial_rate_per_MW']-sum(x[1] for x in pools.values()),1-v['pjm_new_load_share'])
        else:pools={'US':(v['incumbent_MW'],v['incumbent_MW']*v['national_initial_rate_per_MW'],1)}
        close(sum(x[2] for x in pools.values()),1,'pool weights')
        f=v['real_financing']/(1-(1+v['real_financing'])**(-v['recovery_life']))
        totals={k:0. for k in ['gross_incremental_cost','common_existing_direct_equivalent','residual_incremental_cost','baseline_embedded_payment','higher_of_benchmark','and_payment','extra_above_baseline','total_above_defined_cost','baseline_shortfall_to_benchmark','above_incremental_cost','baseline_above_incremental_signed','other_ratepayer_relief','above_selected_fully_allocated','pure_gross_rollin_higherof','above_pure_gross_rollin_higherof','nominal_extra_above_baseline','PV3_extra_above_baseline']}
        rows={}
        for y in range(v['policy_start'],2057):
            full_cap=eligible_cap=0.
            for entry in range(2027,y+1):
                if y-entry>=v['recovery_life']:continue
                investment=(q[entry]-q[entry-1])*v['gross_capital_million_per_MW']*1e6*(1+v['real_capital_escalation'])**(entry-2026)
                full_cap+=investment
                if entry>=first_entry:eligible_cap+=investment
            for zone,(n0,k0,w) in pools.items():
                n=n0*(1+v['incumbent_load_growth'])**(y-2026)
                all_mw=q[y]*w*v['billing_multiplier'];new_mw=(q[y]-q[first_entry-1])*w*v['billing_multiplier']
                s=new_mw/(n+all_mw)
                capital=eligible_cap*w
                c=capital*(f+v['annual_om_fraction'])
                d=capital*(f*v['existing_direct_fraction']+v['annual_om_fraction']*v['existing_om_direct_fraction'])
                u=c-d
                old_u=(full_cap-eligible_cap)*w*(f*(1-v['existing_direct_fraction'])+v['annual_om_fraction']*(1-v['existing_om_direct_fraction']))
                k=k0*(1+v['inherited_revenue_growth'])**(y-2026)+old_u
                pre=d+s*(k+u);post=c+s*k;high=max(pre,c);gross_high=max(s*(k+c),c)
                a=post-pre;b=post-high
                close(a,(1-s)*u,'transfer');close(pre+(1-s)*(k+u),k+c,'baseline conservation');close(post+(1-s)*k,k+c,'AND conservation')
                vals=dict(gross_incremental_cost=c,common_existing_direct_equivalent=d,residual_incremental_cost=u,baseline_embedded_payment=pre,higher_of_benchmark=high,and_payment=post,extra_above_baseline=a,total_above_defined_cost=b,baseline_shortfall_to_benchmark=high-pre,above_incremental_cost=post-c,baseline_above_incremental_signed=pre-c,other_ratepayer_relief=(1-s)*u,above_selected_fully_allocated=post-(c+s*k),pure_gross_rollin_higherof=gross_high,above_pure_gross_rollin_higherof=post-gross_high,nominal_extra_above_baseline=a*(1+v['inflation'])**(y-2026),PV3_extra_above_baseline=a/1.03**(y-2026))
                rows[(y,zone)]={k:v/1e9 for k,v in vals.items()}
                for name,value in vals.items():totals[name]+=value/1e9
        return totals,rows

    totals,rows=reconstruct()
    for name,value in ref['central']['totals_billion_2026_USD'].items():close(totals[name],value,name)
    ledger=list(csv.DictReader((ROOT/'pool-ledger.csv').open()))
    if len(ledger)!=len(rows) or len(rows)!=594:raise AssertionError('central row count')
    for r in ledger:
        for name,value in rows[(int(r['year']),r['pool'])].items():
            if name in r:close(r[name],value,'ledger '+name)
    for r in csv.DictReader((ROOT/'annual.csv').open()):
        y=int(r['year'])
        for name in totals:
            close(r[name],sum(v[name] for (year,zone),v in rows.items() if year==y),'annual '+name)
    checks.append('594 region-year rows and all central annual/national payment columns independently reconstructed; conservation in each row')
    scenario_csv={r['scenario']:r for r in csv.DictReader((ROOT/'sensitivity.csv').open())}
    for r in ref['sensitivities']:
        t,_=reconstruct(r['changed_inputs'])
        for name,value in t.items():
            close(r[name],value,r['scenario']+' '+name)
            close(scenario_csv[r['scenario']][name],value,r['scenario']+' CSV '+name)
    checks.append(f'All {len(ref["sensitivities"])} published sensitivity cases independently reconstructed')
    for name,case in brief['scenarios'].items():
        t,_=reconstruct(case.get('overrides'),first_entry=2030 if name=='only_2030_and_later_entrants' else 2027)
        close(t['extra_above_baseline'],case['additional_payments_bn'],name)
        close(t['total_above_defined_cost'],case['above_higherof_bn'],name+' higher-of')
    checks.append('All five brief scenarios, including entrant-date sensitivity, independently reconstructed')
    jct=[float(r['nominal_cost_bn']) for r in csv.DictReader((ROOT/'review/itc-calculation.csv').open())]
    close(sum(jct),11.279,'JCT official total')
    normalized=3*sum(v/(1.025**(y-2026)) for y,v in zip(range(2022,2032),jct))
    close(normalized,brief['itc']['illustrative_30year_bn'],'ITC repetition')
    close(totals['extra_above_baseline']/normalized,brief['comparison']['central_multiple'],'ITC ratio')
    for n,r in zip([50,100],brief['comparison']['rounded_band_multiples']):close(n/normalized,r,'band ratio')
    checks.append('JCT annual total, inflation normalization, 30-year repetition and all comparison ratios')
    return dict(status='PASS',checks=checks,limitations='Reproducibility and arithmetic only. Transcription cross-checks use archived extracted source values; source documents, legal implementation and empirical representativeness require separate review.',central_additional_bn=totals['extra_above_baseline'],central_above_higherof_bn=totals['total_above_defined_cost'])

if __name__=='__main__':
    try:print(json.dumps(audit(),indent=2))
    except Exception as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)},indent=2));sys.exit(1)
