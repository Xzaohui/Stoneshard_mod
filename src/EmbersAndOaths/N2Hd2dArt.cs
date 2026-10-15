using System;
using System.Text;
using ModShardLauncher;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Visual adapters only. N2Quest remains the authority for actors, doors and cells.
internal static class N2Hd2dArt
{
    internal const string Active="!variable_global_exists(\"EAO_dev_enabled\") || !global.EAO_dev_enabled || global.EAO_dev_art";
    internal static void Ensure()
    {
        foreach (var room in N2Quest.Shapes.Keys)
            foreach (var layer in new[] { "backing", "floor", "structure", "foreground" })
                Hd2dArt.Add(room + "__" + layer,1040,780,0,0);
        Hd2dArt.Add("r01_coffin_coat",52,78,26,65);
        Hd2dArt.Add("r01_winch_socket",52,52,26,43);
        Hd2dArt.Add("r01_worker_shed",260,208,130,190);
        Hd2dArt.Add("r01_winch_shed",208,182,104,165);
        Hd2dArt.Add("r01_canal_entry",260,234,130,216);
    }
    internal static string DrawFloor()
    {
        var code = new StringBuilder("if (" + Active + ") {\n");
        foreach (var room in N2Quest.Shapes.Keys) {
            code.AppendLine("if (room == " + room + ") {");
            foreach (var layer in new[] { "backing", "floor", "structure" })
                code.AppendLine("draw_sprite(" + Hd2dArt.Sprite(room + "__" + layer) + ",0,0,0);");
            code.AppendLine("exit; }");
        }
        return code.AppendLine("}").ToString();
    }
    internal static string DrawForeground()
    {
        var code = new StringBuilder("if (" + Active + ") {\n");
        foreach (var room in N2Quest.Shapes.Keys)
            code.AppendLine("if (room == " + room + ") draw_sprite(" + Hd2dArt.Sprite(room+"__foreground") + ",0,0,0);");
        return code.AppendLine("}").ToString();
    }
    internal static void Configure(Action<UndertaleGameObject,string,EventType,uint> set)
    {
        set(Msl.GetObject("o_eao_n2_floor"),DrawFloor()+N2Quest.FloorDraw(),EventType.Draw,0);
        foreach (var pair in new[] { ("coffin","r01_coffin_coat"),("winch","r01_winch_socket") })
            set(Msl.GetObject("o_eao_n2_"+pair.Item1),"if ("+Active+") { draw_sprite("+Hd2dArt.Sprite(pair.Item2)+",0,x,y); } else { event_inherited(); }",EventType.Draw,0);
    }
}
