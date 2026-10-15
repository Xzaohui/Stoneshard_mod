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
        var all=data.Code.Where(c=>c.ParentEntry==null&&c.Name.Content.StartsWith("gml_Object_o_eao_dev")).Select(c=>Asm(c.Name.Content)).ToArray();
        var forbidden=new[]{"call.i room_goto","call.i room_restart","scr_globalmapFogUpdate","scr_globalmapFogSave","scr_quest_get_complete","EAO_N1_stage","EAO_N1_plan","scr_gold","ds_grid_set"};
        Require(!all.Any(c=>forbidden.Any(c.Contains)),"dev-no-quest-reward-exploration-grid-or-direct-room-writes");
        using var manifest=JsonDocument.Parse(File.ReadAllText(Path.Combine(ProjectPaths.Root(),"src/Art/hd2d_26x26_20261013/manifest.json")));
        var sources=manifest.RootElement.GetProperty("assets").EnumerateArray().ToDictionary(a=>a.GetProperty("id").GetString()!);
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
        var sprites=data.Sprites.Where(s=>s.Name.Content.StartsWith("s_eao_hd2d_")).ToArray();
        Require(sprites.Length==47,"hd2d-forty-seven-native-sprites");
        foreach(var sprite in sprites){
            var id=sprite.Name.Content["s_eao_hd2d_".Length..];var source=sources[id];
            var dimensions=source.GetProperty("size").EnumerateArray().Select(v=>v.GetInt32()).ToArray();
            Require(sprite.Width==dimensions[0]&&sprite.Height==dimensions[1],id+"-dimensions");
            var origin=source.TryGetProperty("sprite_origin",out var p)?p:source.GetProperty("origin");
            Require(sprite.OriginX==origin[0].GetInt32()&&sprite.OriginY==origin[1].GetInt32(),id+"-origin");
            var folder=id.StartsWith("n2site_")?"src/Art/native-n2-built-v1":id.StartsWith("r_eao_n2_")||id.StartsWith("r01_")?"src/Art/native-n2-hd2d-v1":"src/Art/hd2d_26x26_20261013";
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
        checks.AddRange(EaoSceneAssembly.Validate(data,Asm));
        return checks.ToArray();
    }
}
