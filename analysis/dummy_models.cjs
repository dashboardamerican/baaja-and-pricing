'use strict';
/* Synthetic diagnostic cases, not an empirical estimate or calibrated forecast.
   Run: node analysis/dummy_models.cjs
   Writes data/dummy-models.json. Does not change the dashboard's model. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const model=require('../model.js');
const annualFactor=.05/(1-Math.pow(1.05,-40))+.015;
const close=(a,b)=>assert(Math.abs(a-b)<1e-6*Math.max(1,Math.abs(b)));

function ledger({name,incumbentMW=10000,newMW=1000,nitsKWYear=95.1,capitalMillionMW}){
 const inherited=incumbentMW*nitsKWYear*1000;
 const incremental=newMW*capitalMillionMW*1e6*annualFactor;
 const share=newMW/(incumbentMW+newMW),total=inherited+incremental;
 const embedded=share*total,higherOf=Math.max(embedded,incremental),and=share*inherited+incremental;
 const aEmbedded=and-embedded,aHigherOf=and-higherOf,b=and-incremental;
 const otherEmbedded=total-embedded,otherHigherOf=total-higherOf,otherAND=total-and;
 close(aEmbedded,otherEmbedded-otherAND);close(aHigherOf,otherHigherOf-otherAND);
 close(aEmbedded,(1-share)*incremental);close(b,share*inherited);
 close(and+otherAND,total);
 return {name,inputs:{incumbentMW,newMW,nitsKWYear,capitalMillionMW},
  annualMillion:{incremental:incremental/1e6,embedded:embedded/1e6,higherOf:higherOf/1e6,
   AND:and/1e6,additionalVsEmbedded:aEmbedded/1e6,additionalVsHigherOf:aHigherOf/1e6,
   aboveIncrementalCost:b/1e6,incrementalCostShiftToOthersUnderEmbedded:(incremental-embedded)/1e6}};
}
const cases=[['Low-cost connection',.25],['Dashboard capital assumption',.65],['Expensive connection',2]]
 .map(([name,capitalMillionMW])=>ledger({name,capitalMillionMW}));
assert(cases[0].annualMillion.embedded>cases[0].annualMillion.incremental);
assert(cases[2].annualMillion.embedded<cases[2].annualMillion.incremental);
assert(cases[2].annualMillion.additionalVsEmbedded>cases[2].annualMillion.aboveIncrementalCost);
const zero=ledger({name:'Boundary: no new capital',capitalMillionMW:0});
close(zero.annualMillion.additionalVsEmbedded,0);

// Equal new/old demand ratios isolate the nonlinear higher-of aggregation effect.
const regions=[cases[0],cases[2]],pooled=ledger({name:'Two regions pooled',incumbentMW:20000,newMW:2000,capitalMillionMW:(.25+2)/2});
const regionSum=Object.fromEntries(Object.keys(pooled.annualMillion).map(k=>[k,regions.reduce((s,r)=>s+r.annualMillion[k],0)]));
close(pooled.annualMillion.additionalVsEmbedded,regionSum.additionalVsEmbedded);
assert(pooled.annualMillion.additionalVsHigherOf>regionSum.additionalVsHigherOf);

// Replay existing 30-year paths with both counterfactuals, keeping all other inputs unchanged.
const horizonCases=[];
for(const growth of ['low','medium','high'])for(const cost of [.25,.65,1.3,2]){
 const r=model.calculate({growth,cost,baseline:'higher_of'});
 const embedded=r.rows.filter(x=>x.policyOn).reduce((s,x)=>s+x.ANDPayment-x.ordinaryPayment,0)/1e9;
 horizonCases.push({growth,capitalMillionMW:cost,nitsKWYear:r.params.nits,
  additionalVsEmbeddedBillion:embedded,additionalVsHigherOfBillion:r.A,aboveIncrementalCostBillion:r.B});
}
const output={status:'Synthetic mechanism tests and conditional sensitivity runs; not a national forecast.',
 units:'Toy cases: annual million USD. Horizon cases: cumulative billion constant 2026 USD, 2027-2056; policy on from 2030.',
 assumptions:{annualFactor,toyIncumbentMW:10000,toyNewMW:1000,toyNitsKWYear:95.1},
 interpretation:[
  'Additional payments must always name their counterfactual: embedded or higher-of.',
  'With an embedded baseline, additional payments can exceed total payments above incremental cost when the baseline fails to recover incremental costs.',
  'Pooling heterogeneous regions can overstate AND uplift versus region-specific higher-of tariffs.',
  'Financial examples cannot identify the cost, necessity, or attribution of actual transmission upgrades. Engineering models and empirical matching are separate tasks.'
 ],toyCases:cases,aggregation:{regionalSumAnnualMillion:regionSum,pooledAnnualMillion:pooled.annualMillion},horizonCases};
fs.writeFileSync(path.join(__dirname,'../data/dummy-models.json'),JSON.stringify(output,null,2)+'\n');
console.table(cases.map(x=>({case:x.name,...Object.fromEntries(Object.entries(x.annualMillion).map(([k,v])=>[k,+v.toFixed(2)]))})));
console.log('Higher-of aggregation:',JSON.stringify({regional:regionSum.additionalVsHigherOf,pooled:pooled.annualMillion.additionalVsHigherOf}));
console.table(horizonCases.filter(x=>x.growth==='medium'));
console.log('PASS: payment conservation, customer-bill transfer identities, zero-cost boundary, expensive-connection distinction, and pooling diagnostic.');
