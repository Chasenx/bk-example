import{S as Q,a as u}from"./sidebar-YD_tqtuq.js";import{_ as W,r as f,a as i,D as Y,b as h,o as b,c as S,w as l,m as j,d,e as m,f as v,g as C,F as x,h as g,t as k,u as Z,p as ee,i as _e}from"./index-BDtIV3k3.js";const ae=y=>(ee("data-v-966a2f19"),y=y(),_e(),y),te={style:{height:"1200px"}},ue={style:{"margin-left":"40px"}},ne={class:"search_filed"},be=ae(()=>m("div",{style:{width:"40px",display:"inline-block"}},null,-1)),ie={class:"container"},de={class:"left"},se={class:"right"},oe={__name:"index",setup(y){const U=f({host_data:[]}),c=i("全部"),s=i("全部"),o=i("全部"),q=i(!1),I=i({}),B=()=>{u.defaults.baseURL=j;let _={};c.value!=="全部"&&c.value!==0&&(_.business=c.value),s.value!=="全部"&&s.value!==0&&(_.set=s.value),o.value!=="全部"&&o.value!==0&&(_.module=o.value);const e="/hosts?"+new URLSearchParams(_).toString();console.log(e),u.get(e).then(t=>{U.host_data=t.data.data}).catch(t=>{console.log(t)})};B();const M=i({count:U.length,limit:10}),N=Y.map(_=>({..._})),F=_=>{console.log("handleRowSelect",_)};f({});const $=i({}),T=(_,e,t,n,w)=>{u.defaults.baseURL=j;const L=`host-info?host=${e.host_id}`;u.get(L).then(r=>{$.value=r.data}).catch(r=>{console.log(r)}),I.value=e,q.value=!0};i("search");const V=f([]);function A(){u.defaults.baseURL=j,u.get("business/").then(e=>{const t=e.data.data;t.unshift({biz_id:0,biz_name:"全部"}),V.splice(0,V.length,...t)}).catch(e=>{console.log(e)})}A();const z=f([]);function H(){u.defaults.baseURL=j;const e=`set?business=${c.value}`;u.get(e).then(t=>{const n=t.data.data;n.unshift({set_id:0,set_name:"全部"}),z.splice(0,z.length,...n)}).catch(t=>{console.log(t)})}const R=f([]);function P(){u.defaults.baseURL=j;const e=`module?set=${s.value}`;u.get(e).then(t=>{const n=t.data.data;n.unshift({module_id:0,module_name:"全部"}),R.splice(0,R.length,...n)}).catch(t=>{console.log(t)})}const E=_=>{console.log("selectChange",_),H(),s.value="全部",o.value="全部"},O=_=>{console.log("selectChange",_),P(),o.value="全部"},X=()=>{console.log("update CMDB"),u.defaults.baseURL=j,u.get("/sync-cmdb/").then(e=>{console.log(e.data)}).catch(e=>{console.log(e)})},G=f([{bk_inst_id:3,bk_inst_name:"demo体验业务",bk_obj_id:"biz",bk_obj_name:"业务",default:0,child:[{bk_inst_id:3,bk_inst_name:"agent可用环境",bk_obj_id:"environment",bk_obj_name:"环境",default:0,child:[{bk_inst_id:6,bk_inst_name:"自定义层级",bk_obj_id:"subsystem",bk_obj_name:"子系统",default:0,child:[{bk_inst_id:17,bk_inst_name:"通过集群模板创建的",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:76,bk_inst_name:"gamesvr",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1897,bk_inst_name:"nginx",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:77,bk_inst_name:"websvr",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:18,bk_inst_name:"直接创建的集群",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1893,bk_inst_name:"aa",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:78,bk_inst_name:"gamesvr",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1845,bk_inst_name:"logsvr",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:79,bk_inst_name:"websvr",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:80,bk_inst_name:"windows_svr",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]}]}]},{bk_inst_id:119,bk_inst_name:"测试环境",bk_obj_id:"environment",bk_obj_name:"环境",default:0,child:[{bk_inst_id:120,bk_inst_name:"订单",bk_obj_id:"subsystem",bk_obj_name:"子系统",default:0,child:[{bk_inst_id:147,bk_inst_name:"测试系统集群",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:585,bk_inst_name:"测试业务",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]}]}]},{bk_inst_id:493,bk_inst_name:"test",bk_obj_id:"environment",bk_obj_name:"环境",default:0,child:[{bk_inst_id:494,bk_inst_name:"test-1",bk_obj_id:"subsystem",bk_obj_name:"子系统",default:0,child:[{bk_inst_id:466,bk_inst_name:"test-集群",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1931,bk_inst_name:"test-模块",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:468,bk_inst_name:"test-集群2",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1933,bk_inst_name:"test-jqmysql",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1932,bk_inst_name:"test-web",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:469,bk_inst_name:"test-集群3",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1935,bk_inst_name:"test-jqmysql",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1934,bk_inst_name:"test-web",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:470,bk_inst_name:"test-集群4",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1937,bk_inst_name:"test-jqmysql",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1936,bk_inst_name:"test-web",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]}]}]},{bk_inst_id:495,bk_inst_name:"业务拓扑-新建",bk_obj_id:"environment",bk_obj_name:"环境",default:0,child:[{bk_inst_id:496,bk_inst_name:"业务拓扑-层级1",bk_obj_id:"subsystem",bk_obj_name:"子系统",default:0,child:[{bk_inst_id:471,bk_inst_name:"业务拓扑-关联集群模板",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1938,bk_inst_name:"服务模板",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]}]}]},{bk_inst_id:126,bk_inst_name:"正式环境",bk_obj_id:"environment",bk_obj_name:"环境",default:0,child:[{bk_inst_id:157,bk_inst_name:"门户网站",bk_obj_id:"subsystem",bk_obj_name:"子系统",default:0,child:[{bk_inst_id:447,bk_inst_name:"33",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1889,bk_inst_name:"mysql",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1890,bk_inst_name:"testtt",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:448,bk_inst_name:"testt",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1892,bk_inst_name:"test",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1891,bk_inst_name:"testtt",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:164,bk_inst_name:"网站集群1",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:629,bk_inst_name:"mysql",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:628,bk_inst_name:"nginx",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:630,bk_inst_name:"php",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:635,bk_inst_name:"redis",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:165,bk_inst_name:"网站集群2",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:632,bk_inst_name:"mysql",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:631,bk_inst_name:"nginx",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:633,bk_inst_name:"php",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:634,bk_inst_name:"redis",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:464,bk_inst_name:"网站集群3",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1925,bk_inst_name:"mysql",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1924,bk_inst_name:"nginx",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1926,bk_inst_name:"php",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1927,bk_inst_name:"redis",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]}]}]},{bk_inst_id:491,bk_inst_name:"这是一个环境",bk_obj_id:"environment",bk_obj_name:"环境",default:0,child:[{bk_inst_id:492,bk_inst_name:"这是一个层级",bk_obj_id:"subsystem",bk_obj_name:"子系统",default:0,child:[{bk_inst_id:465,bk_inst_name:"这是一个集群",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1928,bk_inst_name:"这是一个模块",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]},{bk_inst_id:467,bk_inst_name:"这是集群模板创建的集群",bk_obj_id:"set",bk_obj_name:"集群",default:0,child:[{bk_inst_id:1930,bk_inst_name:"dbserver",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]},{bk_inst_id:1929,bk_inst_name:"webserver",bk_obj_id:"module",bk_obj_name:"模块",default:0,child:[]}]}]}]}]}]),J=()=>"default",K=(_,e)=>{console.log("click_tree_node",_,e)};return(_,e)=>{const t=h("bk-sideslider"),n=h("bk-option"),w=h("bk-select"),D=h("bk-button"),L=h("bk-tree"),r=h("bk-table");return b(),S(Q,{active_key:"index"},{default:l(()=>[d(t,{isShow:q.value,"onUpdate:isShow":e[0]||(e[0]=a=>q.value=a),title:"主机信息",width:"50%","quick-close":""},{default:l(()=>[m("div",te,[(b(!0),v(x,null,C($.value.data,a=>(b(),v("div",ue,[m("p",null,k(a.bk_property_name)+": "+k(a.bk_property_value),1)]))),256))])]),_:1},8,["isShow"]),m("div",ne,[g(k(_.$t("host.business"))+" ",1),d(w,{modelValue:c.value,"onUpdate:modelValue":e[1]||(e[1]=a=>c.value=a),class:"bk-select",onChange:E},{default:l(()=>[(b(!0),v(x,null,C(V,(a,p)=>(b(),S(n,{id:a.biz_id,key:p,name:a.biz_name},null,8,["id","name"]))),128))]),_:1},8,["modelValue"]),g(" "+k(_.$t("host.set"))+" ",1),d(w,{modelValue:s.value,"onUpdate:modelValue":e[2]||(e[2]=a=>s.value=a),class:"bk-select",onChange:O},{default:l(()=>[(b(!0),v(x,null,C(z,(a,p)=>(b(),S(n,{id:a.set_id,key:p,name:a.set_name},null,8,["id","name"]))),128))]),_:1},8,["modelValue"]),g(" "+k(_.$t("host.module"))+" ",1),d(w,{modelValue:o.value,"onUpdate:modelValue":e[3]||(e[3]=a=>o.value=a),class:"bk-select"},{default:l(()=>[(b(!0),v(x,null,C(R,(a,p)=>(b(),S(n,{id:a.module_id,key:p,name:a.module_name},null,8,["id","name"]))),128))]),_:1},8,["modelValue"]),d(D,{onClick:B,theme:"primary"},{default:l(()=>[g(k(_.$t("host.search")),1)]),_:1}),be,d(D,{onClick:X,theme:"success"},{default:l(()=>[g(k(_.$t("host.sync")),1)]),_:1})]),m("div",ie,[m("div",de,[d(L,{data:G,"level-line":"","prefix-icon":J,label:"bk_inst_name",children:"child",onNodeClick:K},null,8,["data"])]),m("div",se,[d(r,{columns:Z(N),data:U.host_data,pagination:M.value,"pagination-heihgt":60,onRowClick:T,onSelect:F,"show-overflow-tooltip":"",height:"100%"},null,8,["columns","data","pagination"])])])]),_:1})}}},me=W(oe,[["__scopeId","data-v-966a2f19"]]);export{me as default};