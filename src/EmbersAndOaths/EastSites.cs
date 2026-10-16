using System;
using System.Linq;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// A real 90x90 world surface. The old 52x38 exterior remains a separate,
// addressable legacy room; it is never used as a world-grid substitute.
internal static class EastSites
{
    internal const string Room = "r_eao_n2_world";
    internal const string Generator = "o_eao_east_steppe_generator";

    internal static void Prepare()
    {
        var generator = Msl.AddObject(Generator, parentName: "o_prairieGenerationController", isVisible: false);
        generator.ParentId = Msl.GetObject("o_prairieGenerationController");
        generator.Sprite = null;
        if (DataLoader.data.Rooms.Any(r => r.Name.Content == Room)) return;
        var source = Msl.GetRoom("r_steppe");
        if (source.Width != 90 * 26 || source.Height != 90 * 26 || source.Tiles.Count != 0 ||
            source.Layers.Any(l => l.LayerType is not (UndertaleRoom.LayerType.Instances or UndertaleRoom.LayerType.Background)))
            throw new InvalidOperationException("Native steppe room changed; refusing an incompatible surface.");
        var room = NativeRooms.Copy(source);
        room.Name = DataLoader.data.Strings.MakeString(Room);
        room.Caption = DataLoader.data.Strings.MakeString("灰堤草原与工营");
        room.Persistent = false;
        room.Views.Clear(); room.Backgrounds.Clear(); room.GameObjects.Clear(); room.Layers.Clear();
        foreach (var view in source.Views) room.Views.Add(NativeRooms.Copy(view));
        foreach (var bg in source.Backgrounds) {
            var copy = NativeRooms.Copy(bg); copy.ParentRoom = room; room.Backgrounds.Add(copy);
        }
        DataLoader.data.Rooms.Add(room);
        var layers = source.Layers.ToDictionary(l => l, l => l.LayerType == UndertaleRoom.LayerType.Background
            ? room.AddLayerBackground(l.LayerName.Content) : room.AddLayerInstance(l.LayerName.Content));
        foreach (var original in source.Layers) {
            var layer = layers[original];
            layer.LayerDepth = original.LayerDepth; layer.XOffset = original.XOffset;
            layer.YOffset = original.YOffset; layer.IsVisible = original.IsVisible;
            if (original.LayerType == UndertaleRoom.LayerType.Background) {
                layer.Data = NativeRooms.Copy(original.BackgroundData);
                continue;
            }
        }
        // GameMaker's room instance creation order and the per-layer draw lists
        // are independent. Preserve both; grouping instances by layer can start
        // the generator before the native controller has initialized its grids.
        var copies = source.GameObjects.ToDictionary(i => i, i => NativeRooms.Copy(i));
        foreach (var instance in source.GameObjects) {
            var copy = copies[instance];
            copy.InstanceID = DataLoader.data.GeneralInfo.LastObj++;
            if (copy.ObjectDefinition.Name.Content == "o_prairieGenerationController") copy.ObjectDefinition = generator;
            room.GameObjects.Add(copy);
        }
        foreach (var original in source.Layers.Where(l => l.LayerType == UndertaleRoom.LayerType.Instances))
            foreach (var instance in original.InstancesData.Instances) layers[original].InstancesData.Instances.Add(copies[instance]);
    }

    internal static void Configure(Action<UndertaleGameObject, string, EventType, uint> set, ModFile files)
    {
        // Native generation calls User 8 after roads and before flora/mobs. Reserve
        // the authored work area in its placement grid without changing walkability.
        set(Msl.GetObject(Generator), files.GetCode("east_sites_preset.gml"), EventType.Other, 18);
        foreach (var id in new[] { "shed", "winch", "canal" })
            set(Msl.GetObject("o_eao_site_door_" + id), files.GetCode("east_sites_enter.gml"), EventType.Alarm, 7);
        foreach (var name in new[] { "o_eao_n2_home", "o_eao_site_winch_back", "o_eao_site_canal_back" })
            set(Msl.GetObject(name), files.GetCode("east_sites_return.gml"), EventType.Step, 0);
    }
}
