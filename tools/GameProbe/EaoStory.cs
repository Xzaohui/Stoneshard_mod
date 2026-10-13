using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Decompiler;

internal static class EaoStory
{
    internal static string[] Validate(UndertaleData data)
    {
        if(!data.GameObjects.Any(o=>o.Name.Content=="o_eao_n1_mara")) return Array.Empty<string>();
        var checks=new List<string>();
        string Asm(string name) {var c=data.Code.Single(c=>c.Name.Content==name);return c.Disassemble(data.Variables,data.CodeLocals.For(c));}
        var step=Asm("gml_Object_o_eao_controller_Step_1");
        if(step.Contains("EAO_MQ01")||step.Contains("EAO_MQ02")||Regex.IsMatch(step,@"pushi\.e 4\s+conv\.i\.v\s+call\.i event_user")||!step.Contains("instance_destroy")) throw new InvalidDataException("Retired quest is still active.");
        foreach(var old in new[]{"courier","d01_clerk","d01_entry"}) {
            var i=data.GameObjects.IndexOf(data.GameObjects.Single(o=>o.Name.Content=="o_eao_"+old));
            if(!Regex.IsMatch(step,@"push(?:i\.e|\.i) "+i+@"\s+conv\.i\.v\s+call\.i instance_destroy")) throw new InvalidDataException("Legacy actor/entrance not retired.");
        }
        if(!step.Contains("astar_get_cell")||!step.Contains("scr_check_collision_not_enemy_around")||!step.Contains("event_user")) throw new InvalidDataException("Camp spawn/retained teleport interface missing.");
        checks.Add("old-quest-retired-with-legacy-resource-indices-retained");
        foreach(var id in new[]{"mara","tor","ivo","rhea","rope","cots"}) {
            var obj=data.GameObjects.Single(o=>o.Name.Content=="o_eao_n1_"+id);
            if(obj.ParentId?.Name.Content!="o_simple_NPC"||obj.Sprite==null||!obj.Visible) throw new InvalidDataException("Story actor lacks native NPC, visible sprite or interaction mask.");
            var create=data.Code.Single(c=>c.Name.Content=="gml_Object_"+obj.Name.Content+"_Create_0");
            EaoInteraction.ValidateStructReceiver(Asm(create.Name.Content));
            var literals=create.Instructions.Select(i=>i.Value).OfType<UndertaleResourceById<UndertaleString,UndertaleChunkSTRG>>().Select(v=>v.Resource.Content).ToArray();
            using var flow=JsonDocument.Parse(literals.Single(s=>s.StartsWith("{\"RootFragment\":\"eao_n1_"+id+"\"")));
            using var lines=JsonDocument.Parse(literals.Single(s=>s.StartsWith("{\"N1_")));
            var fragments=flow.RootElement.GetProperty("Fragments");var specs=flow.RootElement.GetProperty("Specs");
            var root=flow.RootElement.GetProperty("RootFragment").GetString()!;var edges=new Dictionary<string,string[]>();
            foreach(var f in fragments.EnumerateObject()) {
                var next=f.Value.ValueKind==JsonValueKind.Array?f.Value.EnumerateArray().Select(v=>v.GetString()!).ToArray():new[]{f.Value.GetString()!};edges[f.Name]=next;
                if(next.Any(n=>n!="@dialogue_end"&&!fragments.TryGetProperty(n,out _))) throw new InvalidDataException("Broken story dialogue edge.");
                if(f.Name.StartsWith("instruction_")&&!f.Name.EndsWith("_resume")&&!specs.GetProperty(f.Name).GetProperty("action").GetBoolean()) throw new InvalidDataException("Story action runs during preview.");
                if(f.Name.EndsWith("_pc")&&!specs.GetProperty(f.Name).GetProperty("technical").GetBoolean()) throw new InvalidDataException("Repeat option can disappear.");
                if(!f.Name.StartsWith("instruction_")&&f.Name!=root&&!lines.RootElement.TryGetProperty(f.Name,out _)) throw new InvalidDataException("Story line missing.");
            }
            var reached=new HashSet<string>();var queue=new Queue<string>();queue.Enqueue(root);
            while(queue.TryDequeue(out var n)) if(reached.Add(n)&&n!="@dialogue_end") foreach(var e in edges[n])queue.Enqueue(e);
            if(!reached.Contains("@dialogue_end")||edges.Keys.Any(n=>!reached.Contains(n)))throw new InvalidDataException("Unreachable story branch.");
            if(id is "rope" or "cots") {
                var leave="N1_"+id+"_leave_pc";
                if(!edges["N1_"+id+"_intro"].Contains(leave)||!edges[leave].SequenceEqual(new[]{"@dialogue_end"}))
                    throw new InvalidDataException("Clue preview cannot exit before quest acceptance.");
                checks.Add(id+"-unconditional-exit-before-quest-acceptance");
            }
            if(lines.RootElement.EnumerateObject().Any(l=>l.Value.GetArrayLength()!=2||l.Value[1].GetString()!.Length>100))throw new InvalidDataException("Story localization invalid/too long.");
            foreach(var kind in new[]{EventType.Mouse,EventType.Draw})if(!Asm(obj.Events[(int)kind].Single(e=>e.EventSubtype==(kind==EventType.Mouse?4U:0U)).Actions.Single().CodeId.Name.Content).Contains("event_inherited"))throw new InvalidDataException("Story actor replaced native interaction.");
            checks.Add(id+"-native-dialogue-connected-localized-and-preview-safe");
        }
        var roomNames=new[]{"r_eao_n1_yard","r_eao_n1_bellhouse","r_eao_n1_underpass"};var signatures=new HashSet<string>();
        foreach(var name in roomNames) {
            var room=data.Rooms.Single(r=>r.Name.Content==name);
            if(room.Width!=1040||room.Height!=780||room.Persistent||room.CreationCodeId!=null)throw new InvalidDataException("New scene metadata mismatch.");
            if(room.GameObjects.Any(i=>i.ObjectDefinition.Name.Content.Contains("DockStore")||i.ObjectDefinition.Name.Content.StartsWith("o_npc_")))throw new InvalidDataException("Source building art/NPC leaked.");
            var mapped=room.Layers.Where(l=>l.LayerType==UndertaleRoom.LayerType.Instances).SelectMany(l=>l.InstancesData.Instances).ToArray();
            if(mapped.Length!=room.GameObjects.Count||mapped.Distinct().Count()!=mapped.Length)throw new InvalidDataException("New scene layer mapping invalid.");
            var blocked=room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
            var walk=new HashSet<(int,int)>();for(var x=0;x<40;x++)for(var y=0;y<30;y++)if(!blocked.Contains((x,y)))walk.Add((x,y));
            signatures.Add(string.Join(";",walk.OrderBy(p=>p.Item1).ThenBy(p=>p.Item2)));
            var reached=new HashSet<(int,int)>();var queue=new Queue<(int,int)>();queue.Enqueue(walk.First());
            while(queue.TryDequeue(out var p))if(reached.Add(p))foreach(var q in new[]{(p.Item1+1,p.Item2),(p.Item1-1,p.Item2),(p.Item1,p.Item2+1),(p.Item1,p.Item2-1)})if(walk.Contains(q)&&!reached.Contains(q))queue.Enqueue(q);
            if(reached.Count!=walk.Count||walk.Any(p=>p.Item1<2||p.Item2<2||p.Item1>37||p.Item2>27))throw new InvalidDataException("Disconnected floor or unsafe border.");
            var player=room.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_abstract_player");
            foreach(var node in room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content.StartsWith("o_eao_n1_")&&i.ObjectDefinition.Name.Content is not ("o_eao_n1_floor" or "o_eao_n1_bell_art"))) {
                if(!walk.Contains(((int)node.X/26,(int)node.Y/26)))throw new InvalidDataException("Story node outside walkable area.");
                if(node.ObjectDefinition.Name.Content.Contains("start_")&&room.GameObjects.IndexOf(node)>=room.GameObjects.IndexOf(player))throw new InvalidDataException("Arrival marker after player.");
            }
            foreach(var i in room.GameObjects)if(data.Rooms.Sum(r=>r.GameObjects.Count(o=>o.InstanceID==i.InstanceID))!=1)throw new InvalidDataException("Duplicate story instance ID.");
            checks.Add(name+"-connected-unique-native-collision-and-arrival-order");
        }
        if(signatures.Count!=3)throw new InvalidDataException("Same floor plan reused.");checks.Add("three-distinct-floor-plans-without-original-building-backdrops");
        foreach(var (id,target,tag) in new[]{("entry",roomNames[0],"EAO_N1_yard_in"),("home","r_DockStore1floor","NA"),("to_bell",roomNames[1],"EAO_N1_house_in"),("to_yard",roomNames[0],"EAO_N1_yard_back"),("to_drain",roomNames[2],"EAO_N1_drain_in"),("to_house",roomNames[1],"EAO_N1_house_back")}) {
            var obj=data.GameObjects.Single(o=>o.Name.Content=="o_eao_n1_"+id);var create=Asm("gml_Object_"+obj.Name.Content+"_Create_0");var ri=data.Rooms.IndexOf(data.Rooms.Single(r=>r.Name.Content==target));
            if(!Regex.IsMatch(create,@"push(?:i\.e|\.i) "+ri+@"\s+pop\.v\.i self.target")||!create.Contains(tag)||obj.Events[(int)EventType.Mouse].Count!=0||obj.Events[(int)EventType.Other].Count!=0)throw new InvalidDataException("Native story door target/tag mismatch.");
            checks.Add(id+"-native-transition-resource-index-and-tag");
        }
        var entry=Asm("gml_Object_o_eao_n1_entry_Alarm_7");var home=Asm("gml_Object_o_eao_n1_home_Alarm_7");
        if(!entry.Contains("event_inherited")||!entry.Contains("EAO_N1_origin_room")||!home.Contains("event_inherited")||!home.Contains("scr_atr_set_simple")||entry.Contains("scr_smoothRoomChange")||home.Contains("scr_smoothRoomChange"))throw new InvalidDataException("Story route bypasses native save.");
        checks.Add("source-and-return-coordinates-follow-native-door-transition");
        var art=data.Sprites.Single(s=>s.Name.Content=="s_eao_n1_bell");
        // Embedded texture display names are rebuilt by UndertaleIO on read;
        // verify the actual PNG bytes rather than this nonserialized name.
        var actualPng=art.Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray();
        var sourcePng=File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),"src","EmbersAndOaths","Assets","night-bell-v1.png"));
        if(!actualPng.SequenceEqual(sourcePng)||!Asm("gml_Object_o_eao_n1_bell_art_Draw_0").Contains("draw_sprite_ext"))throw new InvalidDataException("Original art bytes or drawing reference missing.");
        foreach(var n in new[]{"s_eao_n1_bellP","s_eao_n1_cotsP"}) {var s=data.Sprites.Single(s=>s.Name.Content==n);if(s.Width!=37||s.Height!=50||s.OriginX!=0||s.OriginY!=0)throw new InvalidDataException("Inspection portrait geometry mismatch.");}
        checks.Add("original-generated-bell-art-and-native-sized-inspection-portraits");return checks.ToArray();
    }
    internal static void Preview(UndertaleData data)
    {
        var layouts=new[]{"r_eao_n1_yard","r_eao_n1_bellhouse","r_eao_n1_underpass"}.Select(n=> {var r=data.Rooms.Single(r=>r.Name.Content==n);return new{name=n,title=r.Caption.Content,blocked=r.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>new[]{(int)i.X/26,(int)i.Y/26}).ToArray(),nodes=r.GameObjects.Where(i=>i.ObjectDefinition.Name.Content.StartsWith("o_eao_n1_")&&!i.ObjectDefinition.Name.Content.Contains("floor")).Select(i=>new{name=i.ObjectDefinition.Name.Content,x=i.X,y=i.Y}).ToArray()};}).ToArray();
        var html="<!doctype html><meta charset='utf-8'><title>无钟之夜 · 场景预览</title><style>body{background:#171f23;color:#eee;font:16px sans-serif;margin:24px}button{padding:10px;margin:5px;background:#4c5551;color:#fff;border:0}canvas{width:min(100%,1040px);image-rendering:pixelated;border:1px solid #777}p{max-width:1000px}</style><h1>无钟之夜 · 候选包实际布局</h1><p>断桥、钟房侧通道、暗渠折返分别重建。灰色为可走格，深色为碰撞格；黄点为剧情交互，绿色为落点。实际光照、鼠标命中与寻路仍须运行验证。</p><nav id='tabs'></nav><h2 id='title'></h2><canvas id='map' width='1040' height='780'></canvas><script>const layouts="+JsonSerializer.Serialize(layouts)+";const c=document.getElementById('map'),g=c.getContext('2d');const bell=new Image();bell.src='../src/EmbersAndOaths/Assets/night-bell-v1.png';function draw(k){let l=layouts[k];document.getElementById('title').textContent=l.title;g.fillStyle='#45504c';g.fillRect(0,0,1040,780);g.fillStyle='#13272c';l.blocked.forEach(p=>g.fillRect(p[0]*26,p[1]*26,26,26));g.strokeStyle='#273a3d';for(let x=0;x<=1040;x+=26){g.beginPath();g.moveTo(x,0);g.lineTo(x,780);g.stroke()}for(let y=0;y<=780;y+=26){g.beginPath();g.moveTo(0,y);g.lineTo(1040,y);g.stroke()}for(let n of l.nodes){if(n.name.includes('bell_art')&&bell.complete)g.drawImage(bell,n.x-52,n.y-130,104,156);g.fillStyle=n.name.includes('start_')?'#8bd58d':'#ffc976';g.fillRect(n.x-4,n.y-4,8,8);g.font='12px sans-serif';g.fillText(n.name.replace('o_eao_n1_',''),n.x+8,n.y-5)}}layouts.forEach((l,k)=>{let b=document.createElement('button');b.textContent=l.title;b.onclick=()=>draw(k);document.getElementById('tabs').append(b)});bell.onload=()=>draw(0);draw(0);</script>";
        File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","night-layout.html"),"artifacts"),html);
    }
}
