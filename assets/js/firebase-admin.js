import {firebaseConfig,firebaseConfigured} from "./firebase-config.js";
const el=id=>document.getElementById(id);
const show=(id,visible)=>el(id).classList.toggle("is-hidden",!visible);
const status=(msg,type="")=>{const node=el("status");node.textContent=msg;node.className="notice"+(type?" "+type:"");};
const fields={
 "siteContent/company":[["heroLead","Homepage hero introduction",700],["heroBangla","Bangla hero tagline",250],["aboutIntro","About page introduction",900],["contactEmail","Official contact email",160],["contactPhone","Official contact phone",120]],
 "products/aeroplane-alkatra":[["summary","Product card summary",300],["description","Product detail introduction",1200]],
 "products/urojahaj-alkatra":[["summary","Product card summary",300],["description","Product detail introduction",1200]],
 "products/orbit-steel-care":[["summary","Product card summary",300],["description","Product detail introduction",1200]]
};
if(!firebaseConfigured){
 status("Firebase project has not been connected. Add your public Web App config in /assets/js/firebase-config.js, enable Google sign-in and deploy the Firestore rules. The public website still works normally.");
}else{
 try{
  const [{initializeApp},{getAuth,GoogleAuthProvider,signInWithPopup,signOut,onAuthStateChanged},{getFirestore,doc,getDoc,setDoc,serverTimestamp}]=await Promise.all([
   import("https://www.gstatic.com/firebasejs/13.2.0/firebase-app.js"),
   import("https://www.gstatic.com/firebasejs/13.2.0/firebase-auth.js"),
   import("https://www.gstatic.com/firebasejs/13.2.0/firebase-firestore.js")
  ]);
  const auth=getAuth(initializeApp(firebaseConfig)),db=getFirestore(auth.app);
  const provider=new GoogleAuthProvider();
  let currentUser=null;
  el("sign-in").addEventListener("click",async()=>{
    el("sign-in").disabled=true;
    try{await signInWithPopup(auth,provider);}
    catch(err){status("Google sign-in failed. Confirm this hostname is in Firebase Authentication Authorized domains. "+(err.code||""),"error");}
    finally{el("sign-in").disabled=false;}
  });
  el("sign-out").addEventListener("click",()=>signOut(auth));
  const buildFields=(path,values={})=>{
   const box=el("editor-fields");box.replaceChildren();
   for(const [key,label,max] of fields[path]){
    const labelEl=document.createElement("label");labelEl.textContent=label;labelEl.htmlFor="field-"+key;box.append(labelEl);
    const input=document.createElement(key==="contactEmail"||key==="contactPhone"?"input":"textarea");
    if(input.tagName==="INPUT")input.type="text";
    input.id="field-"+key;input.name=key;input.maxLength=max;
    if(input.tagName==="TEXTAREA")input.rows=key==="description"?6:3;
    input.value=typeof values[key]==="string"?values[key]:"";box.append(input);
    const hint=document.createElement("p");hint.className="help";hint.textContent="Maximum "+max+" characters.";box.append(hint);
   }
   el("publish").checked=values.published===true;
  };
  const load=async()=>{
    if(!currentUser)return;
    const path=el("doc-choice").value,[collection,id]=path.split("/");
    el("save-state").textContent="Loading…";el("save").disabled=true;
    try{
      const snap=await getDoc(doc(db,collection,id));buildFields(path,snap.exists()?snap.data():{});
      el("save-state").textContent=snap.exists()?"Loaded.":"New draft; not published.";
    }catch(err){
      buildFields(path);el("save-state").textContent="Cannot load: "+(err.code||"error");
      status("Content loading failed. Check Firestore rules and administrator permissions.","error");
    }finally{el("save").disabled=false;}
  };
  el("doc-choice").addEventListener("change",load);
  el("edit-form").addEventListener("submit",async event=>{
    event.preventDefault();if(!currentUser)return;
    const path=el("doc-choice").value,[collection,id]=path.split("/");
    const values={published:el("publish").checked,updatedBy:currentUser.uid,updatedAt:serverTimestamp()};
    for(const [key] of fields[path])values[key]=el("field-"+key).value.trim();
    if(values.published&&collection==="products"&&(!values.summary||!values.description)){
      el("save-state").textContent="Both product fields are required to publish.";return;
    }
    el("save").disabled=true;el("save-state").textContent="Saving…";
    try{
      await setDoc(doc(db,collection,id),values,{merge:true});
      el("save-state").textContent=values.published?"Published.":"Draft saved.";
      status("Changes securely saved to Firestore.","success");
    }catch(err){el("save-state").textContent="Save failed: "+(err.code||"error");status("Save failed. Verify rules and admin access.","error");}
    finally{el("save").disabled=false;}
  });
  onAuthStateChanged(auth,async user=>{
   show("app-panel",false);
   if(!user){currentUser=null;show("login-panel",true);status("Firebase configured. Please sign in to continue.");return;}
   status("Verifying administrator privileges…");
   try{
    const admin=await getDoc(doc(db,"adminUsers",user.uid));
    if(admin.exists()&&admin.data().active===true){
      currentUser=user;show("login-panel",false);show("app-panel",true);
      el("signed-user").textContent=user.email||user.uid;
      status("Authorized administrator.","success");await load();
    }else{
      currentUser=null;show("login-panel",true);
      status("Account not authorized. Your Firebase Auth UID is: "+user.uid,"error");
    }
   }catch(err){currentUser=null;show("login-panel",true);status("Cannot verify access: "+(err.code||"error"),"error");}
  });
 }catch(err){status("Firebase SDK could not be loaded. Verify HTTPS, connectivity and config.","error");}
}
