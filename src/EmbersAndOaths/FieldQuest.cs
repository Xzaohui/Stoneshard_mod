using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Pilot batch P3 (MGMT-PILOT-FX-S157): the field layer. FX-QRY the quarry
// keeper with the four presence states and conditional revisits, the DOC-PLG
// read-only document, the SGN-BR1 observation sign and the ambient region
// pool. The quarry yard is a self-built scene entered from Brynn's
// south-west quarter; real per-site placement stays open (OI-06).
internal static class FieldQuest
{
    internal const string Quarry = "r_eao_fx_quarry";
    internal const int Columns = 40, Rows = 30, Tile = 26;
    // Inclusive native grid cells; the sole source of floors, collisions and
    // exported layout checks, exactly like the N1/N2 scenes.
    internal static readonly Dictionary<string, (int, int, int, int)[]> Shapes = new() {
        [Quarry] = new[] { (4, 5, 14, 12), (14, 13, 27, 24), (28, 8, 35, 22) }
    };
    internal static HashSet<(int, int)> Cells()
    {
        var cells = new HashSet<(int, int)>();
        foreach (var r in Shapes[Quarry]) for (var x = r.Item1; x <= r.Item3; x++) for (var y = r.Item2; y <= r.Item4; y++) cells.Add((x, y));
        return cells;
    }

