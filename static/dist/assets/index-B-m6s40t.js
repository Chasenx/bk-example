import{S as ae,a as l}from"./sidebar-WLqGCHgY.js";import{_ as oe,r as p,a as i,D as se,b as k,o as c,c as V,w as m,m as d,d as u,e as b,f as w,g as D,F as x,h as y,t as v,u as le,p as ne,i as ie}from"./index-CiGULDlY.js";const ce=U=>(ne("data-v-63be38e7"),U=U(),ie(),U),de={style:{height:"1200px"}},ue={style:{"margin-left":"40px"}},re={class:"search_filed"},he=ce(()=>b("div",{style:{width:"40px",display:"inline-block"}},null,-1)),_e={class:"container"},ge={class:"left"},pe={class:"right"},me={__name:"index",setup(U){const z=p({host_data:[]}),f=i("全部"),r=i("全部"),h=i("全部"),B=i(!1),F=i({}),L=(t,e)=>{l.defaults.baseURL=d;let a={start:t,limit:e};f.value!=="全部"&&f.value!==0&&(a.business=f.value),r.value!=="全部"&&r.value!==0&&(a.set=r.value),h.value!=="全部"&&h.value!==0&&(a.module=h.value);const s="/hosts?"+new URLSearchParams(a).toString();console.log("get host api is: ",s),console.log("current is:",t,"limit is:",e),l.get(s).then(n=>{z.host_data=n.data.data,$.value=n.data.total}).catch(n=>{console.log(n)})};L(1,10);const $=i(0),_=i(1),g=i(10),A=p({count:$,limit:g,current:_}),H=se.map(t=>({...t})),E=t=>{_.value=t,console.log("current is:",_.value,"limit is:",g.value),L(_.value,g.value)},O=t=>{g.value=t,console.log("current is:",_.value,"limit is:",g.value),L(_.value,g.value)},X=t=>{console.log("handleRowSelect",t)},j=()=>{console.log("click search"),L(_.value,g.value)};p({});const q=i({}),G=(t,e,a,s,n)=>{l.defaults.baseURL=d;const R=`host-info?host=${e.host_id}`;console.log("host info api is: ",R),l.get(R).then(C=>{q.value=C.data}).catch(C=>{console.log(C)}),F.value=e,B.value=!0};i("search");const I=p([]);function J(){l.defaults.baseURL=d,l.get("business/").then(e=>{const a=e.data.data;a.unshift({biz_id:0,biz_name:"全部"}),I.splice(0,I.length,...a)}).catch(e=>{console.log(e)})}J();const P=p([]);function K(){l.defaults.baseURL=d;const e=`set?business=${f.value}`;l.get(e).then(a=>{const s=a.data.data;s.unshift({set_id:0,set_name:"全部"}),P.splice(0,P.length,...s)}).catch(a=>{console.log(a)})}const M=p([]);function Q(){l.defaults.baseURL=d;const e=`module?set=${r.value}`;l.get(e).then(a=>{const s=a.data.data;s.unshift({module_id:0,module_name:"全部"}),M.splice(0,M.length,...s)}).catch(a=>{console.log(a)})}const W=t=>{console.log("selectChange",t),K(),r.value="全部",h.value="全部"},Y=t=>{console.log("selectChange",t),Q(),h.value="全部"},Z=()=>{console.log("update CMDB"),l.defaults.baseURL=d,l.get("/sync-cmdb/").then(e=>{console.log(e.data)}).catch(e=>{console.log(e)})},N=p([]);(()=>{l.defaults.baseURL=d,l.get("/topo").then(e=>{N.splice(0,N.length,...e.data.data)}).catch(e=>{console.log(e)})})();const ee=()=>"default",te=(t,e)=>{console.log("click_tree_node",t,e),l.defaults.baseURL=d;let a={start,limit};const s="/hosts?"+new URLSearchParams(a).toString();console.log("get host api is: ",s),console.log("current is:",start,"limit is:",limit),l.get(s).then(n=>{z.host_data=n.data.data,$.value=n.data.total}).catch(n=>{console.log(n)})};return(t,e)=>{const a=k("bk-sideslider"),s=k("bk-option"),n=k("bk-select"),T=k("bk-button"),R=k("bk-tree"),C=k("bk-table");return c(),V(ae,{active_key:"index"},{default:m(()=>[u(a,{isShow:B.value,"onUpdate:isShow":e[0]||(e[0]=o=>B.value=o),title:"主机信息",width:"50%","quick-close":""},{default:m(()=>[b("div",de,[(c(!0),w(x,null,D(q.value.data,o=>(c(),w("div",ue,[b("p",null,v(o.bk_property_name)+": "+v(o.bk_property_value),1)]))),256))])]),_:1},8,["isShow"]),b("div",re,[y(v(t.$t("host.business"))+" ",1),u(n,{modelValue:f.value,"onUpdate:modelValue":e[1]||(e[1]=o=>f.value=o),class:"bk-select",onChange:W},{default:m(()=>[(c(!0),w(x,null,D(I,(o,S)=>(c(),V(s,{id:o.biz_id,key:S,name:o.biz_name},null,8,["id","name"]))),128))]),_:1},8,["modelValue"]),y(" "+v(t.$t("host.set"))+" ",1),u(n,{modelValue:r.value,"onUpdate:modelValue":e[2]||(e[2]=o=>r.value=o),class:"bk-select",onChange:Y},{default:m(()=>[(c(!0),w(x,null,D(P,(o,S)=>(c(),V(s,{id:o.set_id,key:S,name:o.set_name},null,8,["id","name"]))),128))]),_:1},8,["modelValue"]),y(" "+v(t.$t("host.module"))+" ",1),u(n,{modelValue:h.value,"onUpdate:modelValue":e[3]||(e[3]=o=>h.value=o),class:"bk-select"},{default:m(()=>[(c(!0),w(x,null,D(M,(o,S)=>(c(),V(s,{id:o.module_id,key:S,name:o.module_name},null,8,["id","name"]))),128))]),_:1},8,["modelValue"]),u(T,{onClick:j,theme:"primary"},{default:m(()=>[y(v(t.$t("host.search")),1)]),_:1}),he,u(T,{onClick:Z,theme:"success"},{default:m(()=>[y(v(t.$t("host.sync")),1)]),_:1})]),b("div",_e,[b("div",ge,[u(R,{data:N,"level-line":"","prefix-icon":ee,label:"bk_inst_name",children:"children",onNodeClick:te},null,8,["data"])]),b("div",pe,[u(C,{columns:le(H),data:z.host_data,pagination:A,"remote-pagination":!0,onPageValueChange:E,onPageLimitChange:O,onRowClick:G,onSelect:X,"show-overflow-tooltip":"",height:"100%"},null,8,["columns","data","pagination"])])])]),_:1})}}},ke=oe(me,[["__scopeId","data-v-63be38e7"]]);export{ke as default};
