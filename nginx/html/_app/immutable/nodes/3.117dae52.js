import{s as u,o as d}from"../chunks/scheduler.e108d1fd.js";import{S as g,i as m}from"../chunks/index.0719bd3d.js";function p(i){return d(()=>{const t=new HTMLScriptElement;t.src="/rstudio/js/encrypt.min.js",t.onload=async()=>{const o=()=>{console.log("Redirecting to RStudio..."),window.location.href="/rstudio/"};try{console.log("Checking if user is already logged in...");let e=await fetch("/rstudio/",{credentials:"include",redirect:"manual"});if(e.ok||(console.log("User is not logged in, attempting to log in..."),e=await fetch("/rstudio/auth-sign-in",{credentials:"include",redirect:"manual"}),!e.ok))return o();let s=await e.text();const n=new DOMParser().parseFromString(s,"text/html"),r=n.getElementsByName("public-key-url")[0].getAttribute("content");if(console.log("Fetching public key..."),e=await fetch(`/rstudio/${r}`,{credentials:"include"}),!e.ok)return o();s=await e.text();const a=`${e.headers.get("Remote-User")}
passwd`,[l,c]=s.split(":",2);n.getElementById("clientPath").value="/rstudio/auth-sign-in",n.getElementById("package").value=encrypt(a,l,c),n.getElementById("persist").value="0",console.log("Submitting login form..."),n.getElementsByName("realform")[0].submit()}finally{o()}},document.head.appendChild(t)}),[]}class k extends g{constructor(t){super(),m(this,t,p,null,u,{})}}export{k as component};
