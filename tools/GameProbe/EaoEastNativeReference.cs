using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using UndertaleModLib;

// Small, local-only reference sheet from the user-provided atlas sample.
// Uses current sprite metadata; this preview is not embedded-pixel verification.
internal static class EaoEastNativeReference
{
    internal static void Export(UndertaleData data, string sampleRoot)
    {
        foreach (var id in new[] { 340,355,359,360,361,362,363,366,367,368,369,370,302,300 }) {
            var room=data.Rooms[id]; Console.WriteLine($"ROOM {id} {room.Name.Content} {room.Width}x{room.Height}");
        }
        var names=new[] { "s_glmap_steppe_strip16", "s_glmap_sea_strip16", "s_gmount01_1_strip16", "s_gmount01_2_strip16", "s_gmount01_3_strip16", "s_gmount01_4_strip16" };
        var atlases=new Dictionary<int,BitmapSource>();
        var canvas=new DrawingVisual();
        using(var dc=canvas.RenderOpen()) {
            dc.DrawRectangle(Brushes.DarkSlateGray,null,new Rect(0,0,16*64,names.Length*86));
            for(var y=0;y<names.Length;y++) {
                var sprite=data.Sprites.Single(s=>s.Name.Content==names[y]);
                for(var x=0;x<16;x++) {
                    var texture=sprite.Textures[x].Texture;
                    var page=data.EmbeddedTextures.IndexOf(texture.TexturePage);
                    if(!atlases.TryGetValue(page,out var atlas)) {
                        using var ms=File.OpenRead(Path.Combine(sampleRoot,$"atlas-{page:000}.png"));
                        atlas=BitmapFrame.Create(ms,BitmapCreateOptions.PreservePixelFormat,BitmapCacheOption.OnLoad);atlases.Add(page,atlas);
                    }
                    var crop=new CroppedBitmap(atlas,new Int32Rect(texture.SourceX,texture.SourceY,texture.SourceWidth,texture.SourceHeight));
                    dc.DrawImage(crop,new Rect(x*64+texture.TargetX,y*86+texture.TargetY,texture.TargetWidth,texture.TargetHeight));
                    dc.DrawText(new FormattedText(x.ToString(),System.Globalization.CultureInfo.InvariantCulture,FlowDirection.LeftToRight,new Typeface("Segoe UI"),12,Brushes.White,1),new Point(x*64,y*86+55));
                }
                Console.WriteLine($"ROW {y} {names[y]}");
            }
        }
        var image=new RenderTargetBitmap(16*64,names.Length*86,96,96,PixelFormats.Pbgra32);image.Render(canvas);
        var encoder=new PngBitmapEncoder();encoder.Frames.Add(BitmapFrame.Create(image));
        var path=ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","east-native-reference.png"),"artifacts");
        using(var file=File.Create(path))encoder.Save(file);Console.WriteLine(path);
    }
}
