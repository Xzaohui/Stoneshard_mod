using System;
using System.IO;
using System.Linq;
using System.Buffers.Binary;
using System.Text;
using ModShardLauncher;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Util;

namespace EmbersAndOaths;

internal static class Hd2dArt
{
    // N1 artwork is the ordinary scene renderer. F10 remains a diagnostic
    // fallback while observation is enabled; quarry keeps its existing gate.
    internal const string Active=N2Hd2dArt.Active;
    internal const string ObserverActive="variable_global_exists(\"EAO_dev_enabled\") && global.EAO_dev_enabled && global.EAO_dev_art";
    internal static string Sprite(string id)=>"s_eao_hd2d_"+id;
    internal static void Ensure()
    {
        foreach(var room in NightRooms.Shapes.Keys)
            foreach(var layer in new[]{"backing","floor","structure","foreground"}) Add(room+"__"+layer,1040,780,0,0);
        Add("n1_bell",78,104,39,95); Add("n1_bedding",104,78,52,60);
        Add("n1_cut_rope",26,26,13,20); Add("n1_bellhouse_exterior",312,260,167,249);
    }
    internal static void Add(string id,int w,int h,int ox,int oy)
    {
        var data=DataLoader.data;
        using var input=typeof(Hd2dArt).Assembly.GetManifestResourceStream("EAO.HD2D."+id+".png") ?? throw new InvalidDataException("Missing embedded HD2D asset: "+id);
        using var stream=new MemoryStream(); input.CopyTo(stream);var png=stream.ToArray();
        if(BinaryPrimitives.ReadInt32BigEndian(png.AsSpan(16,4))!=w||BinaryPrimitives.ReadInt32BigEndian(png.AsSpan(20,4))!=h)throw new InvalidDataException("HD2D dimensions drift: "+id);
        var sprite=data.Sprites.SingleOrDefault(s=>s.Name.Content==Sprite(id));
        if(sprite!=null&&(sprite.Width!=w||sprite.Height!=h||sprite.OriginX!=ox||sprite.OriginY!=oy))throw new InvalidDataException("Version changed HD2D sprite geometry: "+id);
        var texture=sprite?.Textures.Single().Texture.TexturePage;
        if(texture==null){texture=new UndertaleEmbeddedTexture{Name=data.Strings.MakeString("EAO_HD2D_"+id)};data.EmbeddedTextures.Add(texture);}
        texture.TextureData.Image=GMImage.FromPng(png);
        if(sprite!=null)return;
        var item=Msl.CreateTexureItem(texture,new RectTexture(0,0,(ushort)w,(ushort)h),new RectTexture(0,0,(ushort)w,(ushort)h),new BoundingData<ushort>((ushort)w,(ushort)h));
        data.TexturePageItems.Add(item);
        sprite=Msl.CreateSpriteNoCollisionMasks(Sprite(id),new MarginData(0,h-1,0,w-1),new OriginData(ox,oy),new BoundingData<uint>((uint)w,(uint)h));
        sprite.Textures.Add(new UndertaleSprite.TextureEntry{Texture=item});data.Sprites.Add(sprite);
    }
    internal static string DrawFloor(bool includeDoorways=false)
    {
        var code=new StringBuilder("if ("+Active+") {\n");
        foreach(var room in NightRooms.Shapes.Keys){
            code.AppendLine("if (room == "+room+") {");
            foreach(var layer in new[]{"backing","floor","structure"})code.AppendLine("draw_sprite("+Sprite(room+"__"+layer)+",0,0,0);");
            if(includeDoorways)code.Append(N1DoorwayArt.DrawStamps(room));
            code.AppendLine("exit; }");
        }
        return code.AppendLine("}").ToString();
    }
    internal static string DrawForeground()
    {
        var code=new StringBuilder();
        code.AppendLine("if ("+Active+") {");
        foreach(var room in NightRooms.Shapes.Keys)code.AppendLine("if (room == "+room+") draw_sprite("+Sprite(room+"__foreground")+",0,0,0);");
        return code.AppendLine("}").ToString();
    }
}
