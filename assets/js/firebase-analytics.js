// GA4 via Firebase Analytics. Staging visits are intentionally excluded.
// Tracking starts only after a visitor explicitly accepts optional analytics cookies.
import {firebaseConfig,firebaseConfigured} from "./firebase-config.js";
const stagingHosts=new Set(["coral-oyster-225966.hostingersite.com","localhost","127.0.0.1"]);
if(firebaseConfigured && firebaseConfig.measurementId && !stagingHosts.has(location.hostname)){
 const key="nazrul_analytics_consent_v1";
 const getChoice=()=>{try{return localStorage.getItem(key)}catch{return null}};
 const saveChoice=choice=>{try{localStorage.setItem(key,choice)}catch{}};
 async function enableAnalytics(){
   try{
    const [{initializeApp,getApps,getApp},{getAnalytics,isSupported}]=await Promise.all([
       import("https://www.gstatic.com/firebasejs/13.2.0/firebase-app.js"),
       import("https://www.gstatic.com/firebasejs/13.2.0/firebase-analytics.js")
    ]);
    if(await isSupported()){
      const app=getApps().length?getApp():initializeApp(firebaseConfig);
      getAnalytics(app);
    }
   }catch(error){console.info("Analytics unavailable on this device or browser.");}
 }
 const choice=getChoice();
 if(choice==="accepted")enableAnalytics();
 else if(choice!=="declined"){
   const wrap=document.createElement("div");wrap.id="analytics-consent";
   wrap.setAttribute("role","region");wrap.setAttribute("aria-label","Analytics preferences");
   const text=document.createElement("p");
   text.textContent="We use optional analytics to understand visits and improve this website. You can accept or decline.";
   const actions=document.createElement("div");
   const accept=document.createElement("button");accept.type="button";accept.textContent="Accept analytics";accept.className="consent-accept";
   const decline=document.createElement("button");decline.type="button";decline.textContent="Decline";decline.className="consent-decline";
   accept.addEventListener("click",()=>{saveChoice("accepted");wrap.remove();enableAnalytics()});
   decline.addEventListener("click",()=>{saveChoice("declined");wrap.remove()});
   actions.append(decline,accept);wrap.append(text,actions);document.body.append(wrap);
 }
}
