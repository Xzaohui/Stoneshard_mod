using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using UndertaleModLib;
using UndertaleModLib.Models;

// Compare actual serialized door placements and embedded pixels to hit rectangles.
internal static class EaoN1DoorwayChecks
{
    internal static string[] Validate(UndertaleData data,Func<string,string> asm,JsonElement layout)
    {
        var checks=new List<string>();
        void Require(bool ok,string name){if(!ok)throw new InvalidDataException(name);checks.Add(name);}
        foreach(var asset in layout.GetProperty("assets").EnumerateArray()) {
            var id=asset.GetProperty("id").GetString()!;
            var art=data.Sprites.Single(s=>s.Name.Content=="s_eao_hd2d_"+id);
            var mask=data.Sprites.Single(s=>s.Name.Content=="s_eao_"+id+"_hit");
            using var stream=new MemoryStream(art.Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray());
            var frame=BitmapFrame.Create(stream,BitmapCreateOptions.PreservePixelFormat,BitmapCacheOption.OnLoad);
            var image=new FormatConvertedBitmap(frame,PixelFormats.Bgra32,null,0);
            var pixels=new byte[image.PixelWidth*image.PixelHeight*4];image.CopyPixels(pixels,image.PixelWidth*4,0);
            var left=image.PixelWidth;var top=image.PixelHeight;var right=-1;var bottom=-1;var binary=true;
            for(var y=0;y<image.PixelHeight;y++)for(var x=0;x<image.PixelWidth;x++) {
                var alpha=pixels[(y*image.PixelWidth+x)*4+3];binary&=alpha is 0 or 255;if(alpha<128)continue;
                left=Math.Min(left,x);top=Math.Min(top,y);right=Math.Max(right,x);bottom=Math.Max(bottom,y);
            }
            Require(binary&&right>=left&&mask.Width==52&&mask.Height==39&&mask.OriginX==26&&mask.OriginY==26&&
                mask.BBoxMode==2&&mask.SepMasks==0&&mask.CollisionMasks.Count==0&&mask.Textures.Single().Texture==art.Textures.Single().Texture&&
                mask.MarginLeft==left&&mask.MarginTop==top&&mask.MarginRight==right&&mask.MarginBottom==bottom,
                "n1-doorway-hit-matches-embedded-opaque-bounds-"+id);
        }
        var floor=asm("gml_Object_o_eao_n1_floor_Draw_0");
        Require(Regex.IsMatch(asm("gml_Object_o_eao_n1_floor_Create_0"),@"pushi\.e 100\s+pop\.v\.[iv] self.depth"),"n1-doorway-art-below-player-floor-depth");
        foreach(var spec in layout.GetProperty("doors").EnumerateArray()) {
            var name=spec.GetProperty("object").GetString()!;var artId=spec.GetProperty("art").GetString()!;
            var room=data.Rooms.Single(r=>r.Name.Content==spec.GetProperty("room").GetString());
            var obj=data.GameObjects.Single(o=>o.Name.Content==name);
            var instances=room.GameObjects.Where(i=>i.ObjectDefinition==obj).ToArray();
            var cx=spec.GetProperty("cell")[0].GetInt32();var cy=spec.GetProperty("cell")[1].GetInt32();
            Require(instances.Length==1&&instances[0].X==cx*26+13&&instances[0].Y==cy*26+13&&
                !room.GameObjects.Any(i=>i.ObjectDefinition.Name.Content=="o_hut_wall"&&(int)i.X/26==cx&&(int)i.Y/26==cy),
                "n1-doorway-art-at-unblocked-native-anchor-"+name);
            var create=asm("gml_Object_"+name+"_Create_0");var sprite=obj.Sprite!;
            Require(obj.ParentId?.Name.Content=="o_Doors_all_small"&&sprite.Name.Content=="s_eao_scene_door_anchor"&&
                sprite.OriginX==sprite.Width/2&&sprite.OriginY==sprite.Height/2&&obj.TextureMaskId?.Name.Content=="s_eao_"+artId+"_hit"&&
                obj.Events[(int)EventType.Mouse].Count==0&&obj.Events[(int)EventType.Other].Count==0&&create.Contains("event_inherited")&&
                !Regex.IsMatch(create,@"pop\.v\.\w+ self\.(?:grid_x|grid_y|mask_index|sprite_index)\b"),
                "n1-doorway-keeps-native-grid-lock-and-input-"+name);
            var draw=asm("gml_Object_"+name+"_Draw_0");
            var artIndex=data.Sprites.IndexOf(data.Sprites.Single(s=>s.Name.Content=="s_eao_hd2d_"+artId));
            Require(draw.Contains("event_inherited")&&draw.Contains("scr_cursor_get_pointed_instance")&&draw.Contains("bbox_top")&&
                Regex.IsMatch(draw,@"push(?:i\.e|\.i) "+artIndex+@"\b")&&
                Regex.Matches(draw,@"pop\.v\.\w+ self\.sprite_index\b").Count==2&&Regex.Matches(draw,@"pop\.v\.\w+ self\.shaderHighlight\b").Count==2&&
                !new[]{"self.sprlight","lock_movement","scr_smoothRoomChange","room_goto","scr_atr_set_simple"}.Any(draw.Contains),
                "n1-doorway-highlight-restores-native-state-"+name);
            var variant=@"\s+conv\.i\.v\s+";
            var pattern=@"push(?:i\.e|\.i) "+instances[0].Y+variant+@"push(?:i\.e|\.i) "+instances[0].X+variant+@"pushi\.e 0"+variant+@"push(?:i\.e|\.i) "+artIndex+variant+@"call\.i draw_sprite\(argc=4\)";
            Require(Regex.Matches(floor,pattern).Count==2,"n1-doorway-stamped-in-hd2d-and-native-floor-passes-"+name);
        }
        return checks.ToArray();
    }
}
