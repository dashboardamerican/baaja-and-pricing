/* BAAJA section 2107(a) screening ledger. Constant 2026 USD, 2027-2056.
   The same grid is built in both tariff cases. No existing AND overlap haircut. */
(function(root){
'use strict';
const FIXED = Object.freeze({first:2027,last:2056,chargeStart:2030,loadFactor:0.80,
  coveredShare:0.75,incumbentMW:829000,life:40,finance:0.05,om:0.015,inflation:0.025});
const CENTRAL = Object.freeze({growth:2,cost:0.65,nits:95.1});
const JCT = Object.freeze([[2022,0],[2023,0],[2024,0],[2025,0.788],[2026,1.213],
  [2027,1.213],[2028,1.213],[2029,2.001],[2030,2.426],[2031,2.425]]);
function demand(year,growth){
  return year<=2030 ? 300*Math.pow(2,(year-2026)/4) : 600*Math.pow(1+growth/100,year-2030);
}
function itc(){
  const profile=JCT.map(([year,value])=>value/Math.pow(1+FIXED.inflation,year-2026));
  return {officialTenYear:JCT.reduce((s,r)=>s+r[1],0),realTenYear:profile.reduce((s,x)=>s+x,0),
    realThirtyYear:3*profile.reduce((s,x)=>s+x,0),profile,
    annual:Array.from({length:30},(_,i)=>({year:2027+i,billion:profile[i%10]}))};
}
function calculate(input={}){
  const p={...CENTRAL,...input};
  if(![p.growth,p.cost,p.nits].every(Number.isFinite)||p.growth<0||p.cost<0||p.nits<0)
    throw new RangeError('Growth, capital cost, and NITS must be finite and nonnegative.');
  const f=FIXED, rate=p.nits*1000, capital=p.cost*1e6;
  const crf=f.finance/(1-Math.pow(1+f.finance,-f.life));
  const unit=capital*(crf+f.om),base=f.incumbentMW*rate;
  let mw=0,A=0,B=0,incremental=0,before=0,andTotal=0,firstTenA=0,firstTenB=0;
  const rows=[];
  for(let year=f.first;year<=f.last;year++){
    const added=Math.max(0,demand(year,p.growth)-demand(year-1,p.growth))/8.76/f.loadFactor*1000*f.coveredShare;
    mw+=added;
    // Every cohort's 40-year asset life exceeds its age inside this 30-year window.
    const I=mw*unit,s=mw/(f.incumbentMW+mw);
    const ordinary=s*(base+I),higher=Math.max(ordinary,I),and=s*base+I;
    const on=year>=f.chargeStart;
    const a=on?and-higher:0,b=on?s*base:0;
    A+=a;B+=b;
    if(on){incremental+=I;before+=higher;andTotal+=and;}
    if(year<=2036){firstTenA+=a*Math.pow(1+f.inflation,year-2026);firstTenB+=b*Math.pow(1+f.inflation,year-2026);}
    rows.push({year,twh:demand(year,p.growth),coveredMW:mw,addedMW:added,share:s,policyOn:on,
      inheritedRequirement:base,incrementalCost:I,ordinaryPayment:ordinary,higherOfPayment:higher,
      ANDPayment:on?and:higher,existingPaymentBefore:base+I-higher,
      existingPaymentAND:base+I-(on?and:higher),A:a,B:b,cumulativeA:A,cumulativeB:B});
  }
  return {params:p,A:A/1e9,B:B/1e9,incremental:incremental/1e9,before:before/1e9,
    andTotal:andTotal/1e9,firstTenNominalA:firstTenA/1e9,firstTenNominalB:firstTenB/1e9,
    endTWh:demand(f.last,p.growth),endCoveredGW:mw/1000,annualCostPerMW:unit,rows,itc:itc()};
}
const api={FIXED,CENTRAL,JCT,demand,itc,calculate};
root.Baaja=api;
if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
