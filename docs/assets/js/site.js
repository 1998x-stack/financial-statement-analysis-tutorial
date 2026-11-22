(()=>{'use strict';const input=document.getElementById('chapter-search');if(input){const cards=[...document.querySelectorAll('.chapter-card')];const status=document.getElementById('search-status');input.addEventListener('input',()=>{const q=input.value.trim().toLocaleLowerCase();let n=0;cards.forEach(c=>{const match=(c.textContent+' '+c.dataset.keywords).toLocaleLowerCase().includes(q);c.hidden=!match;if(match)n++});document.querySelectorAll('.module').forEach(m=>{m.hidden=![...m.querySelectorAll('.chapter-card')].some(c=>!c.hidden)});status.textContent=q?'找到 '+n+' 篇匹配章节':''})}document.querySelectorAll('[data-calculator]').forEach(box=>{const type=box.dataset.calculator;const inputs=[...box.querySelectorAll('input[type=number]')];const out=box.querySelector('[data-result]');if(!out)return;const f=()=>{const v=Object.fromEntries(inputs.map(x=>[x.name,Number(x.value)]));let html='';const N=n=>Number.isFinite(n)?Number(n.toFixed(2)).toLocaleString('zh-CN'):'—';if(type==='balance'){const equity=v.assets-v.liabilities;html='资产 '+N(v.assets)+' − 负债 '+N(v.liabilities)+' = <strong>权益 '+N(equity)+'</strong>；资产负债率 '+(v.assets>0?N(v.liabilities/v.assets*100)+'%':'无法计算')}else if(type==='margin'){const gp=v.sales-v.cost,oper=gp-v.expense;html='毛利 '+N(gp)+' ｜毛利率 <strong>'+(v.sales>0?N(gp/v.sales*100)+'%':'无法计算')+'</strong> ｜简化经营利润 '+N(oper)}else if(type==='cash'){const cfo=v.profit+v.nonCash-v.workingCapital,fcf=cfo-v.capex;html='经营现金流 <strong>'+N(cfo)+'</strong>；示意自由现金流（CFO−CapEx） '+N(fcf)}else if(type==='notes'){const accessible=v.cash-v.restricted,coverage=v.debt>0?N(accessible/v.debt)+' 倍':'无短债分母';html='可动用现金 <strong>'+N(accessible)+'</strong>；短债现金覆盖 '+coverage} else if(type==='link'){html=v.collected>=v.revenue?'现金收款不低于本次确认收入（仍需核对期初应收及预收）':'本次收入 '+N(v.revenue)+'，本次收款 '+N(v.collected)+'，差额 '+N(v.revenue-v.collected)+' 需要查看应收或合同资产等科目'}out.innerHTML=html};inputs.forEach(x=>x.addEventListener('input',f));f()})})();
/* Chapter 06–10 analysis workbenches. No dependencies, no external data. */
(()=>{'use strict';
const f=n=>Number.isFinite(n)?Number(n.toFixed(2)).toLocaleString('zh-CN',{maximumFractionDigits:2}):'不适用';
const pct=n=>Number.isFinite(n)?f(n*100)+'%':'不适用';
const div=(x,y)=>y===0?NaN:x/y;
const choices={
 policy:v=>{if(v.bookValue<0||v.residual<0||v.bookValue<v.residual||v.oldLife<=0||v.newLife<=0)return '检查输入：净值≥残值≥0，且剩余年限必须大于0。';let old=(v.bookValue-v.residual)/v.oldLife,next=(v.bookValue-v.residual)/v.newLife;return '旧预计年折旧 '+f(old)+' 万；新预计年折旧 '+f(next)+' 万；未来完整年度税前利润示意变化 '+(old-next>=0?'+':'')+f(old-next)+' 万（不含税、减值及其他差异）。';},
 evidence:v=>{if(v.prevRevenue<=0||v.prevAr<=0)return '上期收入和上期末应收须大于0，才能计算增长率。';let rev=(v.revenue-v.prevRevenue)/v.prevRevenue,ar=(v.ar-v.prevAr)/v.prevAr;return '收入同比 '+pct(rev)+'；期末应收同比 '+pct(ar)+'；增速差 '+f((ar-rev)*100)+' 个百分点；CFO / 当期净利润 '+(v.net>0?pct(v.cfo/v.net):'利润非正，需另行解释')+'。异常不等于舞弊。';},
 profit:v=>{if(v.revenue<=0||v.assets<=0||v.equity<=0||v.cogs<0)return '检查输入：收入、平均资产、平均权益须大于0，成本不能为负。';let margin=v.net/v.revenue,turn=v.revenue/v.assets,mult=v.assets/v.equity,roe=v.net/v.equity;return '毛利 '+f(v.revenue-v.cogs)+' 万（'+pct(1-v.cogs/v.revenue)+'）；净利率 '+pct(margin)+'；ROA '+pct(v.net/v.assets)+'；资产周转 '+f(turn)+' 倍 × 权益乘数 '+f(mult)+' 倍 → ROE '+pct(roe)+'。';},
 solvency:v=>{if(v.ca<0||v.inv<0||v.prepaid<0||v.cl<=0||v.cash<0||v.restricted<0||v.restricted>v.cash||v.cash>v.ca||v.inv+v.prepaid>v.ca||v.interest<0)return '检查输入：流动负债>0，受限现金≤账面现金≤流动资产，扣除项目不超过流动资产，利息费用≥0。';let quick=v.ca-v.inv-v.prepaid;return '流动比率 '+f(v.ca/v.cl)+' 倍；速动比率 '+f(quick/v.cl)+' 倍；不受限现金 '+f(v.cash-v.restricted)+' 万，对流动负债覆盖 '+f((v.cash-v.restricted)/v.cl)+' 倍；EBIT/利息 '+(v.interest>0?f(v.ebit/v.interest)+' 倍':'分母为0，不适用')+'。';},
 cycle:v=>{if(v.sales<=0||v.cogs<=0||v.days<=0||v.ar<0||v.inv<0||v.ap<0)return '检查输入：期间收入、成本和天数>0；平均应收、存货、应付不能为负。';let dso=v.ar/v.sales*v.days,dio=v.inv/v.cogs*v.days,dpo=v.ap/v.cogs*v.days;return 'DSO '+f(dso)+' 天；DIO '+f(dio)+' 天；DPO（以成本近似采购） '+f(dpo)+' 天；CCC = '+f(dio+dso-dpo)+' 天。';}
};
document.querySelectorAll('[data-calculator]').forEach(box=>{
 const kind=box.getAttribute('data-calculator');if(!choices[kind])return;
 const controls=[...box.querySelectorAll('input[type=number]')],out=box.querySelector('[data-result]');if(!out)return;
 const update=()=>{if(controls.some(c=>c.value===''||!Number.isFinite(Number(c.value)))){out.textContent='请输入全部有效数值。';return;}
 const data=Object.fromEntries(controls.map(c=>[c.name,Number(c.value)]));out.textContent=choices[kind](data);};
 controls.forEach(c=>c.addEventListener('input',update));update();
});
})();
/* Chapter 11–15 workbenches: transparent ratios, no external data or risk scores. */
(()=>{'use strict';
const n=x=>Number.isFinite(x)?Number(x.toFixed(2)).toLocaleString('zh-CN',{maximumFractionDigits:2}):'不适用';
const p=x=>Number.isFinite(x)?n(x*100)+'%':'不适用';
const signed=x=>(x>0?'+':'')+n(x);
const models={
 growth:v=>{
  if(v.priorRevenue<=0||v.currentRevenue<0||v.acquiredRevenue<0||v.acquiredRevenue>v.currentRevenue||v.roe<0||v.roe>=100||v.retention<0||v.retention>100)return '检查输入：上期收入>0，并购贡献≤本期收入，ROE须在0至100%之间，留存率须在0至100%之间。';
  const reported=(v.currentRevenue-v.priorRevenue)/v.priorRevenue,organic=(v.currentRevenue-v.acquiredRevenue-v.priorRevenue)/v.priorRevenue,rb=(v.roe/100)*(v.retention/100),sgr=rb<1?rb/(1-rb):NaN;
  return '报告收入增长 '+p(reported)+'；简化同口径有机增长 '+p(organic)+'；并购贡献 '+p(v.acquiredRevenue/v.priorRevenue)+'（占上期收入百分点）；ROE×留存率 '+p(rb)+'；模型 SGR '+p(sgr)+'。SGR依赖稳定杠杆与经营政策假设。';
 },
 cashflow:v=>{
  if(Object.values(v).some(x=>!Number.isFinite(x))||v.capex<0)return '检查输入：所有数值须有效，资本开支不能为负。';
  const cfo=v.netIncome+v.depreciation+v.impairment-v.gain-v.deltaAR-v.deltaInventory+v.deltaAP+v.other,fcf=cfo-v.capex;
  return '经营现金流 CFO '+n(cfo)+' 万；CFO/净利润 '+(v.netIncome!==0?p(cfo/v.netIncome):'净利润为0，不适用')+'；简化 FCF '+n(fcf)+' 万；FCF/净利润 '+(v.netIncome!==0?p(fcf/v.netIncome):'净利润为0，不适用')+'。';
 },
 dupont:v=>{
  if(v.pretax<=0||v.ebit<=0||v.revenue<=0||v.assets<=0||v.equity<=0||v.netIncome<0)return '检查输入：税前利润、EBIT、收入、平均资产和平均权益须大于0；本演示要求净利润非负。';
  const tax=v.netIncome/v.pretax,interest=v.pretax/v.ebit,margin=v.ebit/v.revenue,turn=v.revenue/v.assets,lev=v.assets/v.equity,roe=v.netIncome/v.equity;
  return '税负因子 '+p(tax)+'；利息负担 '+p(interest)+'；EBIT利润率 '+p(margin)+'；资产周转 '+n(turn)+' 次；权益乘数 '+n(lev)+' 倍；五因素 ROE '+p(tax*interest*margin*turn*lev)+'（直接计算 '+p(roe)+'）。';
 },
 peers:v=>{
  const a=[v.peer1,v.peer2,v.peer3,v.peer4].sort((x,y)=>x-y);if([v.target,...a].some(x=>!Number.isFinite(x)))return '请填写所有有效数值。';
  const median=(a[1]+a[2])/2,mean=a.reduce((s,x)=>s+x,0)/a.length,rank=a.filter(x=>x<=v.target).length/a.length;
  return '同行中位数 '+n(median)+'%；同行均值 '+n(mean)+'%；目标值 '+n(v.target)+'%；目标在同行样本中的“越高越好”百分位 '+p(rank)+'。该样本仅4家，分位数只作描述。';
 },
 'fraud-screen':v=>{
  if(v.q4Share<0||v.q4Share>100)return '检查输入：第四季度收入占比须在0至100之间。';
  const gap=v.arGrowth-v.revenueGrowth,ratio=v.netIncome!==0?p(v.cfo/v.netIncome):'净利润为0，不适用';
  return '应收增速−收入增速 '+signed(gap)+' 个百分点；第四季度收入占比 '+n(v.q4Share)+'%；CFO/净利润 '+ratio+'。只展示差异，不生成舞弊概率或风险评级。';
 }
};
document.querySelectorAll('[data-calculator]').forEach(box=>{
 const type=box.getAttribute('data-calculator');if(!models[type])return;
 const controls=[...box.querySelectorAll('input[type=number]')],out=box.querySelector('[data-result]');if(!out)return;
 const update=()=>{if(controls.some(c=>c.value===''||!Number.isFinite(Number(c.value)))){out.textContent='请输入全部有效数值。';return;}
 const v=Object.fromEntries(controls.map(c=>[c.name,Number(c.value)]));out.textContent=models[type](v);};
 controls.forEach(c=>c.addEventListener('input',update));update();
});
})();