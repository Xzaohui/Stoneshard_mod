using System;
using System.Linq;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Bake one coastline for the editor appendix and the runtime terrain/draw hook.
// The coast occupies the sea-side ring; all 83 planned land/river cells stay dry.
internal static class EastCoast
{
    private const string Digits = "0123456789abcdef";
    internal const int FirstX = 40, Width = 10, Height = 45;

    internal static string[] Bake(UndertaleRoom room)
    {
        var sea = room.Layers.Single(l => l.LayerName.Content == "Sea").TilesData.TileData;
        if (sea.Length != 79 || sea.Any(r => r.Length != 127))
            throw new InvalidOperationException("Unsupported native coastline layer shape.");
        int West(int y) {
            var frame = sea[y+22][39+77];
            if (frame > 15) throw new InvalidOperationException("Unsupported west coast transform.");
            return (int)frame;
        }
        // Every west-edge vertex must meet both original adjacent sprite edges.
        for (var y=0;y<Height-1;y++)
            if (((West(y)&8)!=0) != ((West(y+1)&2)!=0))
                throw new InvalidOperationException("Native west coast has an inconsistent shared corner.");
        var vertices = new bool[Width+1,Height+1];
        for (var vx=0;vx<=Width;vx++) for (var vy=0;vy<=Height;vy++) {
            if (vx==0) {
                vertices[vx,vy]=(West(Math.Min(vy,Height-1)) & (vy<Height ? 2 : 8))!=0;
                continue;
            }
            var water=true;
            for(var dx=-1;dx<=0;dx++) for(var dy=-1;dy<=0;dy++)
                water &= EastRegion.Cell(Math.Clamp(FirstX+vx+dx,FirstX,49),Math.Clamp(vy+dy,0,Height-1))=='~';
            vertices[vx,vy]=water;
        }
        var rows=new string[Height];
        for(var y=0;y<Height;y++) {
            var row=new char[Width];
            for(var x=0;x<Width;x++) {
                var frame=(vertices[x,y]?1:0)+(vertices[x+1,y]?2:0)
                    +(vertices[x,y+1]?4:0)+(vertices[x+1,y+1]?8:0);
                if(frame is 6 or 9) throw new InvalidOperationException("Coast saddle has no native room.");
                if(frame!=0 && EastRegion.Cell(x+FirstX,y)!='~')
                    throw new InvalidOperationException("Coast would flood planned land or a task site.");
                row[x]=Digits[frame];
            }
            rows[y]=new string(row);
        }
        return rows;
    }

    internal static int Frame(string[] rows,int x,int y)
        => y<0 ? 0 : y>=Height ? 15 : Digits.IndexOf(rows[y][x-FirstX]);
}
