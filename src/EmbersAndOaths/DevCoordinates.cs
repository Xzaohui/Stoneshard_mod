using System;
using ModShardLauncher;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// The native confirm-panel parent blocks can_press and owns focused GUI input.
// Only this child and its borrowed text buffer are changed; no player locks.
internal static class DevCoordinates
{
    internal static void Prepare()
    {
        var parent=Msl.GetObject("o_confirm_panel");
        var input=Msl.AddObject("o_eao_dev_coordinates",parentName:"o_confirm_panel",isVisible:true);
        input.ParentId=parent; input.Sprite=parent.Sprite;
        input.Visible=true; input.Persistent=false;
    }

    internal static void Configure(Action<UndertaleGameObject,string,EventType,uint> set,ModFile files)
    {
        var input=Msl.GetObject("o_eao_dev_coordinates");
        set(input,files.GetCode("dev_coordinates_create.gml"),EventType.Create,0);
        set(input,files.GetCode("dev_coordinates_step.gml"),EventType.Step,1);
        set(input,files.GetCode("dev_coordinates_submit.gml"),EventType.Other,12);
        set(input,files.GetCode("dev_coordinates_cancel.gml"),EventType.Other,11);
        set(input,files.GetCode("dev_coordinates_release.gml"),EventType.Other,13);
        // Native confirm-panel Destroy also writes floor-target can_move=true.
        // Keep its GUI cleanup without that unrelated control-flag write.
        set(input,"event_user(3); scr_guiContainerDestroy();",EventType.Destroy,0);
        set(input,"event_user(3); event_inherited();",EventType.CleanUp,0);
    }
}
