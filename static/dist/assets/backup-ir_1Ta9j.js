import{S as b,a as u}from"./sidebar-WLqGCHgY.js";import{_ as v,r as _,a as c,k as f,b as k,o as C,c as w,w as P,m as x,e as L,d as S,u as U}from"./index-CiGULDlY.js";const y={style:{width:"100%",height:"100%"}},B={__name:"backup",setup(D){const l=_({host_data:[]}),n=(a,r)=>{u.defaults.baseURL=x;let s={start:a,limit:r};const m="/backup-records?"+new URLSearchParams(s).toString();u.get(m).then(o=>{l.host_data=o.data.data,i.value=o.data.total}).catch(o=>{console.log(o)})};n(1,10);const i=c(0),t=c(1),e=c(10),p=_({count:i,limit:e,current:t}),d=f.map(a=>({...a})),g=a=>{t.value=a,n(t.value,e.value)},h=a=>{e.value=a,n(t.value,e.value)};return(a,r)=>{const s=k("bk-table");return C(),w(b,{active_key:"backup"},{default:P(()=>[L("div",y,[S(s,{columns:U(d),data:l.host_data,pagination:p,"remote-pagination":!0,onPageValueChange:g,onPageLimitChange:h,"show-overflow-tooltip":"",height:"100%"},null,8,["columns","data","pagination"])])]),_:1})}}},N=v(B,[["__scopeId","data-v-edee158f"]]);export{N as default};