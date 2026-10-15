using System.IO;
using System.Text.Json;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using UndertaleModLib;

// Compare embedded artwork pixels with the actual serialized collision objects,
// independently of the exporter and its layout rectangles.
internal static class EaoN1SurfaceChecks
{
    private static byte[] Png(UndertaleData data,string id)
        =>data.Sprites.Single(s=>s.Name.Content=="s_eao_hd2d_"+id).Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray();
    private static byte[] Pixels(UndertaleData data,string id)
    {
        using var stream=new MemoryStream(Png(data,id));
        var frame=BitmapFrame.Create(stream,BitmapCreateOptions.PreservePixelFormat,BitmapCacheOption.OnLoad);
        var image=new FormatConvertedBitmap(frame,PixelFormats.Bgra32,null,0);
        if(image.PixelWidth!=1040||image.PixelHeight!=780)throw new InvalidDataException("N1 canvas: "+id);
        var pixels=new byte[1040*780*4];image.CopyPixels(pixels,1040*4,0);return pixels;
    }

    internal static string[] ValidateArchitecture(UndertaleData data,JsonElement manifest)
    {
        var checks=new List<string>();
        void Require(bool ok,string name){if(!ok)throw new InvalidDataException(name);checks.Add(name);}
        var art=manifest.GetProperty("n1_architecture_repair");
        foreach(var floor in art.GetProperty("floor_sha256").EnumerateObject()) {
            var hash=Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(Png(data,floor.Name+"__floor")));
            Require(hash.Equals(floor.Value.GetString(),StringComparison.OrdinalIgnoreCase),"n1-architecture-floor-preserved-"+floor.Name);
        }
        foreach(var name in new[]{"r_eao_n1_bellhouse","r_eao_n1_underpass"}) {
            var room=data.Rooms.Single(r=>r.Name.Content==name);
            var walls=room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall")
                .Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
            var structure=Pixels(data,name+"__structure");
            long eligible=0,covered=0;
            for(var cy=2;cy<30;cy++)for(var cx=0;cx<40;cx++) {
                if(walls.Contains((cx,cy))||!walls.Contains((cx,cy-1)))continue;
                // Require a substantial two-tile north wall independently of
                // the exporter's height and image placement declarations.
                for(var y=cy*26-52;y<cy*26;y++)for(var x=cx*26;x<(cx+1)*26;x++) {
                    if(!walls.Contains((x/26,y/26)))continue;
                    eligible++;if(structure[(y*1040+x)*4+3]==255)covered++;
                }
            }
            Require(eligible>0&&covered>=eligible*0.90,"n1-architecture-two-tile-north-walls-"+name);
        }
        var backing=Pixels(data,"r_eao_n1_underpass__backing");
        var flat=true;
        for(var i=0;i<backing.Length;i+=4)
            flat&=backing[i]==backing[0]&&backing[i+1]==backing[1]&&backing[i+2]==backing[2]&&backing[i+3]==255;
        Require(flat,"n1-architecture-drain-backing-flat-no-old-water-fragments");
        return checks.ToArray();
    }

    internal static string[] Validate(UndertaleData data,JsonElement manifest)
    {
        var checks=new List<string>();
        void Require(bool ok,string name){if(!ok)throw new InvalidDataException(name);checks.Add(name);}
        foreach(var spec in manifest.GetProperty("n1_surface_repair").GetProperty("layout").GetProperty("scenes").EnumerateArray()) {
            var name=spec.GetProperty("room").GetString()!;
            var room=data.Rooms.Single(r=>r.Name.Content==name);
            var walls=room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall")
                .Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
            foreach(var layer in new[]{"floor","structure","foreground"}) {
                var sprite=data.Sprites.Single(s=>s.Name.Content=="s_eao_hd2d_"+name+"__"+layer);
                using var stream=new MemoryStream(sprite.Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray());
                var frame=BitmapFrame.Create(stream,BitmapCreateOptions.PreservePixelFormat,BitmapCacheOption.OnLoad);
                var image=new FormatConvertedBitmap(frame,PixelFormats.Bgra32,null,0);
                var pixels=new byte[image.PixelWidth*image.PixelHeight*4];image.CopyPixels(pixels,image.PixelWidth*4,0);
                var agrees=image.PixelWidth==1040&&image.PixelHeight==780;
                for(var y=0;y<image.PixelHeight;y++)for(var x=0;x<image.PixelWidth;x++) {
                    var alpha=pixels[(y*image.PixelWidth+x)*4+3];var blocked=walls.Contains((x/26,y/26));
                    agrees&=alpha is 0 or 255;
                    agrees&=layer=="floor" ? (alpha==255)==!blocked : alpha==0||blocked;
                }
                Require(agrees,"n1-surface-embedded-"+layer+"-matches-native-collision-"+name);
            }
        }
        return checks.ToArray();
    }
}
