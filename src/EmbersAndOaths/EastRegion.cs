using System;
using System.Linq;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// World coordinates remain relative to (77,22). The approved layout's task
// coordinates are reserved as native ground until their separate migration.
internal static class EastRegion
{
    internal static readonly string[] Rows = {
        "^^^^^^^^", "^^^^^^^^", "^^^^^^^^", "^^pp^^^^", "^pppp^^^",
        "pppppp^^", "mmpppp^^", "mmmpprp^", "mmmmprp^", "^mmmmrp^",
        "^mmmmrm^", "^mmmsrm^", "^msssrs^", "sssssrss", "sssssrss",
        "sssssrs~", "sss~s~~~", "~~~~~~~~", "~~~~~~~~"
    };

    internal static char Cell(int x, int y) => x >= 48 ? (y < 35 ? '^' : '~')
        : y >= 22 && y <= 40 ? Rows[y-22][x-40] : y < 22 ? '^' : '~';

    internal static string[] PrepareMap()
    {
        PrepareRidgePaper();
        var room=Msl.GetRoom("r_GlobalMap");
        if (Rows.Length != 19 || Rows.Any(r=>r.Length != 8)) throw new InvalidOperationException("East layout shape.");
        var coast=EastCoast.Bake(room);
        // Only EAO's appended columns are authored; all 119 original editor
        // columns, including the two former border columns, remain byte-exact.
        foreach(var layer in room.Layers.Where(l=>l.TilesData != null && l.LayerName.Content != "map_eao_east")) {
            var tiles=layer.TilesData;
            for(var x=119;x<127;x++) for(var y=0;y<tiles.TileData.Length;y++) {
                var cell=Cell(x-77,y-22);
                var frame=EastCoast.Frame(coast,x-77,y-22);
                if(cell=='~' && frame==0) cell='s';
                tiles.TileData[y][x] = layer.LayerName.Content switch {
                    "Biomes" => cell switch { '^'=>7u, '~'=>8u, 'p'=>3u, 'm'=>1u, 'r' when y-22 < 33=>1u, _=>2u },
                    "Steppe" => cell is 's' or '~' || cell=='r' && y-22>=33 ? 15u : 0u,
                    "Sea" => (uint)frame,
                    _=>0u
                };
            }
        }
        var paper=room.Layers.SingleOrDefault(l=>l.LayerName.Content=="map_eao_east");
        if(paper==null) {
            var source=room.Layers.Single(l=>l.LayerName.Content=="map_brynn");
            paper=room.AddLayerInstance("map_eao_east");
            paper.LayerType=source.LayerType;paper.LayerDepth=source.LayerDepth;
            paper.XOffset=source.XOffset;paper.YOffset=source.YOffset;paper.IsVisible=source.IsVisible;
            paper.Data=NativeRooms.Copy(source.TilesData);
        }
        var t=paper.TilesData;t.TilesX=127;
        t.TileData=Enumerable.Range(0,(int)t.TilesY).Select(_=>new uint[127]).ToArray();
        for(var x=40;x<=47;x++)for(var y=25;y<=40;y++) t.TileData[y+22][x+77]=1;
        return coast;
    }

    private static void PrepareRidgePaper()
    {
        const string name="s_eao_east_ridge_paper";
        var data=DataLoader.data;
        if(data.Sprites.Any(s=>s.Name.Content==name)) return;
        var original=data.Sprites.Single(s=>s.Name.Content=="s_gmount01_paper").Textures[3].Texture;
        if(original.SourceWidth!=original.TargetWidth || original.SourceHeight!=original.TargetHeight)
            throw new InvalidOperationException("Native ridge packing changed.");
        var sprite=Msl.CreateSpriteNoCollisionMasks(name,new MarginData(0,51,0,51),new OriginData(0,0),new BoundingData<uint>(52,52));
        foreach(var frame in new[] {0,1,5,6,13,14}) {
            var left=(frame%4)*52;var top=(frame/4)*52;
            var x=Math.Max(left,original.TargetX);var y=Math.Max(top,original.TargetY);
            var right=Math.Min(left+52,original.TargetX+original.TargetWidth);var bottom=Math.Min(top+52,original.TargetY+original.TargetHeight);
            if(right<=x || bottom<=y) throw new InvalidOperationException("Empty native ridge crop.");
            // Reference the installed texture page. No PNG or texture bytes are
            // copied into the source assets or SML package.
            var item=Msl.CreateTexureItem(original.TexturePage,new RectTexture((ushort)(original.SourceX+x-original.TargetX),(ushort)(original.SourceY+y-original.TargetY),(ushort)(right-x),(ushort)(bottom-y)),new RectTexture((ushort)(x-left),(ushort)(y-top),(ushort)(right-x),(ushort)(bottom-y)),new BoundingData<ushort>(52,52));
            data.TexturePageItems.Add(item);sprite.Textures.Add(new UndertaleSprite.TextureEntry{Texture=item});
        }
        data.Sprites.Add(sprite);
    }
}
