using System.IO;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Decompiler;

// Candidate data/interface checks against the approved layout. These prove the
// serialized inputs and authored coarse connectivity, not GameMaker execution.
internal static class EaoEastRegionChecks
{
    internal static string[] Validate(UndertaleData data)
    {
        var checks=new List<string>();
        void Need(bool value,string name){if(!value)throw new InvalidDataException(name);checks.Add(name);}
        string Asm(string name){var c=data.Code.Single(c=>c.Name.Content==name);return c.Disassemble(data.Variables,data.CodeLocals.For(c));}
        var cache=Asm("gml_GlobalScript_scr_globalmapCacheInit");
        var expected=new[]{"^^^^^^^^","^^^^^^^^","^^^^^^^^","^^pp^^^^","^pppp^^^","pppppp^^","mmpppp^^","mmmpprp^","mmmmprp^","^mmmmrp^","^mmmmrm^","^mmmsrm^","^msssrs^","sssssrss","sssssrss","sssssrs~","sss~s~~~","~~~~~~~~","~~~~~~~~"};
        var rows=Regex.Matches(cache,"push\\.s \"([\\^pmrs~]{8})\"").Select(m=>m.Groups[1].Value).Reverse().ToArray();
        Need(rows.SequenceEqual(expected),"east-region-compiled-nineteen-rows-match-approved-layout");
        char Cell(int x,int y)=>x>=48 ? y<35?'^':'~' : y>=22&&y<=40?rows[y-22][x-40]:y<22?'^':'~';
        var room=data.Rooms.Single(r=>r.Name.Content=="r_GlobalMap");
        var paper=room.Layers.Single(l=>l.LayerName.Content=="map_eao_east");
        Need(paper.TilesData!=null&&paper.TilesData.TilesX==127&&paper.TilesData.TilesY==79,"east-region-owned-paper-layer-native-size");
        Need(paper.TilesData!.TileData.SelectMany((r,y)=>r.Select((v,x)=>v==((x>=117&&x<=124&&y>=47&&y<=62)?1u:0u))).All(v=>v),"east-region-owned-paper-layer-exact-region-only");
        foreach(var layer in room.Layers.Where(l=>l.TilesData!=null&&l.LayerName.Content!="map_eao_east")) {
            var valid=true;
            for(var x=119;x<127;x++)for(var y=0;y<79;y++) {
                var cell=Cell(x-77,y-22);
                uint value=layer.LayerName.Content switch {
                    "Biomes"=>cell switch{'^'=>7u,'~'=>8u,'p'=>3u,'m'=>1u,'r' when y-22<33=>1u,_=>2u},
                    "Steppe"=>cell=='s'||cell=='r'&&y-22>=33?15u:0u,
                    "Sea"=>cell=='~'?15u:0u,_=>0u};
                valid &= layer.TilesData.TileData[y][x]==value;
            }
            Need(valid,"east-region-appended-editor-cells-"+layer.LayerName.Content);
        }
        var land=new HashSet<(int x,int y)>();
        for(var y=22;y<=40;y++)for(var x=40;x<=47;x++)if(Cell(x,y) is not ('^' or '~'))land.Add((x,y));
        Need(land.Count==83,"east-region-eighty-three-planned-land-and-river-cells");
        var queue=new Queue<(int x,int y)>();var seen=new HashSet<(int x,int y)>();queue.Enqueue((40,35));
        while(queue.Count>0){var p=queue.Dequeue();if(!land.Contains(p)||!seen.Add(p))continue;foreach(var d in new[]{(1,0),(-1,0),(0,1),(0,-1)})queue.Enqueue((p.x+d.Item1,p.y+d.Item2));}
        Need(seen.SetEquals(land),"east-region-all-planned-ground-connected-to-west-entry");
        Need(new[]{(43,37),(44,38),(41,33),(42,32),(45,36)}.All(land.Contains),"east-region-five-final-task-coordinates-reserved-as-ground");
        foreach(var key in new[]{"SpawnerSettings","AmbushChance","LevelRange","Wilderness","Influence","NpcSpawnChance","presetSeed","growSeed","mobsSeed","containersSeed"})
            Need(cache.Contains('"'+key+'"'),"east-region-native-tile-field-"+key);
        Need(cache.Contains("ds_map_copy")&&cache.Contains("ds_map_add_map"),"east-region-spawner-child-map-ownership-independent");
        foreach(var name in new[]{"astarCaravanGrid","astarCartGrid","roadCollisionGrid"})
            Need(cache.Contains("global."+name),"east-region-expands-native-path-grid-"+name);
        Need(cache.Contains("buffer_create")&&cache.Contains("buffer_get_address")&&cache.Contains("buffer_delete")&&cache.Contains("astar_get_weight")&&cache.Contains("astar_add_cell")&&cache.Contains("weight_grid")&&!cache.Contains("astar_grid_destroy"),"east-region-rebuilds-native-buffers-and-retains-original-weights");
        Need(cache.IndexOf("buffer_create",StringComparison.Ordinal)<cache.IndexOf("global.globalmapCacheMap",StringComparison.Ordinal),"east-region-path-grid-expansion-precedes-native-cache-return");
        Need(cache.Contains("self._eao_ds_grids")||cache.Contains("local._eao_ds_grids"),"east-region-keeps-native-grid-struct-identity");
        Need(cache.Contains("local._eao_steppe_frame")&&cache.Contains("scr_globaltile_get"),"east-region-native-steppe-corner-blend");
        var init=Asm("gml_Object_o_globalmap_controller_Other_19");
        Need(init.IndexOf("scr_globalmapCacheInit",StringComparison.Ordinal)<init.IndexOf("scr_globalmapFogInit",StringComparison.Ordinal)&&init.IndexOf("scr_globalmapPaperInit",StringComparison.Ordinal)<init.IndexOf("scr_glmap_caravanAstarGridUpdate",StringComparison.Ordinal),"east-region-native-fog-paper-and-path-weight-order-retained");
        Need(cache.Contains("scr_glmap_findShoreTile")&&cache.Contains("ShoreDirection")&&cache.Contains("scr_glmap_findRoadTile")&&cache.Contains("EAO_east_road_join_y"),"east-region-native-shore-road-and-real-west-join-data");
        Need(cache.Contains("\"BridgeWoodV01\"")&&!cache.Contains("\"BridgeWoodH01\""),"east-region-vertical-river-uses-east-west-walking-bridge");
        foreach(var name in new[]{"r_field","r_pineforest","r_steppe","r_SeaShore_North01","r_SeaShore_East01","r_SeaShore_SouthWest","r_River_BridgeWood_vertical_01"}) {
            var native=data.Rooms.Single(r=>r.Name.Content==name);
            Need(native.Width==2340&&native.Height==2340,"east-region-native-full-size-room-"+name);
        }
        Need(cache.Contains("r_eao_n2_world")&&!cache.Contains("r_eao_n1_yard")&&!cache.Contains("r_eao_fx_quarry"),"east-region-retains-pilot-room-without-faking-final-scene-migrations");
        Need(!cache.Contains("call.i random")&&!cache.Contains("call.i irandom")&&!cache.Contains("random_set_seed")&&!cache.Contains("scr_atr_set_simple")&&!cache.Contains("room_goto"),"east-region-no-rng-consumption-save-write-or-live-player-relocation");
        var ridge=data.Sprites.Single(s=>s.Name.Content=="s_eao_east_ridge_paper");
        var original=data.Sprites.Single(s=>s.Name.Content=="s_gmount01_paper").Textures[3].Texture;
        Need(ridge.Width==52&&ridge.Height==52&&ridge.Textures.Count==6&&ridge.Textures.All(t=>t.Texture.TexturePage==original.TexturePage&&t.Texture.SourceX>=original.SourceX&&t.Texture.SourceY>=original.SourceY&&t.Texture.SourceX+t.Texture.SourceWidth<=original.SourceX+original.SourceWidth&&t.Texture.SourceY+t.Texture.SourceHeight<=original.SourceY+original.SourceHeight),"east-region-paper-ridge-references-native-atlas-crops-only");
        Need(cache.Contains("global.glmapBatchArrayPaperMountBottom")&&cache.Contains("global.glmapBatchArrayPaperGround"),"east-region-clears-old-border-decals-in-normal-and-paper-batches");
        return checks.ToArray();
    }
}
