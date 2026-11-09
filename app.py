"""스마트 소비 분석이 — Streamlit Community Cloud 배포용 단일 파일.

1. GitHub 저장소 루트에 app.py, requirements.txt를 올립니다.
2. Streamlit Community Cloud에서 저장소와 main file: app.py를 선택합니다.
3. 배포된 공개 https 주소로 QR코드를 생성하면 스마트폰에서 바로 접속합니다.
로컬 실행: pip install -r requirements.txt && streamlit run app.py

월 전체 예산과 같은 달의 누적 지출을 비교합니다. 금융 진단이 아닌
단순 예산 관리 참고 도구입니다. 서버/DB로 소비 내역을 전송하지 않습니다.
저장은 브라우저 localStorage를 사용하며 브라우저 정책에 따라 제한될 수 있습니다.
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="스마트 소비 분석이", page_icon="💳", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""<style>
[data-testid="stHeader"], [data-testid="stToolbar"], footer {display:none!important}
[data-testid="stAppViewContainer"] {background:#eef3f8}
.block-container {padding:0!important;max-width:500px!important}
[data-testid="stMainBlockContainer"] {padding:0!important}
iframe {width:100%;height:calc(100svh - 4px)!important;border:0;display:block}
[data-testid="stVerticalBlock"] {gap:0!important}
</style>""", unsafe_allow_html=True)

