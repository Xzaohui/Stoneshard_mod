using System;
using ModShardLauncher;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

internal static class DevTools
{
    internal static void Prepare()
    {
        Hd2dArt.Ensure();
        N2Hd2dArt.Ensure();
        FieldQuest.Ensure();
        Msl.AddObject("o_eao_devtools",isVisible:true,isPersistent:true);
        var portal=Msl.AddObject("o_eao_dev_portal",parentName:"o_Doors_all_small",isVisible:false);
        portal.ParentId=Msl.GetObject("o_Doors_all_small");portal.Sprite=Msl.GetObject("o_Doors_all_small").Sprite;
    }
    internal static void Configure(Action<UndertaleGameObject,string,EventType,uint> set,ModFile files)
    {
        var dev=Msl.GetObject("o_eao_devtools");dev.Visible=true;dev.Persistent=true;
        set(dev,files.GetCode("dev_create.gml"),EventType.Create,0);
        set(dev,files.GetCode("dev_step.gml"),EventType.Step,2);
        set(dev,files.GetCode("dev_reset.gml"),EventType.Other,10);
        set(dev,"event_user(0);",EventType.CleanUp,0);
        set(dev,"if (global.EAO_dev_enabled) dev_panel = !dev_panel;",EventType.KeyPress,116);
        set(dev,files.GetCode("dev_toggle.gml"),EventType.KeyPress,117);
        set(dev,"if (global.EAO_dev_enabled && instance_exists(o_player) && !instance_exists(o_smoothRoomChanger)) { dev_reveal = !dev_reveal; }",EventType.KeyPress,118);
        set(dev,"if (global.EAO_dev_enabled) dev_grid = !dev_grid;",EventType.KeyPress,120);
        set(dev,"if (global.EAO_dev_enabled) global.EAO_dev_art = !global.EAO_dev_art;",EventType.KeyPress,121);
        set(dev,files.GetCode("dev_visit.gml"),EventType.KeyPress,122);
        // Use the same world draw pass as the verified grid; the installed game's
        // GUI passes did not display this independent observer during runtime tests.
        // Each optional observer section uses exit, so isolate it in a block
        // guarded at the call site. Foreground remains visible with F6 off.
        set(dev,Hd2dArt.DrawForeground()+N2Hd2dArt.DrawForeground()+FieldQuest.DrawForeground()+SceneAssembly.DrawForeground()+
            "if (global.EAO_dev_enabled && dev_grid && instance_exists(o_player) && instance_exists(o_controller)) {\n"+files.GetCode("dev_draw_world.gml")+"\n}\n"+
            files.GetCode("dev_draw_gui.gml"),EventType.Draw,0);
        set(dev,"// Observer now draws in the world pass.",EventType.Draw,64);
        set(dev,"// Observer now draws in the world pass.",EventType.Draw,(uint)EventSubtypeDraw.DrawGUIEnd);
        var portal=Msl.GetObject("o_eao_dev_portal");
        set(portal,"event_inherited(); visible=false; is_lock=false; is_crime_door=false; dungeon_level_incr=0; dev_return=false; scr_locationRoomEntityInitSavable(id,false);",EventType.Create,0);
        set(portal,files.GetCode("dev_portal_alarm.gml"),EventType.Alarm,7);
    }
}