    internal static void PrepareRooms()
    {
        foreach (var n in Shapes.Keys) {
            if (DataLoader.data.Rooms.Any(r => r.Name.Content == n)) continue;
            var source = Msl.GetRoom("r_DockStore1floor"); var room = NativeRooms.Copy(source);
            room.Name = DataLoader.data.Strings.MakeString(n); room.Caption = DataLoader.data.Strings.MakeString("废弃石场");
            room.Width = Columns * Tile; room.Height = Rows * Tile; room.Persistent = false; room.CreationCodeId = null;
            room.Views.Clear(); foreach (var view in source.Views) room.Views.Add(NativeRooms.Copy(view));
            room.GameObjects.Clear(); room.Layers.Clear(); room.Backgrounds.Clear(); room.Tiles.Clear();
            DataLoader.data.Rooms.Add(room);
            room.AddLayerInstance("Controllers").LayerDepth = -4000;
            room.AddLayerInstance("Collisions").LayerDepth = -3900;
            room.AddLayerInstance("Story").LayerDepth = -500;
            room.AddLayerInstance("EAO_Floor").LayerDepth = 100;
        }
    }
    private static void Add(UndertaleRoom r, string obj, int cx, int cy, string layer = "Story", bool corner = false)
        => r.AddGameObject(layer, obj, x: cx * Tile + (corner ? 0 : 13), y: cy * Tile + (corner ? 0 : 13));
    internal static void BuildRooms()
    {
        foreach (var name in Shapes.Keys) {
            var r = Msl.GetRoom(name); if (r.GameObjects.Count != 0) continue;
            var source = Msl.GetRoom("r_DockStore1floor");
            foreach (var id in new[] { "o_controller", "o_dialog_controller", "o_generationController" }) {
                var original = source.GameObjects.Single(i => i.ObjectDefinition.Name.Content == id);
                r.AddGameObject("Controllers", id, id == "o_controller" ? original.CreationCode : null, x: (int)original.X, y: (int)original.Y);
            }
            Add(r, "o_eao_fx_floor", 0, 0, "EAO_Floor", true);
            var cells = Cells();
            for (var x = 0; x < Columns; x++) for (var y = 0; y < Rows; y++) if (!cells.Contains((x, y))) Add(r, "o_hut_wall", x, y, "Collisions", true);
            Add(r, "o_eao_fx_back", 6, 10);
            Add(r, "o_eao_fx_keeper", 18, 13);
            Add(r, "o_eao_fx_whiteline", 20, 13);
            Add(r, "o_loot_eao_notice_plg", 8, 7);
            Add(r, "o_eao_fx_sign", 31, 10);
            Add(r, "o_candle03", 9, 10); Add(r, "o_candlefire", 9, 10);
            Add(r, "o_candle03", 29, 12); Add(r, "o_candlefire", 29, 12);
            Add(r, "o_eao_fx_start_in", 6, 10, "Controllers");
            Add(r, "o_abstract_player", 6, 10, "Controllers");
        }
    }
    internal static void Ensure()
    {
        foreach (var layer in new[] { "backing", "floor", "structure", "foreground" })
            Hd2dArt.Add("r_eao_fx_quarry__" + layer, 1040, 780, 0, 0);
    }
    internal static string DrawForeground() =>
        "if (" + Hd2dArt.Active + ") { if (room == " + Quarry + ") draw_sprite(" + Hd2dArt.Sprite(Quarry + "__foreground") + ",0,0,0); }\n";
    internal static string FloorDraw()
    {
        var code = new StringBuilder("if (" + Hd2dArt.Active + ") { if (room == " + Quarry + ") { draw_sprite(" + Hd2dArt.Sprite(Quarry + "__backing") + ",0,0,0); draw_sprite(" + Hd2dArt.Sprite(Quarry + "__floor") + ",0,0,0); draw_sprite(" + Hd2dArt.Sprite(Quarry + "__structure") + ",0,0,0); exit; } }\n");
        code.Append("var _c = draw_get_color(); var _a = draw_get_alpha(); draw_set_alpha(1); draw_set_color(make_color_rgb(19,21,20)); draw_rectangle(0,0,room_width,room_height,false);\n");
        var cells = Cells();
        code.AppendLine("if (room == " + Quarry + ") {");
        foreach (var p in cells.OrderBy(p => p.Item2).ThenBy(p => p.Item1)) {
            var px = p.Item1 * Tile; var py = p.Item2 * Tile;
            var tint = p.Item2 >= 13 && p.Item1 <= 27 ? "make_color_rgb(56,54,50)" : "make_color_rgb(62,60,55)";
            code.AppendLine($"draw_set_color({tint}); draw_rectangle({px},{py},{px+25},{py+25},false);");
            code.AppendLine($"draw_set_color(make_color_rgb(38,38,35)); draw_line({px},{py+25},{px+25},{py+25});");
            if ((p.Item1 + p.Item2) % 4 == 0) code.AppendLine($"draw_sprite_ext(s_dungeonfloor01, {(p.Item1+p.Item2)%12}, {px+13}, {py+13}, 0.25, 0.25, 0, c_white, 0.3);");
            if (!cells.Contains((p.Item1, p.Item2 - 1))) code.AppendLine($"draw_set_color(make_color_rgb(84,82,72)); draw_rectangle({px},{py-13},{px+25},{py+2},false); draw_set_color(make_color_rgb(30,31,29)); draw_line({px},{py},{px+25},{py});");
            if (!cells.Contains((p.Item1 - 1, p.Item2))) code.AppendLine($"draw_set_color(make_color_rgb(78,76,66)); draw_rectangle({px-6},{py},{px+1},{py+25},false);");
            if (!cells.Contains((p.Item1 + 1, p.Item2))) code.AppendLine($"draw_set_color(make_color_rgb(36,37,35)); draw_rectangle({px+23},{py},{px+29},{py+25},false);");
        }
        code.AppendLine("}");
        code.AppendLine("draw_set_color(_c); draw_set_alpha(_a);"); return code.ToString();
    }

