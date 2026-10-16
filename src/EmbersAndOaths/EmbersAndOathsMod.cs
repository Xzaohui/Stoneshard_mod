using System;
using System.Linq;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

/// <summary>Development build for the user's current Stoneshard installation.</summary>
public sealed class EmbersAndOathsMod : Mod
{
    public override string Name => "余烬与誓约（开发版）";
    public override string Author => "Stoneshard_mod project";
    public override string Version => "0.3.27";
    public override string TargetVersion => "0.9.4.25";
    public override string ShortDesc => "无钟之夜＋灰堤＋布林试点 · HD2D开发观察模式";
    public override string Description => "旧文书查档任务退役；无钟之夜包含现场探索、失踪者反转与两条可执行的处理路线；灰堤没有墓碑（N2）五桩五键与HD2D素材；0.3.4 试点批次P2/P3：布林租约案CS-BRY-01（十四桩十键、服务班SVC-BRY、信任档与分池闲谈）与野外层FX-QRY（石场看守存在性四态、只读文书、观察迹象、地区池）。原存档资源保留，F8地图测试保留；0.3.5 新增灰堤外院、三处原生建筑门与室内陈设；完整回归仍在开发。";

    public override void PatchMod()
    {
        var data = DataLoader.data;
        if (!data.Strings.Any(s => s.Content == TargetVersion))
            throw new InvalidOperationException("This build requires Stoneshard 0.9.4.25 modbranch.");
        if (data.GameObjects.Any(o => o.Name.Content == "o_eao_controller"))
            throw new InvalidOperationException("EAO was already applied. Rebuild from the pre-EAO combination backup or a fresh MSL build.");
        foreach (var name in new[] { "gml_Object_o_gameLoader_Create_0", "gml_GlobalScript_scr_quest_get_complete", "gml_GlobalScript_scr_caravanPositionGetDistance", "gml_GlobalScript_scr_characterMapInit" })
            if (!data.Code.Any(c => c.Name.Content == name)) throw new InvalidOperationException("Missing required interface: " + name);
        var boot = Msl.GetStringGMLFromFile("gml_Object_o_gameLoader_Create_0");
        var originalEntries = data.Code.ToHashSet();
        if (!boot.Contains("scr_slotsInit()") || !boot.Contains("scr_settingsInit()"))
            throw new InvalidOperationException("Boot interface changed; refusing an unsafe patch.");

        // The user explicitly requested development in the current installation and save namespace.
        var controller = Msl.AddObject("o_eao_controller", isVisible: true, isPersistent: true);
        var courier = Msl.AddObject("o_eao_courier", spriteName: "s_peasantmale_13", isVisible: true);
        ConfigureEvents(controller, courier);
        Msl.SetStringGMLInFile(boot + "\nif (!instance_exists(o_eao_controller)) instance_create_depth(0, 0, -100000, o_eao_controller);", "gml_Object_o_gameLoader_Create_0");
        // MSL AddCode compiles before appending its parent. Nested method entries can therefore
        // precede the new parent in CODE, which the 0.6.1 reader cannot deserialize.
        var additions = data.Code.Where(c => !originalEntries.Contains(c)).ToArray();
        foreach (var entry in additions) data.Code.Remove(entry);
        var emitted = originalEntries;
        void Emit(UndertaleCode entry) {
            if (emitted.Contains(entry)) return;
            if (entry.ParentEntry != null) Emit(entry.ParentEntry);
            data.Code.Add(entry);
            emitted.Add(entry);
        }
        foreach (var entry in additions) Emit(entry);
    }

    /// <summary>Update the recognized existing prototype without replacing other Mods.</summary>
    public void UpdatePrototype()
    {
        if (!DataLoader.data.Strings.Any(s => s.Content == TargetVersion)) throw new InvalidOperationException("Unsupported game version.");
        ConfigureEvents(Msl.GetObject("o_eao_controller"), Msl.GetObject("o_eao_courier"));
        // The 0.6.1 reader associates child offsets with the preceding parent.
        // Keep each EAO event and all its children contiguous after an update.
        var events = DataLoader.data.Code.Where(c => c.ParentEntry == null && (c.Name.Content.StartsWith("gml_Object_o_eao_") || c.Name.Content.StartsWith("gml_Object_o_inv_eao_") || c.Name.Content.StartsWith("gml_Object_o_loot_eao_"))).ToArray();
        var children = DataLoader.data.Code.Where(c => c.ParentEntry != null && events.Contains(c.ParentEntry)).ToArray();
        foreach (var entry in events.Concat(children)) DataLoader.data.Code.Remove(entry);
        foreach (var entry in events) {
            DataLoader.data.Code.Add(entry);
            foreach (var child in children.Where(c => c.ParentEntry == entry).OrderBy(c => c.Offset)) DataLoader.data.Code.Add(child);
        }
    }

