using System.IO;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Models;

// Serialized contracts and actual native input gates; UI behavior is separately
// exercised in GameMaker. No static check is a claim of fullscreen validation.
internal static class EaoDevCoordinateChecks
{
    internal static string[] Validate(UndertaleData data,Func<string,string> asm)
    {
        var checks=new List<string>();
        void Need(bool ok,string name){if(!ok)throw new InvalidDataException(name);checks.Add(name);}
        var input=data.GameObjects.Single(o=>o.Name.Content=="o_eao_dev_coordinates");
        var parent=data.GameObjects.Single(o=>o.Name.Content=="o_confirm_panel");
        var index=data.GameObjects.IndexOf(input);var parentIndex=data.GameObjects.IndexOf(parent);
        bool References(string code,int resource)=>Regex.IsMatch(code,@"push(?:i\.e|\.i) "+resource+@"\b");
        var create=asm("gml_Object_o_eao_dev_coordinates_Create_0");
        var step=asm("gml_Object_o_eao_dev_coordinates_Step_1");
        var submit=asm("gml_Object_o_eao_dev_coordinates_Other_12");
        var cancel=asm("gml_Object_o_eao_dev_coordinates_Other_11");
        var release=asm("gml_Object_o_eao_dev_coordinates_Other_13");
        var destroy=asm("gml_Object_o_eao_dev_coordinates_Destroy_0");
        var cleanup=asm("gml_Object_o_eao_dev_coordinates_CleanUp_0");
        Need(input.ParentId==parent&&input.Sprite==parent.Sprite&&input.Visible&&!input.Persistent,
            "dev-coordinate-editor-inherits-native-confirm-panel-and-sprite");
        Need(new[]{create,step}.All(code=>code.Contains("scr_guiLayoutOffsetUpdate(argc=3)")
            &&code.Contains("global.cameraWidth")&&code.Contains("global.cameraHeight")),
            "dev-coordinate-native-layout-centers-panel-and-child-hit-areas");
        var draw=asm("gml_Object_o_eao_devtools_Draw_0");
        Need(References(draw,index)&&draw.IndexOf("instance_exists",StringComparison.Ordinal)<draw.IndexOf("matrix_build",StringComparison.Ordinal),
            "dev-coordinate-inspection-card-hidden-while-editor-is-open");
        var nativeGate=asm("gml_GlobalScript_can_press");
        Need(Regex.IsMatch(nativeGate,@"push(?:i\.e|\.i) "+parentIndex+@"\s+conv\.i\.v\s+call\.i instance_exists\(argc=1\)")
            &&asm("gml_Object_o_player_Step_0").Contains("call.i gml_Script_can_press(argc=0)")
            &&asm("gml_Object_o_button_actionkey_Create_0").Contains("call.i gml_Script_can_press_gui(argc=7)")
            &&asm("gml_GlobalScript_can_press_gui").Contains("scr_isNearestInstanceDepth")
            &&References(asm("gml_Object_o_confirm_panel_Create_0"),data.GameObjects.IndexOf(data.GameObjects.Single(o=>o.Name.Content=="o_gui_no_click"))),
            "dev-coordinate-native-player-and-focused-gui-gates-preserved");
        Need(create.Contains("event_inherited")&&create.Contains("eao_coord_keyboard_before")
            &&create.Contains("builtin.keyboard_string")&&release.Contains("builtin.keyboard_string")
            &&release.Contains("eao_coord_keyboard_owned")&&release.Contains("eao_coord_released"),
            "dev-coordinate-borrowed-keyboard-buffer-restored-once");
        Need(step.Contains("keyboard_check")&&step.Contains("mouse_check_button")
            &&step.Contains("eao_coord_closing")&&step.Contains("eao_coord_armed")
            &&step.Contains("instance_destroy")&&submit.Contains("eao_coord_closing"),
            "dev-coordinate-modal-waits-for-trigger-release-before-close");
        Need(submit.Contains("builtin.keyboard_string")&&!submit.Contains("string_copy")
            &&step.Contains("string_copy")&&step.Contains("local._shown"),
            "dev-coordinate-validates-full-text-and-only-shortens-display");
        Need(submit.Contains("dev_coord_submitting")&&submit.Contains("dev_coord_text")
            &&submit.Contains("dev_coord_error")&&cancel.Contains("eao_coord_queued")
            &&cancel.Contains("eao_coord_character")&&cancel.Contains("global.characterDataMap")
            &&References(cancel,data.GameObjects.IndexOf(data.GameObjects.Single(o=>o.Name.Content=="o_smoothRoomChanger"))),
            "dev-coordinate-submit-and-cancel-have-owned-request-fields");
        var execute=asm("gml_Object_o_eao_controller_Other_13");
        var click=asm("gml_Object_o_globalmapInteractiveNormal_Other_20");
        Need(References(execute,index)&&References(click,index)
            &&execute.IndexOf("instance_exists",StringComparison.Ordinal)<execute.IndexOf("scr_smoothRoomChange",StringComparison.Ordinal),
            "dev-coordinate-executor-and-map-click-wait-for-modal");
        Need(destroy.Contains("scr_guiContainerDestroy")&&destroy.Contains("event_user")
            &&cleanup.Contains("event_inherited")&&release.Contains("scr_escapeButtonListRemove")
            &&release.Contains("instance_destroy"),
            "dev-coordinate-native-gui-and-escape-list-cleanup-on-destroy-and-room-end");
        var all=string.Join("\n",new[]{create,step,submit,cancel,release,destroy,cleanup});
        Need(!new[]{"get_string","get_integer","keyboard_clear","keyboard_set_map","scr_atr_set","room_goto","ds_list_clear"}.Any(all.Contains)
            &&!Regex.IsMatch(all,@"pop\.\w+\.\w+ (?:self|global|\[stacktop\]self)\.(?:can_move|lock_turn|lock_movement|playerGridX|playerGridY|HP)\b"),
            "dev-coordinate-no-os-dialog-player-lock-health-or-world-coordinate-writes");
        var reset=asm("gml_Object_o_eao_devtools_Other_10");
        Need(References(reset,index)&&reset.Contains("instance_destroy")
            &&new[]{116,118,120,121,122}.All(k=>References(asm("gml_Object_o_eao_devtools_KeyPress_"+k),index)),
            "dev-coordinate-f6-closes-editor-and-other-dev-hotkeys-stay-modal");
        return checks.ToArray();
    }
}
