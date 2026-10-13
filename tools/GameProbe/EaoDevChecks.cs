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
        Require(dev.Events[(int)EventType.KeyPress].Select(e=>e.EventSubtype).Order().SequenceEqual(new uint[]{117,118,120,121,122}),"dev-f6-f7-f9-f10-f11-wired");
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
        var sprites=data.Sprites.Where(s=>s.Name.Content.StartsWith("s_eao_hd2d_")).ToArray();
        Require(sprites.Length==16,"hd2d-sixteen-native-sprites");
        foreach(var sprite in sprites){
            var id=sprite.Name.Content["s_eao_hd2d_".Length..];var source=sources[id];
            var dimensions=source.GetProperty("size").EnumerateArray().Select(v=>v.GetInt32()).ToArray();
            Require(sprite.Width==dimensions[0]&&sprite.Height==dimensions[1],id+"-dimensions");
            var origin=source.TryGetProperty("sprite_origin",out var p)?p:source.GetProperty("origin");
            Require(sprite.OriginX==origin[0].GetInt32()&&sprite.OriginY==origin[1].GetInt32(),id+"-origin");
            var expected=File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),"src/Art/hd2d_26x26_20261013",source.GetProperty("path").GetString()!));
            var actual=sprite.Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray();
            Require(actual.SequenceEqual(expected),id+"-embedded-png-bytes");
        }
        Require(Asm("gml_Object_o_eao_n1_floor_Draw_0").Contains("global.EAO_dev_art")&&Asm("gml_Object_o_eao_devtools_Draw_0").Contains("astar_get_cell"),"hd2d-toggle-and-live-collision-grid");
        return checks.ToArray();
    }
}
