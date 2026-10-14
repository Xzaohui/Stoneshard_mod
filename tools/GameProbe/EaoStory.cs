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
        checks.Add("original-generated-bell-art-and-native-sized-inspection-portraits");
        // ---- Pilot batch P1 (MGMT-PILOT-N2-S153): 灰堤没有墓碑 ----
        if(data.GameObjects.Any(o=>o.Name.Content=="o_eao_n2_aina")) {
            var registered=new[]{"EAO_encountered_N2","EAO_resolve_N2","EAO_callback_N2_protected","EAO_callback_N2_public","EAO_presence_N2"};
            var scriptRefs=new Dictionary<string,string[]>{
                ["aina"]=new[]{"没有人把他从水里捞出来。可收债的肯承认他死，只要我也承认营里不再欠他工钱。","你要的不是葬礼？","我要能活到下一次葬礼。他要真活着，我也得先吃饭。","他们会问他住哪。","可以只纠正死亡和欠薪，不公开藏身点；也可以要求他到听审处作证。","他是我丈夫，不是我的赔偿凭据。让他自己选。"},
                ["watcher"]=new[]{"事故之后，有人还用过他的刻刀。","刻记不能证明是他。可拆绞盘那天，工头说死人不用领停工钱。","一件工具不能证明人活着。那就找用工具的人。"},
                ["nara"]=new[]{"他们把我的死填好了。再回去，欠薪没了，欠债倒会回来。","艾娜在替你办葬礼。","告诉她我活着。但别替我签回营的纸。我修得了轴，已经爬不上堤。","提交匿名工伤核验，保留住址，追讨欠薪。","纳拉同意实名作证，安排短程安全转移。"}
            };
            foreach(var id in new[]{"aina","watcher","nara","coffin","winch"}) {
                var obj=data.GameObjects.Single(o=>o.Name.Content=="o_eao_n2_"+id);
                if(obj.ParentId?.Name.Content!="o_simple_NPC"||obj.Sprite==null||!obj.Visible) throw new InvalidDataException("N2 actor lacks native NPC, visible sprite or interaction mask.");
                var create=data.Code.Single(c=>c.Name.Content=="gml_Object_o_eao_n2_"+id+"_Create_0");
                EaoInteraction.ValidateStructReceiver(Asm(create.Name.Content));
                var literals=create.Instructions.Select(i=>i.Value).OfType<UndertaleResourceById<UndertaleString,UndertaleChunkSTRG>>().Select(v=>v.Resource.Content).ToArray();
                using var flow=JsonDocument.Parse(literals.Single(s=>s.StartsWith("{\"RootFragment\":\"eao_n2_"+id+"\"")));
                using var lines=JsonDocument.Parse(literals.Single(s=>s.StartsWith("{\"N2_")));
                var fragments=flow.RootElement.GetProperty("Fragments");var specs=flow.RootElement.GetProperty("Specs");
                var root=flow.RootElement.GetProperty("RootFragment").GetString()!;var edges=new Dictionary<string,string[]>();
                foreach(var f in fragments.EnumerateObject()) {
                    var next=f.Value.ValueKind==JsonValueKind.Array?f.Value.EnumerateArray().Select(v=>v.GetString()!).ToArray():new[]{f.Value.GetString()!};edges[f.Name]=next;
                    if(next.Any(n=>n!="@dialogue_end"&&!fragments.TryGetProperty(n,out _))) throw new InvalidDataException("Broken N2 dialogue edge.");
                    if(f.Name.StartsWith("instruction_")&&!f.Name.EndsWith("_resume")&&!specs.GetProperty(f.Name).GetProperty("action").GetBoolean()) throw new InvalidDataException("N2 action runs during preview.");
                    if(f.Name.EndsWith("_pc")&&!specs.GetProperty(f.Name).GetProperty("technical").GetBoolean()) throw new InvalidDataException("N2 repeat option can disappear.");
                    if(!f.Name.StartsWith("instruction_")&&f.Name!=root&&!lines.RootElement.TryGetProperty(f.Name,out _)) throw new InvalidDataException("N2 line missing.");
                }
                var reached=new HashSet<string>();var queue=new Queue<string>();queue.Enqueue(root);
                while(queue.TryDequeue(out var n)) if(reached.Add(n)&&n!="@dialogue_end") foreach(var e in edges[n])queue.Enqueue(e);
                if(!reached.Contains("@dialogue_end")||edges.Keys.Any(n=>!reached.Contains(n)))throw new InvalidDataException("Unreachable N2 branch.");
                if(lines.RootElement.EnumerateObject().Any(l=>l.Value.GetArrayLength()!=2||l.Value[1].GetString()!.Length>100))throw new InvalidDataException("N2 localization invalid/too long.");
                if(scriptRefs.TryGetValue(id,out var expected))
                    foreach(var line in expected)
                        if(!lines.RootElement.EnumerateObject().Any(l=>l.Value[1].GetString()==line)) throw new InvalidDataException("N2 script ref not verbatim: "+line);
                var keyLiterals=literals.Where(s=>s.StartsWith("EAO_")&&s.All(c=>char.IsAsciiLetterOrDigit(c)||c=='_')).ToArray();
                if(keyLiterals.Any(k=>!registered.Contains(k))) throw new InvalidDataException("Unregistered save key in N2 code: "+string.Join(",",keyLiterals.Except(registered)));
                foreach(var kind in new[]{EventType.Mouse,EventType.Draw})if(!Asm(obj.Events[(int)kind].Single(e=>e.EventSubtype==(kind==EventType.Mouse?4U:0U)).Actions.Single().CodeId.Name.Content).Contains("event_inherited"))throw new InvalidDataException("N2 actor replaced native interaction.");
                checks.Add("n2-"+id+"-native-dialogue-verbatim-refs-registered-keys-only");
            }
            var stubAsm=Asm("gml_Object_o_eao_n2_nara_Create_0");
            foreach(var pair in new[]{("evt_N2_entry","10640"),("evt_N2_hub","10641"),("evt_N2_choice_protected","10642"),("evt_N2_choice_public","10643"),("evt_N2_refusal","10644")})
                if(!stubAsm.Contains(pair.Item1)||!stubAsm.Contains(pair.Item2)) throw new InvalidDataException("N2 stub registry/engine number missing: "+pair.Item1);
            if(!stubAsm.Contains("\"protected\"")||!stubAsm.Contains("\"public\"")||!stubAsm.Contains("\"refused\""))throw new InvalidDataException("N2 registered settlement values missing.");
            checks.Add("n2-stub-registry-with-engine-event-numbers-10640-10644");
            var n2Rooms=new[]{"r_eao_n2_camp","r_eao_n2_winch","r_eao_n2_side"};var n2Signatures=new HashSet<string>();
            foreach(var name in n2Rooms) {
                var room=data.Rooms.Single(r=>r.Name.Content==name);
                if(room.Width!=1040||room.Height!=780||room.Persistent||room.CreationCodeId!=null)throw new InvalidDataException("N2 scene metadata mismatch.");
                if(room.GameObjects.Any(i=>i.ObjectDefinition.Name.Content.Contains("DockStore")||i.ObjectDefinition.Name.Content.StartsWith("o_npc_")))throw new InvalidDataException("Source building art/NPC leaked.");
                var mapped=room.Layers.Where(l=>l.LayerType==UndertaleRoom.LayerType.Instances).SelectMany(l=>l.InstancesData.Instances).ToArray();
                if(mapped.Length!=room.GameObjects.Count||mapped.Distinct().Count()!=mapped.Length)throw new InvalidDataException("N2 scene layer mapping invalid.");
                var blocked=room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
                var walk=new HashSet<(int,int)>();for(var x=0;x<40;x++)for(var y=0;y<30;y++)if(!blocked.Contains((x,y)))walk.Add((x,y));
                n2Signatures.Add(string.Join(";",walk.OrderBy(p=>p.Item1).ThenBy(p=>p.Item2)));
                var reached=new HashSet<(int,int)>();var queue=new Queue<(int,int)>();queue.Enqueue(walk.First());
                while(queue.TryDequeue(out var p))if(reached.Add(p))foreach(var q in new[]{(p.Item1+1,p.Item2),(p.Item1-1,p.Item2),(p.Item1,p.Item2+1),(p.Item1,p.Item2-1)})if(walk.Contains(q)&&!reached.Contains(q))queue.Enqueue(q);
                if(reached.Count!=walk.Count||walk.Any(p=>p.Item1<2||p.Item2<2||p.Item1>37||p.Item2>27))throw new InvalidDataException("Disconnected N2 floor or unsafe border.");
                var player=room.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_abstract_player");
                foreach(var node in room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content.StartsWith("o_eao_n2_")&&i.ObjectDefinition.Name.Content!="o_eao_n2_floor")) {
                    if(!walk.Contains(((int)node.X/26,(int)node.Y/26)))throw new InvalidDataException("N2 node outside walkable area.");
                    if(node.ObjectDefinition.Name.Content.Contains("start_")&&room.GameObjects.IndexOf(node)>=room.GameObjects.IndexOf(player))throw new InvalidDataException("N2 arrival marker after player.");
                }
                foreach(var i in room.GameObjects)if(data.Rooms.Sum(r=>r.GameObjects.Count(o=>o.InstanceID==i.InstanceID))!=1)throw new InvalidDataException("Duplicate N2 instance ID.");
                checks.Add(name+"-connected-unique-native-collision-and-arrival-order");
            }
            if(n2Signatures.Count!=3)throw new InvalidDataException("Same N2 floor plan reused.");checks.Add("three-distinct-n2-floor-plans-without-original-building-backdrops");
            foreach(var (id,target,tag) in new[]{("entry",n2Rooms[0],"EAO_N2_camp_in"),("home","r_DockStore1floor","NA"),("to_winch",n2Rooms[1],"EAO_N2_winch_in"),("camp_back",n2Rooms[0],"EAO_N2_camp_back"),("to_side",n2Rooms[2],"EAO_N2_side_in"),("side_back",n2Rooms[1],"EAO_N2_winch_back")}) {
                var obj=data.GameObjects.Single(o=>o.Name.Content=="o_eao_n2_"+id);var create=Asm("gml_Object_o_eao_n2_"+id+"_Create_0");var ri=data.Rooms.IndexOf(data.Rooms.Single(r=>r.Name.Content==target));
                if(!Regex.IsMatch(create,@"push(?:i\.e|\.i) "+ri+@"\s+pop\.v\.i self.target")||!create.Contains(tag)||obj.Events[(int)EventType.Mouse].Count!=0||obj.Events[(int)EventType.Other].Count!=0)throw new InvalidDataException("N2 door target/tag mismatch.");
                checks.Add("n2-"+id+"-native-transition-resource-index-and-tag");
            }
            var n2EntryAlarm=Asm("gml_Object_o_eao_n2_entry_Alarm_7");var n2HomeAlarm=Asm("gml_Object_o_eao_n2_home_Alarm_7");
            if(!n2EntryAlarm.Contains("event_inherited")||!n2EntryAlarm.Contains("EAO_N1_origin_room")||!n2HomeAlarm.Contains("event_inherited")||!n2HomeAlarm.Contains("scr_atr_set_simple")||n2EntryAlarm.Contains("scr_smoothRoomChange")||n2HomeAlarm.Contains("scr_smoothRoomChange"))throw new InvalidDataException("N2 route bypasses native save.");
            checks.Add("n2-source-and-return-coordinates-follow-native-door-transition");
            foreach(var n in new[]{"s_eao_n2_coffinP","s_eao_n2_winchP"}) {var s=data.Sprites.Single(s=>s.Name.Content==n);if(s.Width!=37||s.Height!=50||s.OriginX!=0||s.OriginY!=0)throw new InvalidDataException("N2 inspection portrait geometry mismatch.");}
            checks.Add("n2-native-sized-inspection-portraits");
            var n2EntryIndex=data.GameObjects.IndexOf(data.GameObjects.Single(o=>o.Name.Content=="o_eao_n2_entry"));
            // The object constant is pushed (and converted) before the three
            // coordinate arguments of the native spawn call.
            if(!Regex.IsMatch(step,@"push(?:i\.e|\.i) "+n2EntryIndex+@"\s+conv\.i\.v\s+call\.i instance_destroy")||!Regex.IsMatch(step,@"push(?:i\.e|\.i) "+n2EntryIndex+@"\s+conv\.i\.v(?:\s+.*){4}\s+call\.i instance_create_depth")||!step.Contains("EAO_N1_stage"))throw new InvalidDataException("N2 entrance not gated on the closed bell case.");
            checks.Add("n2-entrance-gated-on-closed-n1-with-native-collision-search");
        }
        return checks.ToArray();
    }
    internal static void Preview(UndertaleData data)
    {
        var layouts=new[]{"r_eao_n1_yard","r_eao_n1_bellhouse","r_eao_n1_underpass","r_eao_n2_camp","r_eao_n2_winch","r_eao_n2_side"}.Select(n=> {var r=data.Rooms.Single(r=>r.Name.Content==n);return new{name=n,title=r.Caption.Content,blocked=r.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>new[]{(int)i.X/26,(int)i.Y/26}).ToArray(),nodes=r.GameObjects.Where(i=>(i.ObjectDefinition.Name.Content.StartsWith("o_eao_n1_")||i.ObjectDefinition.Name.Content.StartsWith("o_eao_n2_"))&&!i.ObjectDefinition.Name.Content.Contains("floor")).Select(i=>new{name=i.ObjectDefinition.Name.Content,x=i.X,y=i.Y}).ToArray()};}).ToArray();
        var html="<!doctype html><meta charset='utf-8'><title>无钟之夜与灰堤 · 场景预览</title><style>body{background:#171f23;color:#eee;font:16px sans-serif;margin:24px}button{padding:10px;margin:5px;background:#4c5551;color:#fff;border:0}canvas{width:min(100%,1040px);image-rendering:pixelated;border:1px solid #777}p{max-width:1000px}</style><h1>无钟之夜与灰堤 · 候选包实际布局</h1><p>断桥、钟房侧通道、暗渠折返与灰堤三景（雇工棚、塌堤绞盘、旧渠侧间）分别重建。灰色为可走格，深色为碰撞格；黄点为剧情交互，绿色为落点。实际光照、鼠标命中与寻路仍须运行验证。</p><nav id='tabs'></nav><h2 id='title'></h2><canvas id='map' width='1040' height='780'></canvas><script>const layouts="+JsonSerializer.Serialize(layouts)+";const c=document.getElementById('map'),g=c.getContext('2d');const bell=new Image();bell.src='../src/EmbersAndOaths/Assets/night-bell-v1.png';function draw(k){let l=layouts[k];document.getElementById('title').textContent=l.title;g.fillStyle='#45504c';g.fillRect(0,0,1040,780);g.fillStyle='#13272c';l.blocked.forEach(p=>g.fillRect(p[0]*26,p[1]*26,26,26));g.strokeStyle='#273a3d';for(let x=0;x<=1040;x+=26){g.beginPath();g.moveTo(x,0);g.lineTo(x,780);g.stroke()}for(let y=0;y<=780;y+=26){g.beginPath();g.moveTo(0,y);g.lineTo(1040,y);g.stroke()}for(let n of l.nodes){if(n.name.includes('bell_art')&&bell.complete)g.drawImage(bell,n.x-52,n.y-130,104,156);g.fillStyle=n.name.includes('start_')?'#8bd58d':'#ffc976';g.fillRect(n.x-4,n.y-4,8,8);g.font='12px sans-serif';g.fillText(n.name.replace('o_eao_n1_','').replace('o_eao_n2_',''),n.x+8,n.y-5)}}layouts.forEach((l,k)=>{let b=document.createElement('button');b.textContent=l.title;b.onclick=()=>draw(k);document.getElementById('tabs').append(b)});bell.onload=()=>draw(0);draw(0);</script>";
        File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","night-layout.html"),"artifacts"),html);
    }
}
