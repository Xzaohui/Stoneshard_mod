using System.IO;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Models;

// Inspect serialized/compiled coast data and actual installed sprite coverage.
// These do not execute GameMaker or prove room save/edge movement behavior.
internal static class EaoEastCoastChecks
{
    internal static string[] ReadFrames(string cache)
    {
        var rows=Regex.Matches(cache,"push\\.s \"([0-9a-f]{10})\"").Select(m=>m.Groups[1].Value).Reverse().ToArray();
        if(rows.Length!=45) throw new InvalidDataException("Compiled east coast rows missing.");
        return rows;
    }

    internal static int Frame(string[] rows,int x,int y)
        =>y<0 ? 0 : y>=45 ? 15 : "0123456789abcdef".IndexOf(rows[y][x-40]);

    internal static string[] Validate(UndertaleData data,string cache,string[] rows,Func<int,int,char> cell)
    {
        var checks=new List<string>();
        void Need(bool ok,string name){if(!ok)throw new InvalidDataException(name);checks.Add(name);}
        bool Bit(int f,int b)=>(f&b)!=0;
        Need(rows.Length==45&&rows.All(r=>r.Length==10),"east-coast-compiled-contour-covers-ten-columns-and-forty-five-rows");
        var horizontal=true;var vertical=true;var west=true;var dry=true;var supported=true;
        var layer=data.Rooms.Single(r=>r.Name.Content=="r_GlobalMap").Layers.Single(l=>l.LayerName.Content=="Sea").TilesData;
        for(var y=0;y<45;y++)for(var x=40;x<50;x++) {
            var f=Frame(rows,x,y);
            if(x<49) {var next=Frame(rows,x+1,y);horizontal &= Bit(f,2)==Bit(next,1)&&Bit(f,8)==Bit(next,4);}
            if(y<44) {var next=Frame(rows,x,y+1);vertical &= Bit(f,4)==Bit(next,1)&&Bit(f,8)==Bit(next,2);}
            if(x==40) {var native=(int)layer.TileData[y+22][116];west &= Bit(native,2)==Bit(f,1)&&Bit(native,8)==Bit(f,4);}
            if(cell(x,y)!='~') dry &= f==0;
            supported &= f is not (6 or 9);
        }
        Need(horizontal,"east-coast-every-horizontal-water-edge-shares-both-endpoints");
        Need(vertical,"east-coast-every-vertical-water-edge-shares-both-endpoints");
        Need(west,"east-coast-retained-native-west-water-edge-matches");
        Need(dry,"east-coast-all-planned-land-river-and-final-task-cells-stay-dry");
        Need(supported,"east-coast-no-saddle-without-a-native-room");
        // Dry portions must connect to the west entrance through non-water
        // edges, not merely touch a diagonal corner or form a detached island.
        var walkable=new HashSet<(int x,int y)>();
        for(var y=0;y<45;y++)for(var x=40;x<48;x++)if(cell(x,y)!='^'&&Frame(rows,x,y)!=15)walkable.Add((x,y));
        var seen=new HashSet<(int x,int y)>();var queue=new Queue<(int x,int y)>();queue.Enqueue((40,35));
        while(queue.TryDequeue(out var p)) {
            if(!walkable.Contains(p)||!seen.Add(p))continue;
            var f=Frame(rows,p.x,p.y);
            foreach(var d in new[]{(-1,0,1,4),(1,0,2,8),(0,-1,1,2),(0,1,4,8)})
                if(!Bit(f,d.Item3)||!Bit(f,d.Item4))queue.Enqueue((p.x+d.Item1,p.y+d.Item2));
        }
        Need(seen.SetEquals(walkable),"east-coast-every-dry-shore-portion-connects-to-west-land-without-diagonal-only-islands");
        Need(Frame(rows,43,38)==0&&cache.Contains("\"EAO_coast_frame\"")&&cache.Contains("string_pos")&&!cache.Contains("scr_glmap_findShoreTile"),
            "east-coast-one-canonical-contour-drives-draw-and-native-terrain-with-dry-inlet");
        foreach(var name in new[]{"r_SeaShore_NorthWestU","r_SeaShore_NorthEastU","r_SeaShore_North01","r_SeaShore_North02","r_SeaShore_North03"}) {
            var room=data.Rooms.Single(r=>r.Name.Content==name);
            Need(room.Width==2340&&room.Height==2340,"east-coast-full-size-native-room-"+name);
        }
        Need(new[]{"\"north\"","\"NorthWestOutside\"","\"NorthEastOutside\""}.All(cache.Contains),"east-coast-north-and-both-outside-corner-directions-present");

        var sprite=data.Sprites.Single(s=>s.Name.Content=="s_glmap_sea_strip16");
        var pages=new Dictionary<UndertaleEmbeddedTexture,(byte[] bytes,int width)>();
        bool Opaque(int f,int x,int y) {
            var t=sprite.Textures[f].Texture;
            var tx=x-t.TargetX;var ty=y-t.TargetY;
            if(tx<0||ty<0||tx>=t.TargetWidth||ty>=t.TargetHeight)return false;
            if(!pages.TryGetValue(t.TexturePage,out var page)) {
                var nativeImage=t.TexturePage.TextureData.Image.ConvertToRawBgra();
                var bytes=nativeImage.GetRawImageData().ToArray();
                page=(bytes,nativeImage.Width);pages.Add(t.TexturePage,page);
            }
            return page.bytes[((t.SourceY+ty)*page.width+t.SourceX+tx)*4+3]>=128;
        }
        var corners=true;
        for(var f=0;f<16;f++) {
            corners &= Opaque(f,3,3)==Bit(f,1)&&Opaque(f,48,3)==Bit(f,2)
                &&Opaque(f,3,48)==Bit(f,4)&&Opaque(f,48,48)==Bit(f,8);
        }
        Need(corners,"east-coast-corner-bits-match-actual-embedded-native-water-pixels");
        var horizontalPixels=true;var verticalPixels=true;
        for(var y=0;y<45;y++)for(var x=40;x<50;x++)foreach(var sample in new[]{8,43}) {
            var f=Frame(rows,x,y);
            if(x<49)horizontalPixels &= Opaque(f,51,sample)==Opaque(Frame(rows,x+1,y),0,sample);
            if(y<44)verticalPixels &= Opaque(f,sample,51)==Opaque(Frame(rows,x,y+1),sample,0);
            if(x==40)horizontalPixels &= Opaque((int)layer.TileData[y+22][116],51,sample)==Opaque(f,0,sample);
        }
        Need(horizontalPixels,"east-coast-horizontal-native-water-pixel-coverage-continuous-at-edge-quarters");
        Need(verticalPixels,"east-coast-vertical-native-water-pixel-coverage-continuous-at-edge-quarters");
        return checks.ToArray();
    }
}
