using System;
using System.Linq;
using System.Text;
using System.Text.Json;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Visual thresholds only. NightQuest/NightRooms retain all routes, locks and cells.
internal static class N1DoorwayArt
{
    private static readonly JsonDocument Document=JsonDocument.Parse(
        typeof(N1DoorwayArt).Assembly.GetManifestResourceStream("EAO.N1Doorways.json")!);
    private static JsonElement Layout=>Document.RootElement;
    private static string Mask(string art)=>"s_eao_"+art+"_hit";
    internal static void Ensure()
    {
        SceneDoorAnchor.Ensure();
        foreach(var asset in Layout.GetProperty("assets").EnumerateArray()) {
            var art=asset.GetProperty("id").GetString()!;
            Hd2dArt.Add(art,52,39,26,26);
            var source=Msl.GetSprite(Hd2dArt.Sprite(art));
            var mask=DataLoader.data.Sprites.SingleOrDefault(s=>s.Name.Content==Mask(art));
            if(mask==null) {
                mask=NativeRooms.Copy(source);mask.Name=DataLoader.data.Strings.MakeString(Mask(art));
                foreach(var entry in source.Textures)mask.Textures.Add(new UndertaleSprite.TextureEntry{Texture=entry.Texture});
                DataLoader.data.Sprites.Add(mask);
            }
            var bounds=asset.GetProperty("alpha_bbox");
            mask.BBoxMode=2;mask.MarginLeft=bounds[0].GetInt32();mask.MarginTop=bounds[1].GetInt32();
            mask.MarginRight=bounds[2].GetInt32()-1;mask.MarginBottom=bounds[3].GetInt32()-1;
        }
    }
    internal static string DrawStamps(string room)
    {
        var code=new StringBuilder();
        foreach(var door in Layout.GetProperty("doors").EnumerateArray())
            if(door.GetProperty("room").GetString()==room) {
                var cell=door.GetProperty("cell");
                code.AppendLine("draw_sprite("+Hd2dArt.Sprite(door.GetProperty("art").GetString()!)+",0,"+(cell[0].GetInt32()*26+13)+","+(cell[1].GetInt32()*26+13)+");");
            }
        return code.ToString();
    }
    internal static void Configure(Action<UndertaleGameObject,string,EventType,uint> set,ModFile files)
    {
        var fallbackStamps=new StringBuilder("if ("+N2Hd2dArt.Active+") {\n");
        foreach(var room in NightRooms.Shapes.Keys)
            fallbackStamps.AppendLine("if (room=="+room+") {\n"+DrawStamps(room)+"}");
        fallbackStamps.AppendLine("}");
        // HD2D floor branches exit early; stamps must be present in both floor passes.
        set(Msl.GetObject("o_eao_n1_floor"),Hd2dArt.DrawFloor(true)+NightRooms.FloorDraw()+fallbackStamps,EventType.Draw,0);
        foreach(var door in Layout.GetProperty("doors").EnumerateArray()) {
            var obj=Msl.GetObject(door.GetProperty("object").GetString()!);
            var art=door.GetProperty("art").GetString()!;
            obj.ParentId=Msl.GetObject("o_Doors_all_small");obj.Sprite=SceneDoorAnchor.Ensure();obj.Visible=true;
            obj.TextureMaskId=Msl.GetSprite(Mask(art));
            set(obj,files.GetCode("n1_door_draw.gml").Replace("EAO_DOORWAY_SPRITE",Hd2dArt.Sprite(art)),EventType.Draw,0);
        }
    }
}