PAGE = r'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#eef3f8;color:#17283c;font-family:system-ui,-apple-system,'Apple SD Gothic Neo','Nanum Gothic',sans-serif}
body{padding:10px 12px}main{max-width:460px;height:100%;margin:auto;display:flex;flex-direction:column;gap:9px}
header{display:flex;align-items:center;justify-content:space-between;flex-shrink:0}h1{font-size:21px;letter-spacing:-1px;margin:0}header p{font-size:11px;color:#52657c;margin:3px 0 0}.logo{background:#17283c;color:white;border-radius:12px;padding:10px;font-size:20px}
.card{background:white;border:1px solid #e0e7ef;border-radius:17px;padding:12px;flex-shrink:0}.eyebrow{font-size:11px;color:#52657c;margin-bottom:4px}.money{display:flex;align-items:center;gap:8px}.money input{flex:1;min-width:0;font-size:24px;font-weight:750;border:0;background:#f2f6fa;border-radius:9px;padding:7px 10px;color:#17283c}.money span{font-size:13px}
.labelrow{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.labelrow strong{font-size:13px}.labelrow span{font-size:10px;color:#52657c}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}label{font-size:11px;color:#41556e;display:block}label input{width:100%;display:block;border:1px solid #d5dfea;border-radius:8px;padding:8px 6px;font-size:14px;color:#17283c;margin-top:4px;background:#fafcfe;min-width:0}input:focus{outline:2px solid #047857;outline-offset:1px}input::-webkit-inner-spin-button{opacity:0}
.summary{display:grid;grid-template-columns:1fr 1fr;gap:8px}.stat{padding:11px;border-radius:12px;background:#f1f6fa;min-width:0}.stat small{font-size:11px;color:#52657c}.stat b{display:block;font-size:19px;letter-spacing:-.7px;margin-top:4px;overflow-wrap:anywhere}.stat.primary{background:#e6f6ef}.stat.primary b{color:#046c4e}
.status{display:flex;justify-content:space-between;align-items:center;margin-top:10px;gap:8px;font-size:12px}.badge{padding:4px 8px;border-radius:20px;background:#e6f6ef;color:#046c4e;font-size:11px;font-weight:700}.tip{font-size:12px;line-height:1.55;margin:8px 0 0;color:#334b65;min-height:38px}.actions{display:flex;gap:8px}button{border:1px solid #cdd9e5;background:#fff;color:#334b65;font:inherit;font-size:12px;font-weight:650;padding:9px;border-radius:10px;cursor:pointer;flex:1}button:first-child{background:#17283c;color:#fff;border-color:#17283c}footer{font-size:10px;color:#52657c;line-height:1.5;text-align:center;margin-top:auto;padding-bottom:3px}#notice{font-size:10px;color:#52657c;text-align:center;min-height:14px}.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}
@media(max-height:650px){body{padding:6px 10px}main{gap:6px}.card{padding:9px}h1{font-size:19px}label input{padding:6px}.stat{padding:8px}.tip{margin-top:5px;min-height:34px}footer{font-size:9px}.logo{padding:7px}.money input{font-size:21px}button{padding:7px}}
@media(max-height:530px){main{gap:4px}.card{padding:7px}.grid{gap:5px}header p{display:none}.stat b{font-size:16px}.tip{font-size:11px;min-height:0}.status{margin-top:5px}footer{margin-top:0}body{overflow:auto}}
</style></head><body><main>
<header><div><h1>스마트 소비 분석이</h1><p>이번 달 소비, 한눈에 가볍게 확인해요.</p></div><div class="logo" aria-hidden="true">💳</div></header>
<section class="card"><div class="eyebrow"><label for="budget">이번 달 전체 예산</label></div><div class="money"><input id="budget" type="number" inputmode="numeric" min="0" max="999999999" step="1000" placeholder="예: 500000" aria-label="이번 달 전체 예산 원"><span>원</span></div></section>
<section class="card"><div class="labelrow"><strong>항목별 누적 지출</strong><span>이번 달 · 단위 원</span></div><div class="grid">
<label>🍚 식비<input id="food" type="number" inputmode="numeric" min="0" max="999999999" placeholder="0" aria-label="식비 원"></label>
<label>🚌 교통<input id="travel" type="number" inputmode="numeric" min="0" max="999999999" placeholder="0" aria-label="교통비 원"></label>
<label>🛍 쇼핑<input id="shop" type="number" inputmode="numeric" min="0" max="999999999" placeholder="0" aria-label="쇼핑비 원"></label>
<label>☕ 카페<input id="cafe" type="number" inputmode="numeric" min="0" max="999999999" placeholder="0" aria-label="카페 지출 원"></label>
<label>🎮 여가<input id="fun" type="number" inputmode="numeric" min="0" max="999999999" placeholder="0" aria-label="여가비 원"></label>
<label>📦 기타<input id="other" type="number" inputmode="numeric" min="0" max="999999999" placeholder="0" aria-label="기타 지출 원"></label>
</div></section>
<section class="card" aria-live="polite" aria-atomic="true"><div class="summary"><div class="stat"><small>총 지출</small><b id="spent">0원</b></div><div class="stat primary"><small id="remainLabel">남은 예산</small><b id="remaining">—</b></div></div><div class="status"><span id="ratio">예산을 입력해 주세요</span><span id="badge" class="badge">입력 대기</span></div><p class="tip" id="tip">예산과 지출을 입력하면 즉시 분석해 드려요.</p></section>
<div class="actions"><button id="example" type="button">예시로 체험</button><button id="reset" type="button">초기화</button></div>
<div id="notice" role="status">입력 즉시 분석 · 이 기기의 브라우저에만 저장</div>
<footer>같은 달의 예산·지출을 비교해요. 잔여 금액은 저축액이 아니에요.<br>개인정보 입력 없이 사용 · 예산 관리 참고용</footer>
</main><script>
'use strict';
const ids=['budget','food','travel','shop','cafe','fun','other'];
const names=['식비','교통','쇼핑','카페','여가','기타'];
const key='smart-spending-v1';
const el=id=>document.getElementById(id);
const won=v=>Math.round(v).toLocaleString('ko-KR')+'원';
function analyze(budget, values){
 const total=values.reduce((a,b)=>a+b,0), remaining=budget-total;
 const max=Math.max(...values), index=values.indexOf(max);
 const pct=budget>0?total/budget*100:null;
 return {total,remaining,max,index,pct};
}
function render(save=true){
 const vals=ids.map(id=>{const node=el(id);let v=Number(node.value);if(!Number.isFinite(v)||v<0)v=0;v=Math.min(999999999,Math.floor(v));if(node.value!==''&&Number(node.value)!==v)node.value=v;return v;});
 const [budget,...values]=vals, a=analyze(budget,values);
 el('spent').textContent=won(a.total);
 el('remaining').textContent=budget>0?won(Math.abs(a.remaining)):'—';
 el('remainLabel').textContent=budget>0&&a.remaining<0?'예산 초과':'남은 예산';
 el('remaining').style.color=a.remaining<0?'#b42318':'#046c4e';
 let status='입력 대기', color='#046c4e', bg='#e6f6ef';
 if(budget>0){status=a.pct>100?'예산 초과':a.pct>=80?'주의 구간':'예산 이내';if(a.pct>=80){color=a.pct>100?'#b42318':'#8a5100';bg=a.pct>100?'#fff0ed':'#fff5de';}}
 el('badge').textContent=status;el('badge').style.color=color;el('badge').style.background=bg;
 el('ratio').textContent=budget>0?'예산 사용률 '+a.pct.toLocaleString('ko-KR',{maximumFractionDigits:1})+'%':'예산을 입력해 주세요';
 let text='예산과 지출을 입력하면 즉시 분석해 드려요.';
 if(a.total>0){const top=names.filter((_,i)=>values[i]===a.max).join('·');text='최대 지출: '+top+' ('+won(a.max)+'). ';text+=budget>0&&a.remaining<0?'예산을 '+won(-a.remaining)+' 초과했어요. 추가 지출을 점검해요.':'이 항목을 10% 줄이면 '+won(a.max*.1)+'을 아낄 수 있어요.';}
 else if(budget>0)text='아직 기록된 지출이 없어요. 이번 달 누적 금액을 입력해 보세요.';
 el('tip').textContent=text;
 if(save){try{localStorage.setItem(key,JSON.stringify(Object.fromEntries(ids.map((id,i)=>[id,el(id).value]))));}catch(e){el('notice').textContent='이 브라우저에서는 저장할 수 없어요 · 현재 화면에서만 유지';}}
}
ids.forEach(id=>el(id).addEventListener('input',()=>render()));
el('example').addEventListener('click',()=>{[500000,180000,50000,80000,45000,40000,25000].forEach((v,i)=>el(ids[i]).value=v);render();});
let resetPending=false, timer;
el('reset').addEventListener('click',()=>{if(!resetPending){resetPending=true;el('reset').textContent='한 번 더 누르면 삭제';timer=setTimeout(()=>{resetPending=false;el('reset').textContent='초기화';},3500);return;}clearTimeout(timer);resetPending=false;el('reset').textContent='초기화';ids.forEach(id=>el(id).value='');try{localStorage.removeItem(key);}catch(e){}render(false);});
try{const saved=JSON.parse(localStorage.getItem(key)||'null');if(saved&&typeof saved==='object')ids.forEach(id=>{if(typeof saved[id]==='string'||typeof saved[id]==='number')el(id).value=saved[id];});}catch(e){el('notice').textContent='저장된 입력을 불러올 수 없어요 · 새로 입력해 주세요';}
render(false);
</script></body></html>'''
components.html(PAGE, height=700, scrolling=False)
