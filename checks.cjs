'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const m=require('./model.js');
const close=(a,b,msg)=>assert(Math.abs(a-b)<=1e-7*Math.max(1,Math.abs(b)),`${msg}: ${a} vs ${b}`);
const cases=JSON.parse(fs.readFileSync(path.join(__dirname,'data/golden.json'),'utf8'));
let count=0;
for(const test of cases){
 const r=m.calculate(test.input),ref=test.reference;
 close(r.A,ref.metrics.A_extra_AND_vs_higher_of_usd.constant_2026_billion,test.name+' A');
 close(r.B,ref.metrics.B_above_incremental_transmission_cost_usd.constant_2026_billion,test.name+' B');
 close(r.endTWh,ref.endpoint_2056_twh,test.name+' demand');
 for(let i=0;i<r.rows.length;i++){
  const a=r.rows[i],b=ref.annual[i];
  assert.equal(a.year,b.year);
  close(a.A,b.A_extra_AND_vs_higher_of_usd,test.name+' annual A');
  close(a.B,b.B_above_incremental_transmission_cost_usd,test.name+' annual B');
  close(a.coveredMW/1000,b.effective_new_billing_gw,test.name+' eligible MW');
  close(a.A,a.existingPaymentBefore-a.existingPaymentAND,test.name+' bill transfer');
  close(a.ANDPayment+a.existingPaymentAND,a.inheritedRequirement+a.incrementalCost,test.name+' conserved revenue');
  assert(a.A>=-1e-4&&a.A<=a.B+1e-4,'Additional relief is part of inherited contribution');
  count++;
 }
}
const c=m.calculate(),z=m.calculate({cost:0}),n=m.calculate({nits:0});
close(z.A,0,'No incremental capital means no added payment');assert(z.B>0,'Ordinary inherited contribution can remain without policy uplift');
close(n.A,0,'No NITS means no extra above incremental-only');close(n.B,0,'No NITS means no inherited contribution');
assert(m.calculate({growth:6}).A>c.A,'More realized demand increases receipts');
close(m.calculate({cost:0.3}).B,c.B,'Inherited contribution is independent of upgrade capital');
close(m.itc().officialTenYear,11.279,'JCT main row includes direct-pay outlays');
close(m.itc().realThirtyYear,31.673927489147527,'Annual-flow normalized repeated ITC');
assert.equal(m.FIXED.loadFactor,.8);assert.equal(m.FIXED.incumbentMW,829000);
const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
assert.equal((html.match(/type="range"/g)||[]).length,3,'Exactly three sliders');
assert(!/https?:\/\/[^"']+\.js/.test(html),'No external runtime scripts');
for(const file of ['baaja-one-pager.pdf','data/central-case.json','data/national-rate.json','data/pudl-review.json'])assert(fs.existsSync(path.join(__dirname,file)),'Artifact exists: '+file);
console.log(`PASS: ${cases.length} independent Python cases, ${count} annual rows, payment conservation, A/B boundaries, ITC normalization, and three-control HTML.`);
