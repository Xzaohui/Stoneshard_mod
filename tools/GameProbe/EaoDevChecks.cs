using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Decompiler;

internal static class EaoDevChecks
{
    internal static string[] Validate(UndertaleData data)
    {
        var checks=new List<string>();
        void Require(bool ok,string message){if(!ok)throw new InvalidDataException(message);checks.Add(message);}
        string Asm(string name){var c=data.Code.Single(c=>c.Name.Content==name);return c.Disassemble(data.Variables,data.CodeLocals.For(c));}
        var dev=data.GameObjects.Single(o=>o.Name.Content=="o_eao_devtools");
        Require(dev.Persistent&&dev.Visible,"dev-persistent-visible-controller");
        Require(Asm("gml_Object_o_eao_devtools_Draw_0").Contains("draw_text")&&Asm("gml_Object_o_eao_devtools_Draw_0").Contains("matrix_set"),"dev-panel-world-pass-restores-transform");
        Require(dev.Events[(int)EventType.KeyPress].Select(e=>e.EventSubtype).Order().SequenceEqual(new uint[]{116,117,118,120,121,122}),"dev-f6-f7-f9-f10-f11-wired");
        Require(Asm("gml_Object_o_eao_controller_Create_0").Contains("instance_create_depth"),"dev-boot-creation");
        var create=Asm("gml_Object_o_eao_devtools_Create_0");
        Require(Regex.IsMatch(create,@"pushi\.e 0\s+pop\.v\.[bi] global.EAO_dev_enabled"),"dev-default-off");
        var reset=Asm("gml_Object_o_eao_devtools_Other_10");
        var step=Asm("gml_Object_o_eao_devtools_Step_2");
        Require(reset.Contains("dev_fog_before")&&reset.Contains("global.fog")&&reset.Contains("EAO_dev_visible_before")&&step.Contains("dev_character_map"),"dev-fog-restored-on-disable-and-character-change");
        var visit=Asm("gml_Object_o_eao_devtools_KeyPress_122");
        Require(new[]{"scr_getAgredMobsCount","ds_list_empty","scr_unitTurnGetTime","EAO_N1_origin_room","event_perform"}.All(visit.Contains),"dev-native-visit-combat-lock-dialogue-return-gates");
        var portal=data.GameObjects.Single(o=>o.Name.Content=="o_eao_dev_portal");
        var alarm=Asm("gml_Object_o_eao_dev_portal_Alarm_7");
        Require(portal.ParentId?.Name.Content=="o_Doors_all_small"&&alarm.Contains("event_inherited")&&alarm.Contains("scr_atr_set_simple"),"dev-visit-through-native-door-alarm");
        var panel=Asm("gml_Object_o_eao_devtools_Draw_0");
        Require(panel.Contains("global.language")&&panel.Contains("F5 面板")&&panel.Contains("F5 panel"),"dev-panel-localized-chinese-and-english");
        var doorDraw=Asm("gml_Object_o_eao_fx_back_Draw_0");
        Require(new[]{"sprite_get_width","sprite_get_height","sprite_get_xoffset","sprite_get_yoffset","event_inherited"}.All(doorDraw.Contains),"scene-door-art-aligns-native-origin-and-retains-highlight");
        var quarry=data.Rooms.Single(r=>r.Name.Content=="r_eao_fx_quarry");
        var arrival=quarry.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_eao_fx_start_in");
        var player=quarry.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_abstract_player");
        var back=quarry.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_eao_fx_back");
        var quarryWalls=quarry.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
        var ax=(int)arrival.X/26;var ay=(int)arrival.Y/26;
        Require(player.X==arrival.X&&player.Y==arrival.Y&&Math.Abs(arrival.X-back.X)+Math.Abs(arrival.Y-back.Y)>=52&&new[]{(ax,ay),(ax-1,ay),(ax+1,ay),(ax,ay-1),(ax,ay+1)}.All(p=>!quarryWalls.Contains(p)),"scene-quarry-arrival-clear-of-return-door-with-four-walkable-neighbors");
        var all=data.Code.Where(c=>c.ParentEntry==null&&c.Name.Content.StartsWith("gml_Object_o_eao_dev")).Select(c=>Asm(c.Name.Content)).ToArray();
        var forbidden=new[]{"call.i room_goto","call.i room_restart","scr_globalmapFogUpdate","scr_globalmapFogSave","scr_quest_get_complete","EAO_N1_stage","EAO_N1_plan","scr_gold","ds_grid_set"};
        Require(!all.Any(c=>forbidden.Any(c.Contains)),"dev-no-quest-reward-exploration-grid-or-direct-room-writes");
        using var manifest=JsonDocument.Parse(File.ReadAllText(Path.Combine(ProjectPaths.Root(),"src/Art/hd2d_26x26_20261013/manifest.json")));
        var sources=manifest.RootElement.GetProperty("assets").EnumerateArray().ToDictionary(a=>a.GetProperty("id").GetString()!);
        foreach(var source in manifest.RootElement.GetProperty("n1_surface_repair").GetProperty("source_sha256").EnumerateObject()) {
            var hash=Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),source.Name))));
            Require(hash.Equals(source.Value.GetString(),StringComparison.OrdinalIgnoreCase),"n1-surface-source-"+source.Name);
        }
        checks.AddRange(EaoN1SurfaceChecks.Validate(data,manifest.RootElement));
        foreach(var source in manifest.RootElement.GetProperty("n1_architecture_repair").GetProperty("source_sha256").EnumerateObject()) {
            var hash=Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),source.Name))));
            Require(hash.Equals(source.Value.GetString(),StringComparison.OrdinalIgnoreCase),"n1-architecture-source-"+source.Name);
        }
        checks.AddRange(EaoN1SurfaceChecks.ValidateArchitecture(data,manifest.RootElement));
        using var n2Manifest=JsonDocument.Parse(File.ReadAllText(Path.Combine(ProjectPaths.Root(),"src/Art/native-n2-hd2d-v1/manifest.json")));
        foreach(var source in n2Manifest.RootElement.GetProperty("source_sha256").EnumerateObject()) {
            var hash=Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),source.Name))));
            Require(hash.Equals(source.Value.GetString(),StringComparison.OrdinalIgnoreCase),"n2-art-source-"+source.Name);
        }
        foreach(var scene in n2Manifest.RootElement.GetProperty("scenes").EnumerateArray()) {
            var room=data.Rooms.Single(r=>r.Name.Content==scene.GetProperty("room").GetString());
            var cells=new HashSet<(int,int)>();
            foreach(var rect in scene.GetProperty("walkable_rectangles").EnumerateArray())
                for(var x=rect[0].GetInt32();x<=rect[2].GetInt32();x++) for(var y=rect[1].GetInt32();y<=rect[3].GetInt32();y++) cells.Add((x,y));
            var walls=room.GameObjects.Where(o=>o.ObjectDefinition.Name.Content=="o_hut_wall").Select(o=>((int)o.X/26,(int)o.Y/26)).ToHashSet();
            Require(Enumerable.Range(0,40).All(x=>Enumerable.Range(0,30).All(y=>walls.Contains((x,y))!=cells.Contains((x,y)))),room.Name.Content+"-art-matches-serialized-native-collision-cells");
        }
        foreach(var a in n2Manifest.RootElement.GetProperty("assets").EnumerateArray()) sources.Add(a.GetProperty("id").GetString()!,a);
        using var builtManifest=JsonDocument.Parse(File.ReadAllText(Path.Combine(ProjectPaths.Root(),"src/Art/native-n2-built-v1/manifest.json")));
        foreach(var source in builtManifest.RootElement.GetProperty("source_sha256").EnumerateObject()) {
            var hash=Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),source.Name))));
            Require(hash.Equals(source.Value.GetString(),StringComparison.OrdinalIgnoreCase),"scene-art-source-"+source.Name);
        }
        foreach(var a in builtManifest.RootElement.GetProperty("assets").EnumerateArray()) sources.Add(a.GetProperty("id").GetString()!,a);
        using var n1Doors=JsonDocument.Parse(File.ReadAllText(Path.Combine(ProjectPaths.Root(),"src/Art/native-n1-doorways-v1/manifest.json")));
        foreach(var source in n1Doors.RootElement.GetProperty("source_sha256").EnumerateObject()) {
            var hash=Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),source.Name))));
            Require(hash.Equals(source.Value.GetString(),StringComparison.OrdinalIgnoreCase),"n1-doorway-art-source-"+source.Name);
        }
        var n1DoorIds=n1Doors.RootElement.GetProperty("assets").EnumerateArray().Select(a=>a.GetProperty("id").GetString()!).ToHashSet();
        foreach(var a in n1Doors.RootElement.GetProperty("assets").EnumerateArray()) sources.Add(a.GetProperty("id").GetString()!,a);
        var sprites=data.Sprites.Where(s=>s.Name.Content.StartsWith("s_eao_hd2d_")).ToArray();
        Require(sprites.Length==51,"hd2d-fifty-one-native-sprites");
        foreach(var sprite in sprites){
            var id=sprite.Name.Content["s_eao_hd2d_".Length..];var source=sources[id];
            var dimensions=source.GetProperty("size").EnumerateArray().Select(v=>v.GetInt32()).ToArray();
            Require(sprite.Width==dimensions[0]&&sprite.Height==dimensions[1],id+"-dimensions");
            var origin=source.TryGetProperty("sprite_origin",out var p)?p:source.GetProperty("origin");
            Require(sprite.OriginX==origin[0].GetInt32()&&sprite.OriginY==origin[1].GetInt32(),id+"-origin");
            var folder=n1DoorIds.Contains(id)?"src/Art/native-n1-doorways-v1":id.StartsWith("n2site_")?"src/Art/native-n2-built-v1":id.StartsWith("r_eao_n2_")||id.StartsWith("r01_")?"src/Art/native-n2-hd2d-v1":"src/Art/hd2d_26x26_20261013";
            var expected=File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),folder,source.GetProperty("path").GetString()!));
            var actual=sprite.Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray();
            Require(actual.SequenceEqual(expected),id+"-embedded-png-bytes");
        }
        Require(Asm("gml_Object_o_eao_n1_floor_Draw_0").Contains("global.EAO_dev_art")&&Asm("gml_Object_o_eao_devtools_Draw_0").Contains("astar_get_cell"),"hd2d-toggle-and-live-collision-grid");
        var n2Rooms=new[]{"r_eao_n2_camp","r_eao_n2_winch","r_eao_n2_side"}.Select(n=>data.Rooms.IndexOf(data.Rooms.Single(r=>r.Name.Content==n))).ToArray();
        bool References(string asm,int index)=>Regex.IsMatch(asm,@"push(?:i\.e|\.i) "+index+@"\b");
        Require(n2Rooms.All(i=>References(visit,i))&&new[]{"EAO_N2_camp_in","EAO_N2_winch_in","EAO_N2_side_in"}.All(visit.Contains),"dev-six-scene-native-cycle-with-n2-arrival-tags");
        Require(n2Rooms.All(i=>References(alarm,i)),"dev-n2-cycle-preserves-first-origin");
        Require(Asm("gml_Object_o_eao_n2_floor_Draw_0").Contains("global.EAO_dev_art"),"n2-floor-visual-toggle-keeps-native-fallback");
        foreach(var id in new[]{"coffin","winch"}) Require(Asm("gml_Object_o_eao_n2_"+id+"_Draw_0").Contains("event_inherited"),"n2-"+id+"-art-keeps-native-draw-fallback");
        using var style=JsonDocument.Parse(File.ReadAllText(Path.Combine(ProjectPaths.Root(),"src/Art/native-n2-hd2d-v1/interior-style-layout.json")));
        var floorAsm=Asm("gml_Object_o_eao_n2_floor_Draw_0");
        Require(Regex.IsMatch(Asm("gml_Object_o_eao_n2_floor_Create_0"),@"pushi\.e 100\s+pop\.v\.[iv] self.depth"),"n2-architectural-stamps-use-background-depth");
        var drainScene=n2Manifest.RootElement.GetProperty("scenes").EnumerateArray().Single(s=>s.GetProperty("room").GetString()=="r_eao_n2_winch");
        Require(drainScene.GetProperty("water_sampling").GetString()=="whole-basin"&&drainScene.GetProperty("water_rectangles").GetArrayLength()==3,"n2-winch-whole-basin-water-contract");
        var cloth=data.Sprites.Single(s=>s.Name.Content=="s_eao_hd2d_n2site_r01_shelter_bedroll");
        foreach(var name in new[]{"camp_bedroll_a","camp_bedroll_b","side_bedroll"}) {
            var obj=data.GameObjects.Single(o=>o.Name.Content=="o_eao_site_"+name);
            Require(obj.Sprite==cloth&&!obj.Solid&&obj.ParentId==null&&Regex.IsMatch(Asm("gml_Object_"+obj.Name.Content+"_Create_0"),@"pushi\.e 1\s+pop\.v\.[iv] self.depth"),"n2-bedroll-floor-depth-and-sprite-"+name);
        }
        var frameIndex=data.Sprites.IndexOf(data.Sprites.Single(s=>s.Name.Content=="s_eao_hd2d_r01_doorway_open"));
        var frameCount=0;
        foreach(var scene in style.RootElement.GetProperty("scenes").EnumerateArray()) {
            var room=data.Rooms.Single(r=>r.Name.Content==scene.GetProperty("room").GetString());
            foreach(var stamp in scene.GetProperty("doors").EnumerateArray()) {
                var name=stamp.GetProperty("object").GetString()!;
                var x=stamp.GetProperty("cell")[0].GetInt32()*26+13;
                var y=stamp.GetProperty("cell")[1].GetInt32()*26+13;
                Require(room.GameObjects.Count(i=>i.ObjectDefinition.Name.Content==name&&i.X==x&&i.Y==y)==1,"n2-doorway-art-matches-native-anchor-"+name);
                var obj=data.GameObjects.Single(o=>o.Name.Content==name);
                var draw=Asm("gml_Object_"+name+"_Draw_0");
                Require(obj.ParentId?.Name.Content=="o_Doors_all_small"&&obj.Sprite?.Name.Content=="s_eao_scene_door_anchor"&&obj.Events[(int)EventType.Mouse].Count==0&&draw.Contains("event_inherited")&&draw.Contains("scr_cursor_get_pointed_instance")&&draw.Contains("string_width")&&draw.Contains("string_height")&&draw.Contains("bbox_top")&&References(draw,frameIndex)&&Regex.Matches(draw,@"pop\.v\.\w+ self\.sprite_index\b").Count==2&&Regex.Matches(draw,@"pop\.v\.\w+ self\.shaderHighlight\b").Count==2&&draw.Contains("self.shaderHighlight")&&!draw.Contains("self.sprlight")&&!new[]{"lock_movement","scr_smoothRoomChange","room_goto","scr_atr_set_simple"}.Any(draw.Contains),"n2-doorway-native-interaction-and-contextual-label-"+name);
                // MSL's compiler converts integer draw arguments to variants.
                var variant=@"\s+conv\.i\.v\s+";
                var pattern=@"push(?:i\.e|\.i) "+y+variant+@"push(?:i\.e|\.i) "+x+variant+@"pushi\.e 0"+variant+@"push(?:i\.e|\.i) "+frameIndex+variant+@"call\.i draw_sprite\(argc=4\)";
                Require(Regex.IsMatch(floorAsm,pattern),"n2-doorway-stamp-in-floor-pass-"+name);
                frameCount++;
            }
        }
        Require(frameCount==7&&Regex.Matches(floorAsm,@"push(?:i\.e|\.i) "+frameIndex+@"\b").Count==frameCount,"n2-seven-doorway-stamps-below-characters");
        checks.AddRange(EaoDoorwayHitChecks.Validate(data,Asm));
        checks.AddRange(EaoN1DoorwayChecks.Validate(data,Asm,n1Doors.RootElement));
        checks.AddRange(EaoSceneAssembly.Validate(data,Asm));
        return checks.ToArray();
    }
}
