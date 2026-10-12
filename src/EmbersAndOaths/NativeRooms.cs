using System;
using System.Collections;
using System.Linq;
using System.Reflection;
using ModShardLauncher;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Build independent rooms from the installed native warehouse geometry.
// Never edit the original room, object, texture, or creation-code resources.
internal static class NativeRooms
{
    internal const string Warehouse = "r_eao_d01_warehouse";
    internal const string Archive = "r_eao_d01_archive";
    internal static T Copy<T>(T source) where T : new()
    {
        var target = new T();
        foreach (var property in typeof(T).GetProperties(BindingFlags.Instance | BindingFlags.Public)) {
            if (!property.CanRead || !property.CanWrite || property.GetIndexParameters().Length != 0 || property.Name.StartsWith("Parent")) continue;
            var value = property.GetValue(source);
            if (value is IEnumerable && value is not string) continue;
            property.SetValue(target, value);
        }
        return target;
    }
    internal static void Build()
    {
        var warehouse = BuildRoom("r_DockStore1floor", Warehouse, "外港封账仓");
        var archive = BuildRoom("r_DockStore2floor", Archive, "封账仓档案室");
        Add(warehouse, "o_eao_d01_return", 326, 476);
        Add(warehouse, "o_eao_d01_archive_door", 354, 335);
        Add(warehouse, "o_eao_d01_clerk", 430, 378);
        Add(warehouse, "o_eao_d01_start", 325, 454);
        Add(warehouse, "o_eao_d01_down_start", 351, 350);
        Add(archive, "o_eao_d01_down", 374, 298);
        Add(archive, "o_eao_d01_archive_start", 351, 298);
        Add(archive, "o_loot_eao_manifest", 455, 325);
        Add(archive, "o_loot_eao_packing", 507, 325);
        Add(archive, "o_loot_eao_seal", 559, 325);
        foreach (var room in new[] { warehouse, archive }) {
            var player = room.GameObjects.Single(i => i.ObjectDefinition.Name.Content == "o_abstract_player");
            room.GameObjects.Remove(player); room.GameObjects.Add(player);
            var layer = room.Layers.Single(l => l.LayerType == UndertaleRoom.LayerType.Instances && l.InstancesData.Instances.Contains(player));
            layer.InstancesData.Instances.Remove(player); layer.InstancesData.Instances.Add(player);
        }
    }
    internal static void Prepare()
    {
        BuildRoom("r_DockStore1floor", Warehouse, "外港封账仓");
        BuildRoom("r_DockStore2floor", Archive, "封账仓档案室");
    }
    private static UndertaleRoom BuildRoom(string sourceName, string name, string caption)
    {
        var data = DataLoader.data;
        var existing = data.Rooms.SingleOrDefault(r => r.Name.Content == name);
        if (existing != null) return existing; // Stable room indices when updating a saved build.
        var source = Msl.GetRoom(sourceName);
        if (source.Tiles.Count != 0 || source.Layers.Any(l => l.LayerType != UndertaleRoom.LayerType.Instances && l.LayerType != UndertaleRoom.LayerType.Background))
            throw new InvalidOperationException("Native warehouse template layout changed.");
        var room = Copy(source);
        room.Name = data.Strings.MakeString(name);
        room.Caption = data.Strings.MakeString(caption);
        room.CreationCodeId = null;
        room.Persistent = false;
        room.Views.Clear(); room.Backgrounds.Clear(); room.GameObjects.Clear(); room.Layers.Clear();
        foreach (var view in source.Views) room.Views.Add(Copy(view));
        foreach (var background in source.Backgrounds) { var copy = Copy(background); copy.ParentRoom = room; room.Backgrounds.Add(copy); }
        data.Rooms.Add(room);
        foreach (var sourceLayer in source.Layers) {
            UndertaleRoom.Layer layer;
            if (sourceLayer.LayerType == UndertaleRoom.LayerType.Background) {
                layer = room.AddLayerBackground(sourceLayer.LayerName.Content);
                layer.Data = Copy(sourceLayer.BackgroundData);
            } else {
                layer = room.AddLayerInstance(sourceLayer.LayerName.Content);
                foreach (var instance in sourceLayer.InstancesData.Instances) {
                    var objName = instance.ObjectDefinition.Name.Content;
                    if (sourceLayer.LayerName.Content is "NPC" or "Targets" || sourceLayer.LayerName.Content.StartsWith("RandomTrader")) continue;
                    if (sourceLayer.LayerName.Content == "Controllers" && objName is not ("o_controller" or "o_dialog_controller" or "o_generationController" or "o_abstract_player")) continue;
                    if (objName.StartsWith("o_npc_") || objName.StartsWith("o_loot_") || objName == "o_position_starter" || IsTransition(instance.ObjectDefinition) || objName is "o_chest" or "o_nightstand01" or "o_nightstand03" or "o_door_presset") continue;
                    var copy = Copy(instance);
                    copy.InstanceID = data.GeneralInfo.LastObj++;
                    // Keep the native house initialization; decorative custom loot/schedules are discarded.
                    copy.CreationCode = objName == "o_controller" ? instance.CreationCode : null;
                    copy.PreCreateCode = null;
                    room.GameObjects.Add(copy);
                    layer.InstancesData.Instances.Add(copy);
                }
            }
            layer.LayerDepth = sourceLayer.LayerDepth;
            layer.XOffset = sourceLayer.XOffset;
            layer.YOffset = sourceLayer.YOffset;
            layer.IsVisible = sourceLayer.IsVisible;
        }
        return room;
    }
    private static bool IsTransition(UndertaleGameObject obj)
    {
        for (var current = obj; current != null; current = current.ParentId)
            if (current.Name.Content == "o_transitions_door") return true;
        return false;
    }
    private static void Add(UndertaleRoom room, string obj, int x, int y)
    {
        if (room.GameObjects.Any(i => i.ObjectDefinition.Name.Content == obj)) return;
        room.AddGameObject("Controllers", obj, x: x, y: y);
    }
}
