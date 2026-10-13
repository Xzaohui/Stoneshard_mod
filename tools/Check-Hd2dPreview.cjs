// Static validation only. This does not claim browser execution.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../src/Art/hd2d_26x26_20261013');
const html=fs.readFileSync(path.join(root,'preview.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script,{filename:'preview.html'});
const links=[...html.matchAll(/(?:src|href)="([^"]+)"/g)].map(m=>m[1]);
for(const rel of links){if(!fs.existsSync(path.join(root,rel)))throw Error('Missing preview link: '+rel);}
const layouts=JSON.parse(fs.readFileSync(path.join(root,'native_layouts.json'),'utf8'));
const roomLiteral=script.match(/const rooms=([\s\S]*?);\s*const canvas=/)[1];
const rooms=vm.runInNewContext('('+roomLiteral+')');
for(const layout of layouts){
  const name=layout.id.replace('r_eao_n1_',''),room=rooms[name];
  for(const [key,value] of Object.entries({rects:layout.walkable_rectangles,doors:layout.anchors.doors.map(a=>a.slice(1)),spawns:layout.anchors.spawns.map(a=>a.slice(1))})){
    if(JSON.stringify(room[key])!==JSON.stringify(value))throw Error('Preview geometry drift: '+name+'.'+key);
  }
  for(const part of ['backing','floor','structure','foreground'])if(!fs.existsSync(path.join(root,'assets/backgrounds/'+layout.id+'__'+part+'.png')))throw Error('Missing '+part);
}
const report={passed:true,scope:'JavaScript syntax, resource links and native geometry metadata; browser execution was unavailable',staticLinks:links.length,rooms:layouts.length,browserVerified:false};
fs.writeFileSync(path.join(root,'preview-validation.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
