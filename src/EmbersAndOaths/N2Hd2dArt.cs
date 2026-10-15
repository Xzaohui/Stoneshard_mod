using System;
using System.Linq;
using System.Text;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Visual adapters only. N2Quest remains the authority for actors, doors and cells.
internal static class N2Hd2dArt
{
    internal const string DoorwayMask="s_eao_n2_doorway_hit";
    internal static readonly (string Room,string Object,int X,int Y)[] Doorways = {
        (N2Quest.Camp,"o_eao_n2_home",7,24),(N2Quest.Camp,"o_eao_n2_to_winch",33,11),
        (N2Quest.Winch,"o_eao_n2_camp_back",12,24),(N2Quest.Winch,"o_eao_n2_to_side",25,7),
        (N2Quest.Winch,"o_eao_site_winch_back",31,23),
        (N2Quest.Side,"o_eao_n2_side_back",29,21),(N2Quest.Side,"o_eao_site_canal_back",8,22)
    };
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
        Hd2dArt.Add("r01_doorway_open",52,65,26,52);
        // The visible floor opening occupies x=-26..25, y=-14..12. The
        // inherited barn mask only reaches x=12, y=4 and misses its right flap.
        // Keep Sprite (and thus native grid calculation) separate from Mask.
        var source=Msl.GetSprite(Hd2dArt.Sprite("r01_doorway_open"));
        var mask=DataLoader.data.Sprites.SingleOrDefault(s=>s.Name.Content==DoorwayMask);
        if(mask==null) {
            mask=NativeRooms.Copy(source);mask.Name=DataLoader.data.Strings.MakeString(DoorwayMask);
            foreach(var entry in source.Textures)mask.Textures.Add(new UndertaleSprite.TextureEntry{Texture=entry.Texture});
            DataLoader.data.Sprites.Add(mask);
        }
        mask.BBoxMode=2;mask.MarginLeft=0;mask.MarginRight=51;mask.MarginTop=38;mask.MarginBottom=64;
    }
    internal static string DrawFloor()
    {
        var code = new StringBuilder("if (" + Active + ") {\n");
        foreach (var room in N2Quest.Shapes.Keys) {
            code.AppendLine("if (room == " + room + ") {");
            foreach (var layer in new[] { "backing", "floor", "structure" })
                code.AppendLine("draw_sprite(" + Hd2dArt.Sprite(room + "__" + layer) + ",0,0,0);");
            // Architectural stamps belong below actors, so a player standing
            // in the native doorway is not covered by a detached door slab.
            foreach(var door in Doorways)
                if(door.Room==room)code.AppendLine("draw_sprite("+Hd2dArt.Sprite("r01_doorway_open")+",0,"+(door.X*26+13)+","+(door.Y*26+13)+");");
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
    internal static void Configure(Action<UndertaleGameObject,string,EventType,uint> set,ModFile files)
    {
        set(Msl.GetObject("o_eao_n2_floor"),DrawFloor()+N2Quest.FloorDraw(),EventType.Draw,0);
        foreach(var name in new[]{"to_winch","camp_back","to_side","side_back"}) {
            var door=Msl.GetObject("o_eao_n2_"+name);
            door.ParentId=Msl.GetObject("o_Doors_all_small");
            door.Sprite=SceneDoorAnchor.Ensure();
            set(door,files.GetCode("n2_door_draw.gml"),EventType.Draw,0);
        }
        // Coffin uses the HD2D coat in both modes so its perspective no longer flips with F10;
        // the fallback still goes through the native draw (outline/interaction) with the coat sprite.
        var coat=Hd2dArt.Sprite("r01_coffin_coat");
        set(Msl.GetObject("o_eao_n2_coffin"),"if ("+Active+") { draw_sprite("+coat+",0,x,y); } else { var _eao_s = sprite_index; sprite_index = "+coat+"; event_inherited(); sprite_index = _eao_s; }",EventType.Draw,0);
        set(Msl.GetObject("o_eao_n2_winch"),"if ("+Active+") { draw_sprite("+Hd2dArt.Sprite("r01_winch_socket")+",0,x,y); } else { event_inherited(); }",EventType.Draw,0);
    }
    internal static void ConfigureDoorwayMasks()
    {
        foreach(var door in Doorways)Msl.GetObject(door.Object).TextureMaskId=Msl.GetSprite(DoorwayMask);
    }
}
