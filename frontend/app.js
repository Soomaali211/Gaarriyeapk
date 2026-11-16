(() => {
  "use strict";
  const $ = (s, root=document) => root.querySelector(s);
  const $$ = (s, root=document) => [...root.querySelectorAll(s)];
  const sidebar=$("#sidebar"), overlay=$("#overlay"), toast=$("#toast");
  const poem=$("#poem"), count=$("#charCount"), liveLines=$("#liveLines"), gutter=$("#editorGutter");
  const MODE_KEY="gaarriye.analysisModes.v1", DRAFT_KEY="gaarriye.noteLive.draft.v1";
  const API_BASE=(document.querySelector('meta[name="gaarriye-api"]')?.content||"").replace(/\/+$/,"");
  const modeDefs=[
    {id:"modeGaarriye",state:"stateGaarriye",key:"gaarriye",apiKey:"gaarriye"},
    {id:"modeResearch",state:"stateResearch",key:"research",apiKey:"researchers"},
    {id:"modeCompatible",state:"stateCompatible",key:"compatible",apiKey:"compatible_other"}
  ];
  let toastTimer, renderTimer, saveTimer, activeLine=1, lastAnalysis=null, requestSequence=0;
  const say=m=>{toast.textContent=m;toast.style.display="block";clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.style.display="none",3000)};
  const selectedModes=()=>Object.fromEntries(modeDefs.map(x=>[x.key,$("#"+x.id).checked]));
  function loadModes(){
    try{const x=JSON.parse(localStorage.getItem(MODE_KEY)||"null");return {gaarriye:x?.gaarriye!==false,research:x?.research===true,compatible:x?.compatible===true}}
    catch(_){return {gaarriye:true,research:false,compatible:false}}
  }
  function paintModes(){
    modeDefs.forEach(x=>{$("#"+x.state).textContent=$("#"+x.id).checked?"ON":"OFF";$("#"+x.state).style.color=$("#"+x.id).checked?"var(--ok)":"var(--muted)"});
    const active=modeDefs.some(x=>$("#"+x.id).checked);
    $("#modeHelp").textContent=active?"Qaybaha ON ayaa loo diri doonaa habka falanqaynta.":"Dhammaan qaybaha waa OFF; daar ugu yaraan hal qayb.";
    $("#analyzeBtn").disabled=!active;
  }
  const savedModes=loadModes();
  modeDefs.forEach(x=>{
    $("#"+x.id).checked=savedModes[x.key];
    $("#"+x.id).addEventListener("change",()=>{
      try{localStorage.setItem(MODE_KEY,JSON.stringify(selectedModes()))}catch(_){say("Doorashada lama kaydin karin.")}
      paintModes();
      lastAnalysis=null;
      renderLive();
      if(poem.value.trim() && API_BASE) analyzePoem({quiet:true});
    });
  });
  paintModes();

  function closeMenu(){sidebar.classList.remove("open");overlay.classList.remove("show")}
  function showPage(name){
    $$(".page").forEach(p=>p.classList.toggle("active",p.id==="page-"+name));
    $$(".nav button").forEach(b=>b.classList.toggle("active",b.dataset.page===name));
    closeMenu();window.scrollTo({top:0,behavior:"smooth"});
  }
  $$(".nav button").forEach(b=>b.addEventListener("click",()=>showPage(b.dataset.page)));
  $("#menuBtn").addEventListener("click",()=>{sidebar.classList.add("open");overlay.classList.add("show")});
  overlay.addEventListener("click",closeMenu);
  $("#themeBtn").addEventListener("click",()=>{
    const root=document.documentElement;root.dataset.theme=root.dataset.theme==="dark"?"light":"dark";
    $("#themeBtn").textContent=root.dataset.theme==="dark"?"☀":"◐";
    try{localStorage.setItem("gaarriye.theme",root.dataset.theme)}catch(_){}
  });
  try{const t=localStorage.getItem("gaarriye.theme");if(t==="dark"||t==="light")document.documentElement.dataset.theme=t}catch(_){}

  function currentLineNumber(){return poem.value.slice(0,poem.selectionStart).split("\n").length;}
  function updateEditorPosition(){
    activeLine=currentLineNumber();
    const lines=poem.value.split("\n");
    gutter.textContent=lines.map((_,i)=>String(i+1)).join("\n");
    gutter.scrollTop=poem.scrollTop;
    $("#selectedLine").textContent=`Sadar hadda: ${activeLine} — ${lines[activeLine-1]?.trim()?"meesha qoraalku yaallo":"diyaar u ah qorista"}`;
    $$(".live-line").forEach(el=>el.classList.toggle("selected",Number(el.dataset.line)===activeLine));
  }
  function renderLive(){
    const lines=poem.value.replace(/\r\n?/g,"\n").split("\n");
    const nonempty=lines.filter(x=>x.trim()).length;
    $("#liveCount").textContent=nonempty+" sadar";
    liveLines.replaceChildren();
    if(!poem.value.trim()){
      const empty=document.createElement("div");empty.className="live-empty";
      empty.textContent="Marka aad wax qorto, sadarradu halkan ayay ka soo muuqanayaan.";
      liveLines.append(empty);updateEditorPosition();return;
    }
    lines.forEach((line,i)=>{
      if(!line.trim())return;
      const row=document.createElement("button");row.type="button";row.className="live-line";row.dataset.line=String(i+1);row.setAttribute("aria-label",`U gudub sadar ${i+1}`);
      const num=node("span","live-number",String(i+1));
      const content=node("span","");
      const txt=node("span","live-text",line);
      const resultLine=lastAnalysis?.lines?.find(x=>x.line_number===i+1);
      const statusText=resultLine
        ? `${resultLine.status}: ${resultLine.explanation_code||"Xaalad la helay"}`
        : "Sadar waa la qabtay; sug falanqaynta API-ga.";
      const status=node("span","live-status",statusText);
      content.append(txt,status);row.append(num,content);
      row.addEventListener("click",()=>{
        const start=lines.slice(0,i).reduce((n,x)=>n+x.length+1,0);
        poem.focus();poem.setSelectionRange(start,start+line.length);updateEditorPosition();
      });
      liveLines.append(row);
    });
    updateEditorPosition();
  }
  function persistDraft(){
    try{localStorage.setItem(DRAFT_KEY,JSON.stringify({text:poem.value,title:"",updatedAt:new Date().toISOString()}));}
    catch(_){say("Kaydinta qoraalka way fashilantay; hubi booska qalabka.")}
  }
  function onTextInput(){
    requestSequence++;
    lastAnalysis=null;
    const analyzeButton=$("#analyzeBtn");
    analyzeButton.disabled=!Object.values(selectedModes()).some(Boolean);
    analyzeButton.textContent="Falanqee maansada →";
    count.textContent=poem.value.length.toLocaleString("so")+" xaraf";
    updateEditorPosition();
    clearTimeout(renderTimer);renderTimer=setTimeout(renderLive,120);
    clearTimeout(saveTimer);saveTimer=setTimeout(persistDraft,450);
  }
  poem.addEventListener("input",onTextInput);
  ["click","keyup","select"].forEach(evt=>poem.addEventListener(evt,updateEditorPosition));
  poem.addEventListener("scroll",()=>{gutter.scrollTop=poem.scrollTop});
  try{const draft=JSON.parse(localStorage.getItem(DRAFT_KEY)||"null");if(draft&&typeof draft.text==="string")poem.value=draft.text}catch(_){}
  onTextInput();

  function node(tag,cls,text){const el=document.createElement(tag);if(cls)el.className=cls;if(text!==undefined)el.textContent=text;return el}
  function showResult(title,message,status,detail){
    const box=$("#resultBox");box.replaceChildren(node("div","result-icon","⌁"),node("h3","",title),node("p","",message));
    const row=node("div","status-row");row.append(node("span","pill",status));if(detail)row.append(node("span","pill",detail));box.append(row);
  }
  async function checkApi(){
    const badge=$("#apiStatus");
    if(!API_BASE){badge.textContent="API: lama dejin";return}
    try{const r=await fetch(API_BASE+"/health");if(!r.ok)throw Error();const d=await r.json();badge.textContent=d.status==="ok"?"API: ku xidhan":"API: jawaab aan la filayn";badge.className="pill "+(d.status==="ok"?"green":"")}
    catch(_){badge.textContent="API: lama heli karo"}
  }
  $("#saveBtn").addEventListener("click",()=>{
    persistDraft();
    try{localStorage.setItem("gaarriye.noteLive.lastSavedAt",new Date().toISOString());say("Maansada waxaa lagu kaydiyey qalabkan.");}
    catch(_){say("Kaydinta way fashilantay; booska qalabka hubi.");}
  });
  $("#downloadBtn").addEventListener("click",()=>{
    if(!poem.value.trim()){say("Ma jiro qoraal la soo dejinayo.");return;}
    const blob=new Blob([poem.value],{type:"text/plain;charset=utf-8"});
    const url=URL.createObjectURL(blob);const a=document.createElement("a");
    a.href=url;a.download="maansadayda.txt";document.body.append(a);a.click();a.remove();URL.revokeObjectURL(url);
    say("Faylka qoraalka waa la diyaariyey.");
  });
  $("#clearBtn").addEventListener("click",()=>{
    if(!poem.value.trim())return;
    if(!confirm("Ma hubtaa inaad tirtirayso qoraalka Note Live?"))return;
    poem.value="";onTextInput();persistDraft();showResult("Qoraalka waa la nadiifiyey","Ku qor maanso cusub si Note Live uu ula socdo.","Qoraal madhan");poem.focus();
  });
  async function analyzePoem({quiet=false}={}){
    const text=poem.value.trim(), modes=selectedModes();
    if(!text){if(!quiet)say("Fadlan marka hore geli maanso.");poem.focus();return}
    if(!Object.values(modes).some(Boolean)){if(!quiet)say("Daar ugu yaraan hal hab oo falanqayn ah.");return}
    if(!API_BASE){
      lastAnalysis=null;renderLive();
      if(!quiet)showResult("Engine-ka falanqaynta lama xidhin","Qoraalka waa la kaydiyey qalabka. API lama dejin, sidaas darteed miisaan rasmi ah lama samayn.","Engine: not connected");
      return;
    }
    const btn=$("#analyzeBtn"),genre=$("#genreSelect").value,seq=++requestSequence;
    const analysisModes={gaarriye:modes.gaarriye,researchers:modes.research,compatible_other:modes.compatible};
    btn.disabled=true;btn.textContent="Waa la hubinayaa…";
    if(!quiet)showResult("Codsiga waa socda","Waxaa API-ga loo dirayaa qoraalka iyo saddexda doorasho ee kala madax-bannaan.","Sugaya API");
    try{
      const r=await fetch(API_BASE+"/api/v1/analyze",{
        method:"POST",
        headers:{"Content-Type":"application/json","Accept":"application/json"},
        body:JSON.stringify({text,genre:genre==="auto"?null:genre,analysis_modes:analysisModes})
      });
      const d=await r.json().catch(()=>({}));
      if(seq!==requestSequence)return;
      if(!r.ok){
        lastAnalysis=null;renderLive();
        showResult("Codsiga wuu fashilmay",d.message||d.detail||"Backend-ku ma aqbalin codsiga.","HTTP "+r.status,d.code||"");
        return;
      }
      lastAnalysis=d;
      renderLive();
      const enabled=(d.enabled_rule_classes||[]).join(" · ")||"Ma jiro fasal la doortay";
      if(d.status==="UNVERIFIED"||d.code==="ENGINE_NOT_READY"){
        showResult("Xeerar la fulin karo weli lama xaqiijin",d.message||"Qoraalka lama miisaamin; xaaladda sadar kasta hoos ayaa lagu muujiyey.","UNVERIFIED",enabled);
      }else{
        showResult("Jawaabta falanqaynta",d.message||"Jawaabta API-ga waa la helay.",d.status||"UNKNOWN",enabled);
      }
    }catch(_){
      if(seq!==requestSequence)return;
      lastAnalysis=null;renderLive();
      showResult("Backend-ka lama gaadhi karo","Qoraalkaagu wuxuu ku sii jiraa qalabka. Hubi API-ga si aad u dirto falanqayn.","API: disconnected");
    }finally{
      if(seq===requestSequence){btn.disabled=!Object.values(selectedModes()).some(Boolean);btn.textContent="Falanqee maansada →"}
    }
  }
  $("#analyzeBtn").addEventListener("click",()=>analyzePoem());
  checkApi();
})();