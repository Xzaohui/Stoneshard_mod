using System.IO;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Decompiler;

internal static class EaoTestTeleport
{
    public static string[] Validate(UndertaleData data)
    {
        string Asm(string name) { var c=data.Code.Single(c=>c.Name.Content==name); return c.Disassemble(data.Variables,data.CodeLocals.For(c)); }
        var controller=data.GameObjects.Single(o=>o.Name.Content=="o_eao_controller");
        if(!controller.Visible) throw new InvalidDataException("F8 map status Draw GUI is disabled.");
        if(!controller.Events[(int)EventType.KeyPress].Any(e=>e.EventSubtype==119)) throw new InvalidDataException("F8 switch missing.");
        var toggle=Asm("gml_Object_o_eao_controller_KeyPress_119");
        var setup=Asm("gml_Object_o_eao_controller_Other_12");
        var click=Asm("gml_Object_o_globalmapInteractiveNormal_Other_20");
        var execute=Asm("gml_Object_o_eao_controller_Other_13");
        var commit=Asm("gml_Object_o_smoothRoomChanger_Other_20");
        var arrival=Asm("gml_Object_o_eao_controller_Step_2");
        if(!arrival.Contains("scr_water_full_filter")) throw new InvalidDataException("Teleport arrival admits swimming instead of dry ground.");
        var waterId=data.GameObjects.IndexOf(data.GameObjects.Single(o=>o.Name.Content=="o_water_grid"));
        if(!arrival.Contains("pushi.e "+waterId) || arrival.IndexOf("pushi.e "+waterId,StringComparison.Ordinal)>arrival.IndexOf("scr_water_full_filter",StringComparison.Ordinal) || !Asm("gml_Object_o_water_grid_Alarm_0").Contains("self.waterGrid")) throw new InvalidDataException("Arrival must wait for native water markers before dry-ground lookup.");
        foreach(var (asm,words) in new[]{(toggle,new[]{"EAO_test_teleport_enabled","EAO_test_map_pending","scr_actionsLogAddMessage"}),(setup,new[]{"EAO_test_map_schema","scr_guiInteractiveStateUpdate","scr_guiInteractiveEventUpdate"}),(click,new[]{"guiInteractiveState","mapScale","mapOffsetX","mapOffsetY","guiMouseX","guiMouseY","floor","scr_globaltile_get_room","scr_globalmapIsBorder","event_user"}),(execute,new[]{"scr_smoothRoomChange","@@NewGMLArray@@","ds_list_empty","scr_unitTurnGetTime","scr_getAgredMobsCount","event_user","EAO_test_map_commit"}),(commit,new[]{"global.playerGridX","global.playerGridY","scr_atr_set_simple","\"NA\"","EAO_test_map_arrival","EAO_test_map_restore"}),(arrival,new[]{"astar_get_cell","scr_check_collision_not_enemy_around","scr_tile_mark_get_instance","newgrid","EAO_test_map_arrival","scr_smoothRoomChange"})}) {
            foreach(var word in words) if(!asm.Contains(word)) throw new InvalidDataException("Map teleport interface missing: "+word);
        }
        foreach(var asm in new[]{setup,click,execute,toggle,commit,arrival}) {
            foreach(var forbidden in new[]{"call.i room_goto", "call.i room_restart", "skill_can_cast", "mouse_clear", "scr_free_tile_array", "o_eao_test_guide"}) if(asm.Contains(forbidden)) throw new InvalidDataException("Retired guide or custom input/room transition: "+forbidden);
            // Only the explicit F8 KeyPress event may inspect modifier keys;
            // map click/transition handlers must never poll world input.
            if(asm!=toggle&&asm.Contains("keyboard_check")) throw new InvalidDataException("Input polling outside the developer F8 key event.");
        }
        var abstractId=data.GameObjects.IndexOf(data.GameObjects.Single(o=>o.Name.Content=="o_abstract_player"));
        var fastId=data.GameObjects.IndexOf(data.GameObjects.Single(o=>o.Name.Content=="o_fastTurnController"));
        if(!Asm("gml_Object_o_biome_generation_controller_Other_25").Contains("pushi.e "+abstractId) || !Asm("gml_Object_o_abstract_player_Alarm_0").Contains("pushi.e "+fastId) || !Asm("gml_Object_o_fastTurnController_Alarm_0").Contains("scr_createPlayer")) throw new InvalidDataException("Native delayed outdoor player creation changed.");
        if(controller.Events[(int)EventType.Step].Single(e=>e.EventSubtype==2).Actions.Single().CodeId.Name.Content!="gml_Object_o_eao_controller_Step_2") throw new InvalidDataException("Arrival must run in End Step before the next native spawn alarm.");
        var executeCode=data.Code.Single(c=>c.Name.Content=="gml_Object_o_eao_controller_Other_13");
        var args=executeCode.Instructions.ToList();
        var arrayIndex=args.FindIndex(i=>i.Function?.Target?.Name.Content=="@@NewGMLArray@@");
        if(arrayIndex<4 || Convert.ToInt32(args[arrayIndex-2].Value)!=4 || Convert.ToInt32(args[arrayIndex-4].Value)!=10) throw new InvalidDataException("Source saver must run before coordinate commit.");
        foreach(var (name,codeName) in new[]{("o_globalmapInteractiveNormal","gml_Object_o_globalmapInteractiveNormal_Other_20"),("o_smoothRoomChanger","gml_Object_o_smoothRoomChanger_Other_20")}) {
            var obj=data.GameObjects.Single(o=>o.Name.Content==name);
            if(obj.Events[(int)EventType.Other].Single(e=>e.EventSubtype==20).Actions.Single().CodeId.Name.Content!=codeName) throw new InvalidDataException("Map bridge event not wired.");
        }
        var guide=data.GameObjects.SingleOrDefault(o=>o.Name.Content=="o_eao_test_guide");
        if(guide!=null && (guide.Visible || !Asm("gml_Object_o_eao_test_guide_Create_0").Contains("instance_destroy"))) throw new InvalidDataException("Legacy guide is still active.");
        return new[]{"f8-toggle-default-off-and-legacy-guide-retired","native-focused-left-click-with-pan-zoom-coordinate-conversion","native-right-mark-middle-drag-and-wheel-fallback","source-saver-before-world-coordinate-commit-and-native-arrival","invalid-tile-combat-dungeon-turn-and-transition-gates"};
    }
}