    private void ConfigureEvents(UndertaleGameObject controller, UndertaleGameObject courier)
    {
        // Allocate both sides before compilation: native save/drop/pickup resolves
        // o_inv_<idName> and o_loot_<idName> by their stable resource names.
        foreach (var doc in NativeDocuments.All) {
            Msl.AddObject("o_inv_" + doc.Id, spriteName: "s_inv_note", parentName: "o_inv_book", isVisible: true);
            Msl.AddObject("o_loot_" + doc.Id, spriteName: "s_loot_note", parentName: "o_consument_loot", isVisible: true);
        }
        // Room constants must exist before compiling target/room comparisons.
        NativeRooms.Prepare();
        NightQuest.Prepare();
        N2Quest.Prepare();
        CityQuest.Prepare();
        FieldQuest.Prepare();
        SceneAssembly.Prepare();
        EastSites.Prepare();
        GroundChunks.Prepare();
        DevTools.Prepare();
        N1DoorwayArt.Ensure();
        Msl.AddObject("o_eao_d01_clerk", spriteName: "s_peasantmale_13", parentName: "o_simple_NPC", isVisible: true);
        foreach (var pair in new[] { ("o_eao_d01_entry", "o_Doors_all_small"), ("o_eao_d01_return", "o_Doors_all_small"), ("o_eao_d01_archive_door", "o_mannshireavern2floorladderup55"), ("o_eao_d01_down", "o_tavernladerdown01") })
            Msl.AddObject(pair.Item1, parentName: pair.Item2, isVisible: true).Sprite = Msl.GetObject(pair.Item2).Sprite;
        foreach (var name in new[] { "o_eao_d01_start", "o_eao_d01_down_start", "o_eao_d01_archive_start" }) Msl.AddObject(name, parentName: "o_position_starter", isVisible: false);
        courier.ParentId = Msl.GetObject("o_simple_NPC");
        controller.Visible = true; // The map-only F8 status uses Draw GUI; no sprite is assigned.
        void SetEvent(UndertaleGameObject obj, string code, EventType kind, uint subtype)
        {
            var existing = obj.Events[(int)kind].SingleOrDefault(e => e.EventSubtype == subtype);
            if (existing == null) Msl.AddNewEvent(obj, code, kind, subtype);
            else Msl.SetStringGMLInFile(code, existing.Actions.Single().CodeId.Name.Content);
        }
        SetEvent(controller, ModFiles.GetCode("controller_create.gml"), EventType.Create, 0);
        DevTools.Configure(SetEvent, ModFiles);
        var step = ModFiles.GetCode("controller_step.gml").Replace("// Native port-store annex:", "event_user(2); if (instance_exists(o_smoothRoomChanger)) exit;\n// Native port-store annex:");
        SetEvent(controller, GroundChunks.EnsureWorld()+ModFiles.GetCode("night_controller_step.gml"), EventType.Step, 1);
        SetEvent(controller, ModFiles.GetCode("annex_entry_spawn.gml"), EventType.Other, 14);
        SetEvent(controller, ModFiles.GetCode("test_teleport_arrival.gml"), EventType.Step, 2);
        SetEvent(controller, ModFiles.GetCode("test_teleport_step.gml"), EventType.Other, 12);
        SetEvent(controller, ModFiles.GetCode("test_teleport_toggle.gml"), EventType.KeyPress, 119);
        SetEvent(controller, ModFiles.GetCode("test_teleport_execute.gml"), EventType.Other, 13);
        var mapInteractive = Msl.GetObject("o_globalmapInteractiveNormal");
        var mapHook = mapInteractive.Events[(int)EventType.Other].SingleOrDefault(e => e.EventSubtype == 20);
        if (mapHook != null && (!DataLoader.data.Code.Any(c => c.Name.Content == TestTeleport.MapHook) || !Msl.GetStringGMLFromFile(TestTeleport.MapHook).Contains("EAO_test_map_pending")))
            throw new InvalidOperationException("Map User 10 is already owned by another modification.");
        SetEvent(mapInteractive, ModFiles.GetCode("test_teleport_map_click.gml"), EventType.Other, 20);
        var changer = Msl.GetObject("o_smoothRoomChanger");
        var commitHook = changer.Events[(int)EventType.Other].SingleOrDefault(e=>e.EventSubtype==20);
        if(commitHook != null && !Msl.GetStringGMLFromFile("gml_Object_o_smoothRoomChanger_Other_20").Contains("EAO_test_map_commit"))
            throw new InvalidOperationException("Room changer User 10 is already owned by another modification.");
        SetEvent(changer, ModFiles.GetCode("test_teleport_commit.gml"), EventType.Other, 20);
        SetEvent(controller, ModFiles.GetCode("controller_draw_gui.gml"), EventType.Draw, 64);
        SetEvent(controller, ModFiles.GetCode("controller_close.gml"), EventType.Other, 10);
        SetEvent(controller, "if (instance_exists(test_guide_id)) instance_destroy(test_guide_id); test_guide_id = noone;", EventType.Other, 11);
        SetEvent(controller, "event_user(0); event_user(1);", EventType.Other, 5); // Room End
        SetEvent(controller, "event_user(0); event_user(1);", EventType.CleanUp, 0);
        foreach (var doc in NativeDocuments.All) {
            var inventory = Msl.GetObject("o_inv_" + doc.Id);
            var loot = Msl.GetObject("o_loot_" + doc.Id);
            inventory.ParentId = Msl.GetObject("o_inv_book");
            loot.ParentId = Msl.GetObject("o_consument_loot");
            SetEvent(inventory, NativeDocuments.InventoryCreate(doc), EventType.Create, 0);
            SetEvent(inventory, NativeDocuments.ReadCode(doc), EventType.Other, 24);
            SetEvent(loot, NativeDocuments.LootCreate(doc), EventType.Create, 0);
        }
        SetEvent(courier, ModFiles.GetCode("courier_create.gml") + NativeDocuments.RegistrationCode() + NativeDialogue.ActionsCode() + NativeDialogue.DataCode(), EventType.Create, 0);
        SetEvent(courier, "event_inherited();", EventType.Draw, 0);
        SetEvent(courier, "event_inherited();", EventType.Mouse, 4);
        // Preserve the legacy resource index without ever spawning a guide again.
        var guide = DataLoader.data.GameObjects.SingleOrDefault(o=>o.Name.Content=="o_eao_test_guide");
        if(guide != null) {
            SetEvent(guide, "instance_destroy();", EventType.Create, 0);
            SetEvent(guide, "exit;", EventType.Mouse, 4);
            SetEvent(guide, "exit;", EventType.Draw, 0);
            guide.Visible = false;
        }
        var clerk = Msl.AddObject("o_eao_d01_clerk", spriteName: "s_peasantmale_13", parentName: "o_simple_NPC", isVisible: true);
        SetEvent(clerk, ModFiles.GetCode("courier_create.gml").Replace("路誓行会信使", "封账仓仓务员").Replace("Roadsworn courier", "Warehouse clerk").Replace("eao_mq01", "eao_mq02") + NativeDocuments.RegistrationCode() + WarehouseQuest.ActionsCode() + WarehouseQuest.DataCode(), EventType.Create, 0);
        SetEvent(clerk, "event_inherited();", EventType.Mouse, 4);
        SetEvent(clerk, "event_inherited();", EventType.Draw, 0);
        void Door(string name, string template, string target, string tag) {
            var original = Msl.GetObject(template);
            var obj = Msl.AddObject(name, parentName: template, isVisible: true);
            obj.Sprite = original.Sprite;
            SetEvent(obj, "event_inherited(); target = " + target + "; position_tag = " + NativeDocuments.Quote(tag) + "; is_lock = false; is_crime_door = false; dungeon_level_incr = 0;", EventType.Create, 0);
        }
        Door("o_eao_d01_entry", "o_Doors_all_small", NativeRooms.Warehouse, "EAO_D01_enter");
        SetEvent(Msl.GetObject("o_eao_d01_entry"), ModFiles.GetCode("annex_entry_gate.gml"), EventType.Step, 0);
        SetEvent(Msl.GetObject("o_eao_d01_entry"), ModFiles.GetCode("annex_entry_draw.gml"), EventType.Draw, 0);
        Door("o_eao_d01_return", "o_Doors_all_small", "r_DockStore1floor", "DockStore01_01");
        SetEvent(Msl.GetObject("o_eao_d01_return"), TestTeleport.ReturnAlarm, EventType.Alarm, 7);
        Door("o_eao_d01_archive_door", "o_mannshireavern2floorladderup55", NativeRooms.Archive, "EAO_D01_archive");
        Door("o_eao_d01_down", "o_tavernladerdown01", NativeRooms.Warehouse, "EAO_D01_down");
        SetEvent(Msl.GetObject("o_eao_d01_archive_door"), "event_inherited(); is_lock = !ds_map_exists(global.characterDataMap, \"EAO_MQ02\") || ds_map_find_value(global.characterDataMap, \"EAO_MQ02\") < 1; LVL = 100; speech_key = \"door_barred\";", EventType.Step, 0);
        foreach (var marker in new[] { ("o_eao_d01_start", "EAO_D01_enter"), ("o_eao_d01_down_start", "EAO_D01_down"), ("o_eao_d01_archive_start", "EAO_D01_archive") }) {
            var obj = Msl.AddObject(marker.Item1, parentName: "o_position_starter", isVisible: false);
            SetEvent(obj, "event_inherited(); position_tag = " + NativeDocuments.Quote(marker.Item2) + ";", EventType.Create, 0);
        }
        NightQuest.Configure(SetEvent, ModFiles);
        N2Quest.Configure(SetEvent, ModFiles);
        CityQuest.Configure(SetEvent, ModFiles);
        FieldQuest.Configure(SetEvent, ModFiles);
        N2Hd2dArt.Configure(SetEvent, ModFiles);
        SceneAssembly.Configure(SetEvent, ModFiles);
        N2Hd2dArt.ConfigureDoorwayMasks();
        N1DoorwayArt.Configure(SetEvent, ModFiles);
        GroundChunks.Configure(SetEvent);
        // F4 cycles the dev-only Brynn trust-band override while F6 is on.
        SetEvent(controller, ModFiles.GetCode("cs_trust_toggle.gml"), EventType.KeyPress, 115);
        EastPilot.Configure(SetEvent, ModFiles);
        NativeRooms.Build();
    }
}
