using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Models;

internal static class EaoSceneAssembly
{
    internal static string[] Validate(UndertaleData data,Func<string,string> asm)
    {
        var checks=new List<string>();
        void Require(bool ok,string message){if(!ok)throw new InvalidDataException(message);checks.Add(message);}
        using var doc=JsonDocument.Parse(File.ReadAllText(Path.Combine(ProjectPaths.Root(),"src/Art/native-n2-built-v1/layout.json")));
        var layout=doc.RootElement;var hub=data.Rooms.Single(r=>r.Name.Content==layout.GetProperty("room").GetString());
        var columns=layout.GetProperty("columns").GetInt32();var rows=layout.GetProperty("rows").GetInt32();
        var cells=new HashSet<(int,int)>();
        foreach(var r in layout.GetProperty("walkable_rectangles").EnumerateArray())
            for(var x=r[0].GetInt32();x<=r[2].GetInt32();x++)for(var y=r[1].GetInt32();y<=r[3].GetInt32();y++)cells.Add((x,y));
        foreach(var b in layout.GetProperty("buildings").EnumerateArray()) {
            var r=b.GetProperty("blocked");
            for(var x=r[0].GetInt32();x<=r[2].GetInt32();x++)for(var y=r[1].GetInt32();y<=r[3].GetInt32();y++)cells.Remove((x,y));
        }
        var walls=hub.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
        Require(hub.Width==columns*26&&hub.Height==rows*26&&Enumerable.Range(0,columns).All(x=>Enumerable.Range(0,rows).All(y=>walls.Contains((x,y))!=cells.Contains((x,y)))),"scene-exterior-serialized-collision-matches-independent-footprints");
        var reached=new HashSet<(int,int)>();var queue=new Queue<(int,int)>();queue.Enqueue(cells.First());
        while(queue.Count>0){var p=queue.Dequeue();if(!cells.Contains(p)||!reached.Add(p))continue;foreach(var d in new[]{(1,0),(-1,0),(0,1),(0,-1)})queue.Enqueue((p.Item1+d.Item1,p.Item2+d.Item2));}
        Require(reached.Count==cells.Count,"scene-exterior-all-floor-cells-connected");
        void Placement(UndertaleRoom r,string name,JsonElement cell) {
            var x=cell[0].GetInt32()*26+13;var y=cell[1].GetInt32()*26+13;
            Require(r.GameObjects.Count(i=>i.ObjectDefinition.Name.Content==name&&i.X==x&&i.Y==y)==1,"scene-unique-placement-"+name);
            var nativeWalls=r.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
            Require(!nativeWalls.Contains((x/26,y/26)),"scene-accessible-anchor-"+name);
        }
        void Door(string name,string room,string tag) {
            var obj=data.GameObjects.Single(o=>o.Name.Content==name);var code=asm("gml_Object_"+name+"_Create_0");
            var target=data.Rooms.IndexOf(data.Rooms.Single(r=>r.Name.Content==room));
            var sprite=obj.Sprite;
            Require(obj.ParentId?.Name.Content=="o_Doors_all_small"&&sprite?.Name.Content=="s_eao_scene_door_anchor"&&obj.Events[(int)EventType.Mouse].Count==0&&obj.Events[(int)EventType.Other].Count==0&&Regex.IsMatch(code,@"push(?:i\.e|\.i) "+target+@"\s+pop\.v\.i self.target")&&code.Contains(tag)&&code.Contains("scr_locationRoomEntityInitSavable"),"scene-native-door-target-and-tag-"+name);
            var native=obj.ParentId!.Sprite;
            Require(sprite!.OriginX==sprite.Width/2&&sprite.OriginY==sprite.Height/2&&sprite.Width==native.Width&&sprite.Height==native.Height&&sprite.Textures.Count==native.Textures.Count&&sprite.Textures.Zip(native.Textures).All(p=>p.First.Texture==p.Second.Texture)&&sprite.CollisionMasks.Count==native.CollisionMasks.Count&&sprite.CollisionMasks.Zip(native.CollisionMasks).All(p=>p.First.Data.SequenceEqual(p.Second.Data)),"scene-door-centred-interaction-anchor-reuses-native-pixels-"+name);
        }
        foreach(var b in layout.GetProperty("buildings").EnumerateArray()) {
            var id=b.GetProperty("id").GetString()!;
            Placement(hub,"o_eao_site_building_"+id,b.GetProperty("door_cell"));
            Placement(hub,"o_eao_site_door_"+id,b.GetProperty("door_cell"));
            Placement(hub,"o_eao_site_start_"+id,b.GetProperty("return_cell"));
            Door("o_eao_site_door_"+id,b.GetProperty("target").GetString()!,b.GetProperty("tag").GetString()!);
            Require(asm("gml_Object_o_eao_site_start_"+id+"_Create_0").Contains(b.GetProperty("return_tag").GetString()!),"scene-return-marker-"+id);
            var inst=hub.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_eao_site_building_"+id);var sprite=inst.ObjectDefinition.Sprite!;
            Require(inst.X-sprite.OriginX>=0&&inst.Y-sprite.OriginY>=0&&inst.X-sprite.OriginX+sprite.Width<=hub.Width&&inst.Y-sprite.OriginY+sprite.Height<=hub.Height,"scene-building-bounds-"+id);
        }
        var pi=hub.GameObjects.IndexOf(hub.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_abstract_player"));
        Require(hub.GameObjects.Where(i=>i.ObjectDefinition.Name.Content.StartsWith("o_eao_site_start_")).All(i=>hub.GameObjects.IndexOf(i)<pi),"scene-exterior-arrival-markers-before-native-player");
        foreach(var d in layout.GetProperty("interior_returns").EnumerateArray()) {
            var name=d.GetProperty("object").GetString()!;Placement(data.Rooms.Single(r=>r.Name.Content==d.GetProperty("room").GetString()),name,d.GetProperty("cell"));
            Door(name,hub.Name.Content,d.GetProperty("tag").GetString()!);
            Require(!asm("gml_Object_"+name+"_Alarm_7").Contains("scr_atr_set_simple"),"scene-interior-return-does-not-write-world-coordinates-"+name);
        }
        foreach(var p in layout.GetProperty("props").EnumerateArray()) {
            var name="o_eao_site_"+p.GetProperty("id").GetString();
            Placement(data.Rooms.Single(r=>r.Name.Content==p.GetProperty("room").GetString()),name,p.GetProperty("cell"));
            var obj=data.GameObjects.Single(o=>o.Name.Content==name);
            Require(obj.ParentId==null&&obj.Events[(int)EventType.Mouse].Count==0&&!obj.Solid&&!p.GetProperty("blocking").GetBoolean(),"scene-nonblocking-scenery-"+name);
        }
        Door("o_eao_n2_entry",hub.Name.Content,"EAO_SITE_in");
        Placement(hub,"o_eao_site_home",layout.GetProperty("home_cell"));
        Require(asm("gml_Object_o_eao_site_home_Alarm_7").Contains("scr_atr_set_simple")&&asm("gml_Object_o_eao_site_home_Step_0").Contains("EAO_N1_origin_room"),"scene-exterior-home-restores-native-world-return");
        Require(!data.Code.Where(c=>c.ParentEntry==null&&c.Name.Content.StartsWith("gml_Object_o_eao_site_")).Any(c=>new[]{"call.i room_goto","scr_gold","EAO_resolve","EAO_encountered"}.Any(asm(c.Name.Content).Contains)),"scene-assembly-no-quest-reward-or-direct-room-writes");
        return checks.ToArray();
    }
}
