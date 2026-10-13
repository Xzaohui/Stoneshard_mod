using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using ModShardLauncher;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

internal static class NightRooms
{
    internal const string Yard="r_eao_n1_yard", Bellhouse="r_eao_n1_bellhouse", Underpass="r_eao_n1_underpass";
    internal const int Columns=40, Rows=30, Tile=26;
    // Inclusive native grid cells. These are the sole source of visual floors,
    // collisions and exported layout checks; no cloned building backdrop.
    internal static readonly Dictionary<string,(int,int,int,int)[]> Shapes = new() {
        [Yard]=new[]{(4,4,16,25),(17,18,29,21),(28,8,35,24)},
        [Bellhouse]=new[]{(4,6,25,23),(26,16,35,19)},
        [Underpass]=new[]{(4,19,15,24),(13,6,17,20),(17,6,33,10)}
    };
    internal static HashSet<(int,int)> Cells(string name)
    {
        var cells=new HashSet<(int,int)>();
        foreach(var r in Shapes[name]) for(var x=r.Item1;x<=r.Item3;x++) for(var y=r.Item2;y<=r.Item4;y++) cells.Add((x,y));
        return cells;
    }
    internal static void Prepare()
    {
        foreach(var n in Shapes.Keys) {
            if(DataLoader.data.Rooms.Any(r=>r.Name.Content==n)) continue;
            var source=Msl.GetRoom("r_DockStore1floor"); var room=NativeRooms.Copy(source);
            room.Name=DataLoader.data.Strings.MakeString(n); room.Caption=DataLoader.data.Strings.MakeString(n==Yard?"旧渡口断桥":n==Bellhouse?"无声钟房":"渡口暗渠");
            room.Width=Columns*Tile; room.Height=Rows*Tile; room.Persistent=false; room.CreationCodeId=null;
            room.Views.Clear(); foreach(var view in source.Views) room.Views.Add(NativeRooms.Copy(view));
            room.GameObjects.Clear(); room.Layers.Clear(); room.Backgrounds.Clear(); room.Tiles.Clear();
            DataLoader.data.Rooms.Add(room);
            room.AddLayerInstance("Controllers").LayerDepth=-4000;
            room.AddLayerInstance("Collisions").LayerDepth=-3900;
            room.AddLayerInstance("Story").LayerDepth=-500;
            room.AddLayerInstance("EAO_Floor").LayerDepth=100;
        }
    }
    private static void Add(UndertaleRoom r,string obj,int cx,int cy,string layer="Story",bool corner=false)
        =>r.AddGameObject(layer,obj,x:cx*Tile+(corner?0:13),y:cy*Tile+(corner?0:13));
    internal static void Build()
    {
        foreach(var name in Shapes.Keys) {
            var r=Msl.GetRoom(name); if(r.GameObjects.Count!=0) continue;
            // Reuse only native lifecycle controllers and their house-light
            // initialization, never source geometry or commercial backdrop art.
            var source=Msl.GetRoom("r_DockStore1floor");
            foreach(var id in new[]{"o_controller","o_dialog_controller","o_generationController"}) {
                var original=source.GameObjects.Single(i=>i.ObjectDefinition.Name.Content==id);
                r.AddGameObject("Controllers",id,id=="o_controller"?original.CreationCode:null,x:(int)original.X,y:(int)original.Y);
            }
            Add(r,"o_eao_n1_floor",0,0,"EAO_Floor",true);
            var cells=Cells(name);
            for(var x=0;x<Columns;x++) for(var y=0;y<Rows;y++) if(!cells.Contains((x,y))) Add(r,"o_hut_wall",x,y,"Collisions",true);
            if(name==Yard) {
                Add(r,"o_eao_n1_home",7,24); Add(r,"o_eao_n1_to_bell",32,9);
                Add(r,"o_eao_n1_tor",11,13); Add(r,"o_eao_n1_rope",31,19);
                Add(r,"o_eao_n1_bell_art",31,16);
                Add(r,"o_candle03",10,7); Add(r,"o_candlefire",10,7);
                Add(r,"o_candle03",30,13); Add(r,"o_candlefire",30,13);
                Add(r,"o_eao_n1_start_yard_in",7,22,"Controllers"); Add(r,"o_eao_n1_start_yard_back",32,11,"Controllers");
                Add(r,"o_abstract_player",7,22,"Controllers");
            } else if(name==Bellhouse) {
                Add(r,"o_eao_n1_to_yard",7,22); Add(r,"o_eao_n1_to_drain",34,17);
                Add(r,"o_eao_n1_ivo",20,10); Add(r,"o_eao_n1_cots",17,20);
                Add(r,"o_candle03",10,10); Add(r,"o_candlefire",10,10);
                Add(r,"o_candle03",22,18); Add(r,"o_candlefire",22,18);
                Add(r,"o_eao_n1_start_house_in",7,20,"Controllers"); Add(r,"o_eao_n1_start_house_back",32,17,"Controllers");
                Add(r,"o_abstract_player",7,20,"Controllers");
            } else {
                Add(r,"o_eao_n1_to_house",6,22); Add(r,"o_eao_n1_rhea",30,8);
                Add(r,"o_candle03",15,15); Add(r,"o_candlefire",15,15);
                Add(r,"o_candle03",25,8); Add(r,"o_candlefire",25,8);
                Add(r,"o_eao_n1_start_drain_in",6,20,"Controllers"); Add(r,"o_abstract_player",6,20,"Controllers");
            }
        }
    }
    internal static string FloorDraw()
    {
        var code=new StringBuilder("var _c = draw_get_color(); var _a = draw_get_alpha(); draw_set_alpha(1); draw_set_color(make_color_rgb(15,23,26)); draw_rectangle(0,0,room_width,room_height,false);\n");
        foreach(var name in Shapes.Keys) {
            var cells=Cells(name); code.AppendLine("if (room == "+name+") {");
            foreach(var p in cells.OrderBy(p=>p.Item2).ThenBy(p=>p.Item1)) {
                var px=p.Item1*Tile; var py=p.Item2*Tile; var tint=name==Bellhouse?"make_color_rgb(65,55,43)":"make_color_rgb(53,62,61)";
                code.AppendLine($"draw_set_color({tint}); draw_rectangle({px},{py},{px+25},{py+25},false);");
                code.AppendLine($"draw_set_color(make_color_rgb(36,39,35)); draw_line({px},{py+25},{px+25},{py+25});");
                if((p.Item1+p.Item2)%4==0) code.AppendLine($"draw_sprite_ext(s_dungeonfloor01, {(p.Item1+p.Item2)%12}, {px+13}, {py+13}, 0.25, 0.25, 0, c_white, 0.3);");
                if(!cells.Contains((p.Item1,p.Item2-1))) code.AppendLine($"draw_set_color(make_color_rgb(91,92,80)); draw_rectangle({px},{py-13},{px+25},{py+2},false); draw_set_color(make_color_rgb(30,32,30)); draw_line({px},{py},{px+25},{py});");
                if(!cells.Contains((p.Item1-1,p.Item2))) code.AppendLine($"draw_set_color(make_color_rgb(85,86,73)); draw_rectangle({px-6},{py},{px+1},{py+25},false);");
                if(!cells.Contains((p.Item1+1,p.Item2))) code.AppendLine($"draw_set_color(make_color_rgb(41,44,40)); draw_rectangle({px+23},{py},{px+29},{py+25},false);");
            }
            code.AppendLine("}");
        }
        code.AppendLine("draw_set_color(_c); draw_set_alpha(_a);"); return code.ToString();
    }
}
