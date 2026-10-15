using System.IO;
using System.Text.RegularExpressions;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using UndertaleModLib;
using UndertaleModLib.Models;

// Check the serialized hit rectangle against the actual embedded artwork,
// independently of the constants used by the Mod's sprite allocator.
internal static class EaoDoorwayHitChecks
{
    internal static string[] Validate(UndertaleData data,Func<string,string> asm)
    {
        var checks=new List<string>();
        void Require(bool ok,string message){if(!ok)throw new InvalidDataException(message);checks.Add(message);}
        var art=data.Sprites.Single(s=>s.Name.Content=="s_eao_hd2d_r01_doorway_open");
        var mask=data.Sprites.Single(s=>s.Name.Content=="s_eao_n2_doorway_hit");
        var bytes=art.Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray();
        using var stream=new MemoryStream(bytes);
        var frame=BitmapFrame.Create(stream,BitmapCreateOptions.PreservePixelFormat,BitmapCacheOption.OnLoad);
        var image=new FormatConvertedBitmap(frame,PixelFormats.Bgra32,null,0);
        var pixels=new byte[image.PixelWidth*image.PixelHeight*4];
        image.CopyPixels(pixels,image.PixelWidth*4,0);
        var left=image.PixelWidth;var top=image.PixelHeight;var right=-1;var bottom=-1;
        for(var y=0;y<image.PixelHeight;y++)for(var x=0;x<image.PixelWidth;x++) {
            if(pixels[(y*image.PixelWidth+x)*4+3]<128)continue;
            left=Math.Min(left,x);top=Math.Min(top,y);right=Math.Max(right,x);bottom=Math.Max(bottom,y);
        }
        Require(right>=left&&mask.BBoxMode==2&&mask.SepMasks==0&&mask.CollisionMasks.Count==0&&
            mask.Width==art.Width&&mask.Height==art.Height&&mask.OriginX==art.OriginX&&mask.OriginY==art.OriginY&&
            mask.MarginLeft==left&&mask.MarginRight==right&&mask.MarginTop==top&&mask.MarginBottom==bottom,
            "n2-doorway-hit-rectangle-matches-opaque-art-bounds");
        Require(mask.Textures.Count==1&&mask.Textures[0].Texture==art.Textures[0].Texture&&
            mask.MarginRight-mask.OriginX>13&&mask.MarginBottom-mask.OriginY>0,
            "n2-doorway-hit-shares-art-with-clickable-right-flap");
        var doors=new[]{"o_eao_n2_home","o_eao_n2_to_winch","o_eao_n2_camp_back","o_eao_n2_to_side",
            "o_eao_site_winch_back","o_eao_n2_side_back","o_eao_site_canal_back"};
        foreach(var name in doors) {
            var obj=data.GameObjects.Single(o=>o.Name.Content==name);
            var sprite=obj.Sprite!;var create=asm("gml_Object_"+name+"_Create_0");
            Require(obj.TextureMaskId==mask&&sprite.Name.Content=="s_eao_scene_door_anchor"&&
                sprite.OriginX==sprite.Width/2&&sprite.OriginY==sprite.Height/2&&
                obj.ParentId?.Name.Content=="o_Doors_all_small"&&obj.Events[(int)EventType.Mouse].Count==0&&
                obj.Events[(int)EventType.Other].Count==0&&create.Contains("event_inherited")&&
                !Regex.IsMatch(create,@"pop\.v\.\w+ self\.(?:grid_x|grid_y|mask_index|sprite_index)\b"),
                "n2-doorway-hit-keeps-native-grid-and-input-"+name);
        }
        return checks.ToArray();
    }
}
