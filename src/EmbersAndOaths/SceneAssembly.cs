using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Physical scene assembly only: no actor, dialogue, quest or reward writes.
internal static class SceneAssembly
{
    internal const string Sites = "r_eao_n2_sites";
    private static readonly JsonDocument Document = JsonDocument.Parse(
        typeof(SceneAssembly).Assembly.GetManifestResourceStream("EAO.SceneAssembly.json")
        ?? throw new InvalidDataException("Missing embedded scene assembly layout."));
    private static JsonElement Layout => Document.RootElement;
    private static string S(JsonElement e, string key) => e.GetProperty(key).GetString()!;
    private static IEnumerable<JsonElement> Items(string key) => Layout.GetProperty(key).EnumerateArray();
    private static string Obj(string id) => "o_eao_site_" + id;
    private static string Art(string source) => Hd2dArt.Sprite("n2site_" + source);
    internal static HashSet<(int,int)> Cells()
    {
        var cells = new HashSet<(int,int)>();
        foreach (var r in Items("walkable_rectangles"))
            for (var x=r[0].GetInt32();x<=r[2].GetInt32();x++) for(var y=r[1].GetInt32();y<=r[3].GetInt32();y++) cells.Add((x,y));
        foreach (var b in Items("buildings")) {
            var r=b.GetProperty("blocked");
            for(var x=r[0].GetInt32();x<=r[2].GetInt32();x++) for(var y=r[1].GetInt32();y<=r[3].GetInt32();y++) cells.Remove((x,y));
        }
        return cells;
    }
    internal static void Prepare()
    {
        SceneDoorAnchor.Ensure();
        if (!DataLoader.data.Rooms.Any(r=>r.Name.Content==Sites)) {
            var source=Msl.GetRoom("r_DockStore1floor");var room=NativeRooms.Copy(source);
            room.Name=DataLoader.data.Strings.MakeString(Sites);room.Caption=DataLoader.data.Strings.MakeString(S(Layout,"title"));
            room.Width=(uint)(Layout.GetProperty("columns").GetInt32()*26);room.Height=(uint)(Layout.GetProperty("rows").GetInt32()*26);
            room.Persistent=false;room.CreationCodeId=null;
            room.Views.Clear();foreach(var view in source.Views)room.Views.Add(NativeRooms.Copy(view));
            room.GameObjects.Clear();room.Layers.Clear();room.Backgrounds.Clear();room.Tiles.Clear();
            DataLoader.data.Rooms.Add(room);
            room.AddLayerInstance("Controllers").LayerDepth=-4000;
            room.AddLayerInstance("Collisions").LayerDepth=-3900;
            room.AddLayerInstance("Story").LayerDepth=-500;
            room.AddLayerInstance("EAO_Floor").LayerDepth=100;
        }
        foreach(var b in Items("buildings")) {
            Msl.AddObject(Obj("building_"+S(b,"id")),isVisible:true);
            Msl.AddObject(Obj("door_"+S(b,"id")),parentName:"o_Doors_all_small",isVisible:true);
            Msl.AddObject(Obj("start_"+S(b,"id")),parentName:"o_position_starter",isVisible:false);
        }
        foreach(var p in Items("props"))Msl.AddObject(Obj(S(p,"id")),isVisible:true);
        foreach(var d in Items("interior_returns"))
            if(!d.GetProperty("existing").GetBoolean())Msl.AddObject(S(d,"object"),parentName:"o_Doors_all_small",isVisible:true);
        Msl.AddObject(Obj("home"),parentName:"o_Doors_all_small",isVisible:true);
        Msl.AddObject(Obj("start_in"),parentName:"o_position_starter",isVisible:false);
        Msl.AddObject(Obj("floor"),isVisible:true);
        foreach(var layer in new[]{"backing","floor","structure","foreground"})Hd2dArt.Add("n2site__"+layer,1352,988,0,0);
        Hd2dArt.Add("n2site_r01_worker_shed",260,208,130,190);
        Hd2dArt.Add("n2site_r01_winch_shed",208,182,104,165);
        Hd2dArt.Add("n2site_r01_canal_entry",260,234,130,216);
        Hd2dArt.Add("n2site_r01_shelter_bedroll",52,52,26,43);
        Hd2dArt.Add("n2site_r01_water_jug",26,26,13,23);
        Hd2dArt.Add("n2site_r01_maintenance_ladder",26,78,13,65);
    }
    private static void Place(UndertaleRoom room,string name,JsonElement cell,string layer="Story")
        => Place(room,name,cell[0].GetInt32(),cell[1].GetInt32(),layer);
    private static void Place(UndertaleRoom room,string name,int x,int y,string layer="Story",bool corner=false)
    {
        var px=x*26+(corner?0:13);var py=y*26+(corner?0:13);
        var prior=room.GameObjects.Where(i=>i.ObjectDefinition.Name.Content==name&&i.X==px&&i.Y==py).ToArray();
        if(prior.Length>1)throw new InvalidDataException("Duplicate scene instance: "+name);
        if(prior.Length==0)room.AddGameObject(layer,name,x:px,y:py);
    }
    internal static string DrawForeground() => "if (room == "+Sites+") draw_sprite("+Hd2dArt.Sprite("n2site__foreground")+",0,0,0);\n";
    internal static void Configure(Action<UndertaleGameObject,string,EventType,uint> set,ModFile files)
    {
        void Door(string name,string target,string tag,string cn,string en,bool facade=false) {
            var obj=Msl.GetObject(name);obj.ParentId=Msl.GetObject("o_Doors_all_small");obj.Sprite=SceneDoorAnchor.Ensure();obj.Visible=true;
            var interior = N2Hd2dArt.Doorways.Any(d=>d.Object==name);
            // Standing doors (night_door_draw) sort by row like native props: the
            // player on the door row or south of it draws over the door.
            set(obj,"event_inherited(); target = "+target+"; position_tag = "+NativeDocuments.Quote(tag)+"; is_lock=false; is_crime_door=false; is_quest=false; dungeon_level_incr=0; name=global.language==3 ? "+NativeDocuments.Quote(cn)+" : "+NativeDocuments.Quote(en)+"; scr_locationRoomEntityInitSavable(id,false);"+(facade||interior ? "" : " depth = -y + 1;"),EventType.Create,0);
            set(obj,files.GetCode(facade ? "site_door_draw.gml" : interior ? "n2_door_draw.gml" : "night_door_draw.gml"),EventType.Draw,0);
            if (facade) set(obj,files.GetCode("site_door_draw_end.gml"),EventType.Draw,(uint)EventSubtypeDraw.DrawEnd);
        }
        void Marker(string name,string tag) {
            var obj=Msl.GetObject(name);obj.ParentId=Msl.GetObject("o_position_starter");obj.Visible=false;
            set(obj,"event_inherited(); position_tag = "+NativeDocuments.Quote(tag)+";",EventType.Create,0);
        }
        foreach(var b in Items("buildings")) {
            var id=S(b,"id");var building=Msl.GetObject(Obj("building_"+id));building.ParentId=null;building.Sprite=Msl.GetSprite(Art(S(b,"source")));building.Visible=true;
            set(building,"depth=-y;",EventType.Create,0);
            set(building,"draw_self();",EventType.Draw,0);
            Door(Obj("door_"+id),S(b,"target"),S(b,"tag"),S(b,"cn"),S(b,"en"),true);
            Marker(Obj("start_"+id),S(b,"return_tag"));
        }
        foreach(var p in Items("props")) {
            var obj=Msl.GetObject(Obj(S(p,"id")));obj.ParentId=null;obj.Sprite=Msl.GetSprite(Art(S(p,"source")));obj.Visible=true;
            set(obj,"depth="+(p.GetProperty("floor").GetBoolean()?"1":"-y")+";",EventType.Create,0);
            set(obj,"draw_self();",EventType.Draw,0);
        }
        foreach(var d in Items("interior_returns")) {
            Door(S(d,"object"),Sites,S(d,"tag"),"灰堤外院","Ash dike forecourt");
            // Interior return must not restore world localX/Y. The native alarm
            // resolves the dedicated exterior arrival marker instead.
            set(Msl.GetObject(S(d,"object")),"event_inherited();",EventType.Step,0);
            set(Msl.GetObject(S(d,"object")),"event_inherited();",EventType.Alarm,7);
        }
        Door("o_eao_n2_entry",Sites,"EAO_SITE_in","灰堤外院","Ash dike forecourt");
        Door(Obj("home"),"r_DockStore1floor","NA","返回来路","Return the way you came");
        set(Msl.GetObject(Obj("home")),"event_inherited(); if (ds_map_exists(global.characterDataMap,\"EAO_N1_origin_room\")) { var _r=asset_get_index(ds_map_find_value(global.characterDataMap,\"EAO_N1_origin_room\")); if(room_exists(_r)) target=_r; }",EventType.Step,0);
        set(Msl.GetObject(Obj("home")),files.GetCode("night_return_alarm.gml"),EventType.Alarm,7);
        Marker(Obj("start_in"),S(Layout.GetProperty("arrival"),"tag"));
        var floor=Msl.GetObject(Obj("floor"));floor.Visible=true;
        set(floor,"depth=100;",EventType.Create,0);
        var draw=new StringBuilder();
        foreach(var layer in new[]{"backing","floor","structure"})draw.AppendLine("draw_sprite("+Hd2dArt.Sprite("n2site__"+layer)+",0,0,0);");
        set(floor,draw.ToString(),EventType.Draw,0);
        var hub=Msl.GetRoom(Sites);
        if(hub.GameObjects.Count==0) {
            var source=Msl.GetRoom("r_DockStore1floor");
            foreach(var id in new[]{"o_controller","o_dialog_controller","o_generationController"}) {
                var original=source.GameObjects.Single(i=>i.ObjectDefinition.Name.Content==id);
                hub.AddGameObject("Controllers",id,id=="o_controller"?original.CreationCode:null,x:(int)original.X,y:(int)original.Y);
            }
            Place(hub,Obj("floor"),0,0,"EAO_Floor",true);
            var cells=Cells();
            for(var x=0;x<52;x++)for(var y=0;y<38;y++)if(!cells.Contains((x,y)))Place(hub,"o_hut_wall",x,y,"Collisions",true);
            foreach(var b in Items("buildings")) {
                Place(hub,Obj("building_"+S(b,"id")),b.GetProperty("door_cell"));
                Place(hub,Obj("door_"+S(b,"id")),b.GetProperty("door_cell"));
                Place(hub,Obj("start_"+S(b,"id")),b.GetProperty("return_cell"),"Controllers");
            }
            Place(hub,Obj("home"),Layout.GetProperty("home_cell"));
            Place(hub,Obj("start_in"),Layout.GetProperty("arrival").GetProperty("cell"),"Controllers");
            Place(hub,"o_abstract_player",Layout.GetProperty("arrival").GetProperty("cell"),"Controllers");
        }
        foreach(var p in Items("props"))Place(Msl.GetRoom(S(p,"room")),Obj(S(p,"id")),p.GetProperty("cell"));
        foreach(var d in Items("interior_returns"))if(!d.GetProperty("existing").GetBoolean())Place(Msl.GetRoom(S(d,"room")),S(d,"object"),d.GetProperty("cell"));
    }
}