    private sealed class Flow
    {
        private readonly string root, speaker;
        public Flow(string root, string speaker) { this.root = root; this.speaker = speaker; }
        public readonly Dictionary<string, object> Fragments = new();
        public readonly Dictionary<string, string[]> Lines = new();
        public readonly Dictionary<string, string> Callbacks = new();
        public void N(string key, string cn, string en, params string[] next) { Lines[key] = new[] { en, cn }; Fragments[key] = next; }
        public void P(string key, string cn, string en, string next = "@dialogue_end") { Lines[key] = new[] { en, cn }; Fragments[key] = next; }
        public void A(string key, string callback, params string[] next) { Fragments[key] = next; Callbacks[key] = callback; }
        public string Code(string resume, params string[] starts)
        {
            Fragments[root] = "instruction_" + root + "_resume";
            A("instruction_" + root + "_resume", resume, starts);
            var specs = new Dictionary<string, object> { [root] = new { hub = true } };
            foreach (var key in Lines.Keys.Where(k => k.EndsWith("_pc"))) specs[key] = new { technical = true };
            foreach (var key in Callbacks.Keys.Where(k => !k.EndsWith("_resume"))) specs[key] = new { action = true };
            return NativeDialogue.Register(new { RootFragment = root, Monologue = false, Fragments,
                Speakers = new Dictionary<string, string[]> { [speaker] = Lines.Keys.Where(k => !k.EndsWith("_pc")).ToArray(), ["Player"] = Lines.Keys.Where(k => k.EndsWith("_pc")).ToArray() }, Specs = specs, Scripts = new Dictionary<string, string>() }, Lines, Callbacks);
        }
    }

    private static string KeeperResume() =>
        "eao_fx_keeper_resume = function() {\n" +
        "var _p = \"present\";\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_presence_FX_QRY\")) _p = ds_map_find_value(global.characterDataMap, \"EAO_presence_FX_QRY\");\n" +
        "if (_p == \"absent\" || _p == \"dead\") return 6;\n" +
        "if (_p == \"refused\") return 5;\n" +
        "if (variable_global_exists(\"timeDataMap\") && is_real(global.timeDataMap) && ds_exists(global.timeDataMap, ds_type_map)) { var _h = ds_map_find_value(global.timeDataMap, \"hours\"); if (_h >= 21 || _h < 5) return 1; }\n" +
        "if (variable_global_exists(\"EAO_fx_qry_seen\") && global.EAO_fx_qry_seen) return 2;\n" +
        "return 0;\n};\n";
    private const string ChatPick =
        "eao_fx_chat_pick = function() {\n" +
        "if (!variable_global_exists(\"EAO_fx_chat_cursor\")) global.EAO_fx_chat_cursor = 0;\n" +
        "global.EAO_fx_chat_cursor = (global.EAO_fx_chat_cursor + 1) mod 3;\n" +
        "return global.EAO_fx_chat_cursor;\n};\n";
    private const string VisitPick =
        "eao_fx_visit_pick = function() {\n" +
        "var _seen = variable_global_exists(\"EAO_fx_qry_seen\") && global.EAO_fx_qry_seen;\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_resolve_N7\")) {\n" +
        "    if (ds_map_find_value(global.characterDataMap, \"EAO_resolve_N7\") != \"none\") return _seen ? 3 : 1;\n" +
        "    return _seen ? 2 : 0;\n" +
        "}\n" +
        "return 4;\n};\n";
    private const string RegionPick =
        "eao_fx_region_pick = function() {\n" +
        "if (variable_global_exists(\"timeDataMap\") && is_real(global.timeDataMap) && ds_exists(global.timeDataMap, ds_type_map)) { var _h = ds_map_find_value(global.timeDataMap, \"hours\"); if (_h >= 21 || _h < 5) return 2; }\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_resolve_N7\") && ds_map_find_value(global.characterDataMap, \"EAO_resolve_N7\") != \"none\") return 3;\n" +
        "if (!variable_global_exists(\"EAO_fx_region_cursor\")) global.EAO_fx_region_cursor = 0;\n" +
        "global.EAO_fx_region_cursor = 1 - global.EAO_fx_region_cursor;\n" +
        "return global.EAO_fx_region_cursor;\n};\n";

