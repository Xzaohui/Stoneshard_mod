using System.IO;
using System.Security.Cryptography;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using UndertaleModLib;

// Inspect actual serialized chunk pixels, crop coverage and native collision
// objects independently of the composer's rendering implementation.
internal static class EaoGroundChunkChecks
{
    internal static string[] Validate(UndertaleData data,Func<string,string> asm)
    {
        var checks=new List<string>();
        void Require(bool ok,string name) { if(!ok)throw new InvalidDataException(name); checks.Add(name); }
        var folder=Path.Combine(ProjectPaths.Root(),"src/Art/terrain-chunks-v1");
        using var doc=JsonDocument.Parse(File.ReadAllText(Path.Combine(folder,"manifest.json")));
        var manifest=doc.RootElement;
        Require(manifest.GetProperty("cell_size").GetInt32()==26 && manifest.GetProperty("chunk_cells").GetInt32()==30 && manifest.GetProperty("gutter").GetInt32()==2,"ground-native-cell-chunk-and-gutter-contract");
        foreach(var source in manifest.GetProperty("source_sha256").EnumerateObject()) {
            var hash=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(Path.Combine(ProjectPaths.Root(),source.Name))));
            Require(hash.Equals(source.Value.GetString(),StringComparison.OrdinalIgnoreCase),"ground-source-"+source.Name);
        }
        Require(Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(Path.Combine(folder,"layout.json")))).Equals(manifest.GetProperty("layout_sha256").GetString(),StringComparison.OrdinalIgnoreCase),"ground-layout-sha-lock");
        var floor=data.GameObjects.Single(o=>o.Name.Content=="o_eao_ground_world");
        Require(floor.ParentId==null && floor.Sprite==null && floor.Visible && !floor.Persistent && !floor.Solid,"ground-world-pure-decoration-no-parent-mask-or-persistence");
        var create=asm("gml_Object_o_eao_ground_world_Create_0");
        var worldDraw=asm("gml_Object_o_eao_ground_world_Draw_0");
        Require(create.Contains("scr_locationRoomEntityInitSavable") && worldDraw.Contains("global.EAO_dev_art"),"ground-world-excluded-save-and-art-fallback");
        bool References(string code,int index)=>Regex.IsMatch(code,@"push(?:i\.e|\.i) "+index+@"\b");
        var floorIndex=data.GameObjects.IndexOf(floor);
        Require(References(asm("gml_Object_o_eao_east_steppe_generator_Other_18"),floorIndex) && References(asm("gml_Object_o_eao_controller_Step_1"),floorIndex) && asm("gml_Object_o_eao_controller_Step_1").Contains("instance_exists"),"ground-world-fresh-generation-and-visited-load-restoration");
        var actual=data.Sprites.Where(s=>s.Name.Content.StartsWith("s_eao_ground_")).ToArray();
        Require(actual.Length==manifest.GetProperty("assets").GetArrayLength(),"ground-exact-embedded-chunk-count");
        var sceneCount=0;
        foreach(var scene in manifest.GetProperty("scenes").EnumerateArray()) {
            sceneCount++;
            var name=scene.GetProperty("room").GetString()!;
            var room=data.Rooms.Single(r=>r.Name.Content==name);
            var width=(int)room.Width; var height=(int)room.Height;
            var coverage=new byte[width*height];
            var walls=room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content=="o_hut_wall").Select(i=>((int)i.X/26,(int)i.Y/26)).ToHashSet();
            var pixelChunks=new Dictionary<(int,int),byte[]>();
            var draw=name=="r_eao_n2_world" ? worldDraw : asm(name=="r_eao_n2_sites" ? "gml_Object_o_eao_site_floor_Draw_0" : name.StartsWith("r_eao_n1_") ? "gml_Object_o_eao_n1_floor_Draw_0" : "gml_Object_o_eao_n2_floor_Draw_0");
            foreach(var chunk in scene.GetProperty("chunks").EnumerateArray()) {
                var id=chunk.GetProperty("id").GetString()!;
                var sprite=actual.Single(s=>s.Name.Content=="s_eao_ground_"+id);
                Require(sprite.Width==784 && sprite.Height==784 && sprite.OriginX==0 && sprite.OriginY==0 && sprite.CollisionMasks.Count==0,"ground-size-origin-and-no-collision-"+id);
                var png=sprite.Textures.Single().Texture.TexturePage.TextureData.Image.ToSpan(false).ToArray();
                Require(png.SequenceEqual(File.ReadAllBytes(Path.Combine(folder,chunk.GetProperty("path").GetString()!))) && Convert.ToHexString(SHA256.HashData(png))==chunk.GetProperty("sha256").GetString(),"ground-embedded-bytes-"+id);
                using var stream=new MemoryStream(png);
                var frame=BitmapFrame.Create(stream,BitmapCreateOptions.PreservePixelFormat,BitmapCacheOption.OnLoad);
                var image=new FormatConvertedBitmap(frame,PixelFormats.Bgra32,null,0);
                var pixels=new byte[784*784*4]; image.CopyPixels(pixels,784*4,0);
                var x=chunk.GetProperty("x").GetInt32(); var y=chunk.GetProperty("y").GetInt32();
                var w=chunk.GetProperty("width").GetInt32(); var h=chunk.GetProperty("height").GetInt32();
                Require(x%780==0 && y%780==0 && w>0 && h>0 && x+w<=width && y+h<=height,"ground-native-core-placement-"+id);
                var binary=true; var collision=true;
                for(var py=0;py<h;py++) for(var px=0;px<w;px++) {
                    coverage[(y+py)*width+x+px]++;
                    var alpha=pixels[((py+2)*784+px+2)*4+3];
                    binary &= alpha is 0 or 255;
                    if(!scene.GetProperty("overlay").GetBoolean()) collision &= (alpha==255)==!walls.Contains(((x+px)/26,(y+py)/26));
                }
                Require(binary && collision,"ground-core-alpha-matches-real-collision-"+id);
                string Push(int value)=>@"push(?:i\.e|\.i) "+value+@"\s+conv\.i\.v\s+";
                var crop=Push(y)+Push(x)+Push(h)+Push(w)+Push(2)+Push(2)+Push(0)+Push(data.Sprites.IndexOf(sprite))+@"call\.i draw_sprite_part\(argc=8\)";
                Require(Regex.IsMatch(draw,crop) && !draw.Contains("draw_sprite_stretched"),"ground-renderer-native-crop-not-scaled-"+id);
                pixelChunks[(x,y)]=pixels;
            }
            Require(coverage.All(v=>v==1),"ground-exactly-once-core-coverage-"+name);
            if(scene.GetProperty("overlay").GetBoolean()) foreach(var door in scene.GetProperty("native_doors").EnumerateArray()) {
                var dx=door[0].GetInt32()*26; var dy=door[1].GetInt32()*26; var opaque=true;
                for(var yy=dy;yy<dy+26;yy++) for(var xx=dx;xx<dx+26;xx++) {
                    var cx=xx/780*780; var cy=yy/780*780;
                    opaque &= pixelChunks[(cx,cy)][((yy-cy+2)*784+xx-cx+2)*4+3]==255;
                }
                Require(opaque,"ground-world-opaque-doorstep-"+door[0]+"-"+door[1]);
            }
            foreach(var (position,pixels) in pixelChunks) {
                if(pixelChunks.TryGetValue((position.Item1+780,position.Item2),out var right)) {
                    var same=true;
                    for(var y=0;y<784;y++) for(var x=0;x<4;x++) for(var c=0;c<4;c++) same &= pixels[(y*784+x+780)*4+c]==right[(y*784+x)*4+c];
                    Require(same,"ground-shared-horizontal-samples-"+name+"-"+position);
                }
                if(pixelChunks.TryGetValue((position.Item1,position.Item2+780),out var bottom)) {
                    var same=true;
                    for(var y=0;y<4;y++) for(var x=0;x<784;x++) for(var c=0;c<4;c++) same &= pixels[((y+780)*784+x)*4+c]==bottom[(y*784+x)*4+c];
                    Require(same,"ground-shared-vertical-samples-"+name+"-"+position);
                }
            }
        }
        Require(sceneCount==8,"ground-eight-current-scenes-with-large-native-surface");
        Require(!new[]{"room_goto","scr_atr_set_simple","ds_grid_set","scr_gold","EAO_N1_stage","EAO_N2_stage","lock_movement"}.Any(worldDraw.Contains),"ground-draw-no-quest-player-collision-or-reward-writes");
        return checks.ToArray();
    }
}
