// Progressive enhancement; verified static text remains when content is absent/unpublished.
import {firebaseConfig,firebaseConfigured} from "./firebase-config.js";
if(firebaseConfigured){
 try{
  const [{initializeApp},{getFirestore,getDoc,doc}]=await Promise.all([
   import("https://www.gstatic.com/firebasejs/13.2.0/firebase-app.js"),
   import("https://www.gstatic.com/firebasejs/13.2.0/firebase-firestore.js")
  ]);
  const db=getFirestore(initializeApp(firebaseConfig));
  const safe=v=>typeof v==="string"&&v.trim()?v.slice(0,5000):null;
  async function published(col,id,apply){
   try{const docSnap=await getDoc(doc(db,col,id));if(docSnap.exists()&&docSnap.data().published===true)apply(docSnap.data());}
   catch(e){console.info("Using approved static content (dynamic content unavailable).");}
  }
  if(document.querySelector("[data-cms-field]")){
   await published("siteContent","company",data=>{
    document.querySelectorAll("[data-cms-field]").forEach(el=>{
      const value=safe(data[el.dataset.cmsField]);if(value)el.textContent=value;
    });
   });
  }
  const ids=[...new Set([...document.querySelectorAll("[data-product-summary],[data-product-description]")].map(x=>x.dataset.productSummary||x.dataset.productDescription))];
  await Promise.all(ids.map(id=>published("products",id,data=>{
    document.querySelectorAll("[data-product-summary]").forEach(el=>{
      if(el.dataset.productSummary===id){const val=safe(data.summary);if(val)el.textContent=val;}
    });
    document.querySelectorAll("[data-product-description]").forEach(el=>{
      if(el.dataset.productDescription===id){const val=safe(data.description);if(val)el.textContent=val;}
    });
  })));
 }catch(e){console.info("Firebase is unavailable; static pages remain visible.");}
}