    private static string KeeperFlow()
    {
        var f = new Flow("eao_fx_keeper", "EAO_Keeper");
        f.N("FX_intro", "站住。坑边不许靠近，碎石头不认人。", "Halt. Keep off the pit rim. Loose stone does not care who you are.", "instruction_FX_intro");
        f.A("instruction_FX_intro", "eao_fx_qry_intro", "FX_hub");
        f.N("FX_night", "夜里别在坑边转，回声比白天吓人。", "Don't walk the rim at night. The echo outdoes the daylight.", "FX_hub");
        f.N("FX_hub", "又是你。坑里还是那副样子。", "You again. The pit looks the same as it did.", "FX_chat_pc", "FX_site_pc", "FX_task_pc", "FX_region_pc", "FX_scout_pc", "FX_bye_pc");
        f.P("FX_chat_pc", "聊聊这石场。", "Talk about the quarry.", "instruction_FX_chat_pick");
        f.A("instruction_FX_chat_pick", "eao_fx_chat_pick", "FX_chat_1", "FX_chat_2", "FX_chat_3");
        f.N("FX_chat_1", "这块岩是打边城的料。城修完了，人也就散了。", "This rock was cut for the border town. Town got built, crew got scattered.", "FX_hub");
        f.N("FX_chat_2", "凿子钝了能磨，人手散了磨不回来。", "A dull chisel can be ground. A scattered crew cannot.", "FX_hub");
        f.N("FX_chat_3", "你说要买石？今天不卖，石头还没算清是谁的。", "Buying stone? Not today. It isn't settled whose stone this is.", "FX_hub");
        f.P("FX_site_pc", "问坑边的路。", "Ask about the pit.", "FX_arrival");
        f.N("FX_arrival", "你从哪条路来的？要是西边，路上看见工头没有。", "Which road did you come by? From the west? Did you see the foreman?", "FX_hub");
        f.P("FX_task_pc", "问工账的事。", "Ask about the works accounts.", "instruction_FX_visit_pick");
        f.A("instruction_FX_visit_pick", "eao_fx_visit_pick", "FX_visit_before", "FX_visit_after", "FX_visit_early", "FX_visit_late", "FX_hub");
        f.N("FX_visit_before", "你要是替关卡来清账的，先去看坑边的白线，再来跟我说话。", "If you're here to settle accounts for the border post, read the white line first, then talk to me.", "FX_hub");
        f.N("FX_visit_after", "账清了，坑还是这个坑。石头不会因为纸清了就自己爬上来。", "Accounts are clear. The pit is the same pit. Paper doesn't lift stone.", "FX_hub");
        f.N("FX_visit_early", "你先来过石场，后来才去的关卡。那正好，我说的话你自己对得上。", "The quarry was your first stop, the post your second. Good. What I say will match what you saw.", "FX_hub");
        f.N("FX_visit_late", "关卡的事你办完了才来？行。石头的事我照旧，不问你替谁办过。", "You finished at the post before coming here? Fine. The stone stays the same; I don't ask who you worked for.", "FX_hub");
        f.P("FX_region_pc", "听听这地方的风声。", "Hear the talk of this land.", "instruction_FX_region_pick");
        f.A("instruction_FX_region_pick", "eao_fx_region_pick", "AG_R04_1", "AG_R04_2", "AG_R04_3", "AG_R04_4", "AG_R04_5");
        f.N("AG_R04_1", "关楼的石头是从坑里一块块抬上来的。抬石头的人没留下名字。", "The gate stones were carried up one by one. The carriers left no names.", "FX_hub");
        f.N("AG_R04_2", "过关要看文书，看不了的就看人。看得多了，人比纸准。", "At the pass we read papers, and when papers fail we read people. Read enough and people beat paper.", "FX_hub");
        f.N("AG_R04_3", "夜里崖上落石。听见响别抬头，往墙根靠。", "Rock falls off the cliff at night. If you hear it, do not look up - get to the wall foot.", "FX_hub");
        f.N("AG_R04_4", "军需账的事传开了以后，坑边来看热闹的人多了。看热闹不出工钱。", "Since the quartermaster ledger got around, more people come to stare at the pit. Staring pays no wages.", "FX_hub");
        f.N("AG_R04_5", "守门的肯跟你多说两句，说明你上次没给他们添乱。", "The gate men talk a while longer with you - that means last time you caused them no trouble.", "FX_hub");
        f.P("FX_scout_pc", "请她下坑探看塌方线。", "Ask her to scout below the slide line.", "instruction_FX_refusal");
        f.A("instruction_FX_refusal", "eao_fx_qry_refusal", "FX_refused_line");
        f.N("FX_refused_line", "要我替你下坑探路？不行。这坑欠我的工钱还没给。", "Climb down and scout for you? No. This pit still owes me wages.", "FX_warn_pc");
        f.N("FX_refused", "要我替你下坑探路？不行。这坑欠我的工钱还没给。", "Climb down and scout for you? No. This pit still owes me wages.", "FX_arrival_pc", "FX_warn_pc");
        f.P("FX_arrival_pc", "问坑边的路。", "Ask about the pit.", "FX_arrival");
        f.N("FX_warn_pc", "提醒塌方线。", "Mind the slide line.", "FX_warning");
        f.N("FX_warning", "再往里三丈是塌方线，我拦过三个不信的。", "Three paces in is the slide line. I've pulled three men off it who didn't believe me.", "FX_bye_pc");
        f.N("FX_proxy", "看守不在的时候，坑边只留白线；过线的人自己负责。", "Should the keeper be elsewhere, only the white line stands. Cross it and it's on you.", "FX_bye_pc");
        f.P("FX_bye_pc", "离开坑边。", "Leave the pit.");
        return f.Code("eao_fx_keeper_resume", "FX_intro", "FX_night", "FX_hub", "FX_hub", "FX_hub", "FX_refused", "FX_proxy");
    }
    private static string SignFlow()
    {
        var f = new Flow("eao_fx_sign", "EAO_Sign");
        f.N("SGN_intro", "离地一人高的抓痕，三道并排，树皮向外翻；下方落着碎蜂巢。", "Three parallel scores at shoulder height, bark curling outward; a crushed honeycomb below.", "SGN_judge_pc", "SGN_danger_pc", "SGN_bye_pc");
        f.P("SGN_judge_pc", "这痕迹说明什么？", "What do the marks tell?", "SGN_judge");
        f.N("SGN_judge", "是护崽母熊的领地标记：抓痕越高，熊越大。", "A sow bear boundary mark: the higher the scores, the bigger the bear.", "SGN_intro");
        f.P("SGN_danger_pc", "该怎么退？", "How do I back off?", "SGN_danger");
        f.N("SGN_danger", "别顺着抓痕方向走；退的时候别跑。", "Do not follow the line of the marks; back off without running.", "SGN_bye_pc");
        f.P("SGN_bye_pc", "退开。", "Back away.");
        return f.Code("eao_fx_sign_resume", "SGN_intro");
    }
    private static string WhiteLineFlow()
    {
        var f = new Flow("eao_fx_whiteline", "EAO_WhiteLine");
        f.N("WHL_intro", "看守不在的时候，坑边只留白线；过线的人自己负责。", "Should the keeper be elsewhere, only the white line stands. Cross it and it's on you.", "WHL_bye_pc");
        f.P("WHL_bye_pc", "退回白线外。", "Step back behind the line.");
        return f.Code("eao_fx_whiteline_resume", "WHL_intro");
    }

