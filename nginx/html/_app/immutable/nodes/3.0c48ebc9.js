import{s as p,o as w}from"../chunks/scheduler.e108d1fd.js";import{S as f,i as h}from"../chunks/index.0719bd3d.js";function y(r){return w(()=>{const e=document.createElement("script");e.src="/rstudio/js/encrypt.min.js",e.onload=async()=>{const n=()=>window.location.href="/rstudio/";try{let t=await fetch("/auth/api/state");if(!t.ok)return n();const o=`${(await t.json()).data.username}
passwd`;if(t=await fetch("/rstudio/",{redirect:"manual"}),t.ok||(t=await fetch("/rstudio/auth-sign-in"),!t.ok))return n();let s=await t.text();const a=new DOMParser().parseFromString(s,"text/html"),i=a.getElementsByName("public-key-url")[0].getAttribute("content");if(t=await fetch(`/rstudio/${i}`),!t.ok)return n();s=await t.text();const[c,u]=s.split(":",2);a.getElementById("clientPath").value="/rstudio/auth-sign-in",a.getElementById("package").value=encrypt(o,c,u),a.getElementById("persist").value="0";const l=new Request("/rstudio/auth-do-sign-in",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},redirect:"manual",body:new URLSearchParams(Array.from(new FormData(a.getElementsByName("realform")[0]),([d,m])=>[d,m]))});t=await fetch(l)}finally{n()}},document.head.appendChild(e)}),[]}class B extends f{constructor(e){super(),h(this,e,y,null,p,{})}}export{B as component};