    internal static void Prepare()
    {
        PrepareRooms();
        foreach (var n in new[] { "fx_keeper", "fx_sign", "fx_whiteline" }) Msl.AddObject("o_eao_" + n, parentName: "o_simple_NPC", isVisible: true);
        foreach (var n in new[] { "fx_entry", "fx_back" }) Msl.AddObject("o_eao_" + n, parentName: "o_Doors_all_small", isVisible: true);
        Msl.AddObject("o_eao_fx_start_in", parentName: "o_position_starter", isVisible: false);
        Msl.AddObject("o_eao_fx_floor", isVisible: true);
    }
    internal static void Configure(Action<UndertaleGameObject, string, EventType, uint> set, ModFile files)
    {
        var stubs = string.Concat(new[] {
            files.GetCode("fx_qry_intro.gml"), files.GetCode("fx_qry_night.gml"), files.GetCode("fx_qry_hub.gml"),
            files.GetCode("fx_qry_before.gml"), files.GetCode("fx_qry_after.gml"), files.GetCode("fx_qry_early.gml"),
            files.GetCode("fx_qry_late.gml"), files.GetCode("fx_qry_refusal.gml"), files.GetCode("fx_qry_proxy.gml"),
            files.GetCode("cs_system_helpers.gml")
        });
        var npcs = new[] {
            ("fx_keeper", "石场看守德茹", "Deru the quarry keeper", "s_peasantfemale_06", "s_peasantfemale_06P", KeeperResume() + ChatPick + VisitPick + RegionPick + KeeperFlow()),
            ("fx_sign", "倒木上的抓痕", "Claw Marks on a Fallen Trunk", "s_camplog01", "s_peasantmale_13P", "eao_fx_sign_resume = function() {\nreturn 0;\n};\n" + SignFlow()),
            ("fx_whiteline", "坑边白线", "The white line at the pit", "s_carpet03", "s_peasantmale_13P", "eao_fx_whiteline_resume = function() {\nreturn 0;\n};\n" + WhiteLineFlow())
        };
        foreach (var n in npcs) {
            var obj = Msl.AddObject("o_eao_" + n.Item1, spriteName: n.Item4, parentName: "o_simple_NPC", isVisible: true);
            // AddObject reuses allocated resources without updating properties.
            obj.Sprite = Msl.GetSprite(n.Item4); obj.ParentId = Msl.GetObject("o_simple_NPC"); obj.Visible = true;
            var create = files.GetCode("courier_create.gml").Replace("路誓行会信使", n.Item2).Replace("Roadsworn courier", n.Item3).Replace("eao_mq01", "eao_" + n.Item1).Replace("s_peasantmale_13P", n.Item5);
            set(obj, create + stubs + n.Item6, EventType.Create, 0);
            set(obj, "event_inherited();", EventType.Draw, 0);
            set(obj, "event_inherited();", EventType.Mouse, 4);
        }
        foreach (var n in new[] { "fx_entry", "fx_back" }) {
            var obj = Msl.AddObject("o_eao_" + n, parentName: "o_Doors_all_small", isVisible: true);
            obj.Sprite = Msl.GetObject("o_Doors_all_small").Sprite;
        }
        void Door(string id, string target, string tag, string cn, string en)
        {
            var obj = Msl.GetObject("o_eao_" + id);
            set(obj, "event_inherited(); target = " + target + "; position_tag = " + NativeDocuments.Quote(tag) + "; is_lock = false; is_crime_door = false; is_quest = false; dungeon_level_incr = 0; name = global.language == 3 ? " + NativeDocuments.Quote(cn) + " : " + NativeDocuments.Quote(en) + "; scr_locationRoomEntityInitSavable(id, false);", EventType.Create, 0);
            set(obj, files.GetCode("night_door_draw.gml"), EventType.Draw, 0);
        }
        Door("fx_entry", Quarry, "EAO_FX_quarry_in", "城外石场小径", "Quarry path outside the walls");
        Door("fx_back", "r_Brynn_SW", "NA", "返回布林", "Back to Brynn");
        set(Msl.GetObject("o_eao_fx_entry"), files.GetCode("night_entry_alarm.gml"), EventType.Alarm, 7);
        set(Msl.GetObject("o_eao_fx_back"), files.GetCode("night_return_alarm.gml"), EventType.Alarm, 7);
        var marker = Msl.AddObject("o_eao_fx_start_in", parentName: "o_position_starter", isVisible: false);
        set(marker, "event_inherited(); position_tag = \"EAO_FX_quarry_in\";", EventType.Create, 0);
        var floor = Msl.AddObject("o_eao_fx_floor", isVisible: true);
        set(floor, "depth = 100;", EventType.Create, 0);
        set(floor, FloorDraw(), EventType.Draw, 0);
        // Absent or dead keepers leave the white line; nothing fabricates a
        // new consent for her (FX-T01). Inlined presence read.
        set(Msl.GetObject("o_eao_fx_keeper"), "event_inherited(); if (!instance_exists(o_dialogue) && ds_map_exists(global.characterDataMap, \"EAO_presence_FX_QRY\")) { var _p = ds_map_find_value(global.characterDataMap, \"EAO_presence_FX_QRY\"); if (_p == \"absent\" || _p == \"dead\") instance_destroy(); }", EventType.Step, 0);
        BuildRooms();
    }
}
