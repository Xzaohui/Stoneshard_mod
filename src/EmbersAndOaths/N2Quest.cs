using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Pilot batch P1 (MGMT-PILOT-N2-S153): the first handoff slice built on the
// N1 sample. Five registry stubs, five registered state keys, three scenes.
internal static class N2Quest
{
    internal const string Camp = "r_eao_n2_camp", Winch = "r_eao_n2_winch", Side = "r_eao_n2_side";
    internal const int Columns = 40, Rows = 30, Tile = 26;
    // Inclusive native grid cells; the sole source of floors, collisions and
    // exported layout checks, exactly like the N1 scenes.
    internal static readonly Dictionary<string, (int, int, int, int)[]> Shapes = new() {
        [Camp] = new[]{(5,7,17,24),(17,16,28,22),(28,9,35,20)},
        [Winch] = new[]{(4,20,34,25),(10,8,16,20),(22,5,27,19)},
        [Side] = new[]{(7,18,32,25),(10,6,28,18)}
    };
    internal static HashSet<(int, int)> Cells(string name)
    {
        var cells = new HashSet<(int, int)>();
        foreach (var r in Shapes[name]) for (var x = r.Item1; x <= r.Item3; x++) for (var y = r.Item2; y <= r.Item4; y++) cells.Add((x, y));
        return cells;
    }

    private static void N2Art()
    {
        var data = DataLoader.data;
        // Inspection portraits are cropped copies of the referenced native
        // sprites, following the N1 bell/bedding portrait convention.
        void Portrait(string name, string sourceName)
        {
            if (data.Sprites.Any(s => s.Name.Content == name)) return;
            var original = Msl.GetSprite(sourceName).Textures[0].Texture;
            var item = Msl.CreateTexureItem(original.TexturePage,
                new RectTexture(original.SourceX, original.SourceY, original.SourceWidth, original.SourceHeight),
                new RectTexture(0, 0, 37, 50), new BoundingData<ushort>(37, 50));
            data.TexturePageItems.Add(item);
            var icon = Msl.CreateSpriteNoCollisionMasks(name, new MarginData(0, 49, 0, 36), new OriginData(0, 0), new BoundingData<uint>(37, 50));
            icon.Textures.Add(new UndertaleSprite.TextureEntry { Texture = item });
            data.Sprites.Add(icon);
        }
        Portrait("s_eao_n2_coffinP", "s_woodcoffin04");
        Portrait("s_eao_n2_winchP", "s_loot_caravan_wheels2");
    }

    internal static void PrepareRooms()
    {
        foreach (var n in Shapes.Keys) {
            if (DataLoader.data.Rooms.Any(r => r.Name.Content == n)) continue;
            var source = Msl.GetRoom("r_DockStore1floor"); var room = NativeRooms.Copy(source);
            room.Name = DataLoader.data.Strings.MakeString(n); room.Caption = DataLoader.data.Strings.MakeString(n == Camp ? "灰堤雇工棚" : n == Winch ? "塌堤与旧绞盘" : "旧渠检修侧间");
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
            Add(r, "o_eao_n2_floor", 0, 0, "EAO_Floor", true);
            var cells = Cells(name);
            for (var x = 0; x < Columns; x++) for (var y = 0; y < Rows; y++) if (!cells.Contains((x, y))) Add(r, "o_hut_wall", x, y, "Collisions", true);
            if (name == Camp) {
                Add(r, "o_eao_n2_home", 7, 24); Add(r, "o_eao_n2_to_winch", 33, 11);
                Add(r, "o_eao_n2_aina", 11, 12); Add(r, "o_eao_n2_coffin", 8, 16);
                Add(r, "o_candle03", 6, 9); Add(r, "o_candlefire", 6, 9);
                Add(r, "o_candle03", 30, 13); Add(r, "o_candlefire", 30, 13);
                Add(r, "o_eao_n2_start_camp_in", 7, 22, "Controllers"); Add(r, "o_eao_n2_start_camp_back", 32, 12, "Controllers");
                Add(r, "o_abstract_player", 7, 22, "Controllers");
            } else if (name == Winch) {
                Add(r, "o_eao_n2_camp_back", 12, 24); Add(r, "o_eao_n2_to_side", 25, 7);
                Add(r, "o_eao_n2_watcher", 13, 14); Add(r, "o_eao_n2_winch", 24, 10);
                Add(r, "o_candle03", 11, 9); Add(r, "o_candlefire", 11, 9);
                Add(r, "o_candle03", 26, 17); Add(r, "o_candlefire", 26, 17);
                Add(r, "o_eao_n2_start_winch_in", 13, 22, "Controllers"); Add(r, "o_eao_n2_start_winch_back", 25, 9, "Controllers");
                Add(r, "o_abstract_player", 13, 22, "Controllers");
            } else {
                Add(r, "o_eao_n2_side_back", 29, 21);
                Add(r, "o_eao_n2_nara", 14, 10);
                Add(r, "o_candle03", 12, 7); Add(r, "o_candlefire", 12, 7);
                Add(r, "o_candle03", 24, 16); Add(r, "o_candlefire", 24, 16);
                Add(r, "o_eao_n2_start_side_in", 28, 20, "Controllers");
                Add(r, "o_abstract_player", 28, 20, "Controllers");
            }
        }
    }
    internal static string FloorDraw()
    {
        var code = new StringBuilder("var _c = draw_get_color(); var _a = draw_get_alpha(); draw_set_alpha(1); draw_set_color(make_color_rgb(17,19,18)); draw_rectangle(0,0,room_width,room_height,false);\n");
        foreach (var name in Shapes.Keys) {
            var cells = Cells(name); code.AppendLine("if (room == " + name + ") {");
            foreach (var p in cells.OrderBy(p => p.Item2).ThenBy(p => p.Item1)) {
                var px = p.Item1 * Tile; var py = p.Item2 * Tile;
                var tint = name == Camp ? "make_color_rgb(64,58,48)" : name == Winch ? "make_color_rgb(58,64,66)" : "make_color_rgb(52,48,52)";
                code.AppendLine($"draw_set_color({tint}); draw_rectangle({px},{py},{px+25},{py+25},false);");
                code.AppendLine($"draw_set_color(make_color_rgb(35,36,32)); draw_line({px},{py+25},{px+25},{py+25});");
                if ((p.Item1 + p.Item2) % 4 == 0) code.AppendLine($"draw_sprite_ext(s_dungeonfloor01, {(p.Item1+p.Item2)%12}, {px+13}, {py+13}, 0.25, 0.25, 0, c_white, 0.3);");
                if (!cells.Contains((p.Item1, p.Item2 - 1))) code.AppendLine($"draw_set_color(make_color_rgb(88,86,74)); draw_rectangle({px},{py-13},{px+25},{py+2},false); draw_set_color(make_color_rgb(28,30,28)); draw_line({px},{py},{px+25},{py});");
                if (!cells.Contains((p.Item1 - 1, p.Item2))) code.AppendLine($"draw_set_color(make_color_rgb(82,80,69)); draw_rectangle({px-6},{py},{px+1},{py+25},false);");
                if (!cells.Contains((p.Item1 + 1, p.Item2))) code.AppendLine($"draw_set_color(make_color_rgb(39,41,38)); draw_rectangle({px+23},{py},{px+29},{py+25},false);");
            }
            code.AppendLine("}");
        }
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

    // Registry-driven resume selectors. Reads never mutate; a settled case is
    // only ever appended to, never rewritten (N2-T05/T06).
    private static string AinaResume()
    {
        return "eao_n2_aina_resume = function() {\n" +
            "if (ds_map_exists(global.characterDataMap, \"EAO_presence_N2\") && ds_map_find_value(global.characterDataMap, \"EAO_presence_N2\") == \"refused\") return 5;\n" +
            "if (ds_map_exists(global.characterDataMap, \"EAO_resolve_N2\")) { var _r = ds_map_find_value(global.characterDataMap, \"EAO_resolve_N2\"); if (_r == \"public\") return 4; if (_r == \"protected\") return 3; }\n" +
            "if (ds_map_exists(global.characterDataMap, \"EAO_encountered_N2\") && ds_map_find_value(global.characterDataMap, \"EAO_encountered_N2\")) return 1;\n" +
            "return 0;\n};\n";
    }
    private static string WatcherResume()
    {
        return "eao_n2_watcher_resume = function() {\n" +
            "if (ds_map_exists(global.characterDataMap, \"EAO_encountered_N2\") && ds_map_find_value(global.characterDataMap, \"EAO_encountered_N2\")) return 1;\n" +
            "return 0;\n};\n";
    }
    private static string NaraResume()
    {
        return "eao_n2_nara_resume = function() {\n" +
            "if (ds_map_exists(global.characterDataMap, \"EAO_presence_N2\") && ds_map_find_value(global.characterDataMap, \"EAO_presence_N2\") == \"refused\") return 4;\n" +
            "if (ds_map_exists(global.characterDataMap, \"EAO_resolve_N2\")) { var _r = ds_map_find_value(global.characterDataMap, \"EAO_resolve_N2\"); if (_r == \"public\") return 3; if (_r == \"protected\") return 2; }\n" +
            "if (ds_map_exists(global.characterDataMap, \"EAO_encountered_N2\") && ds_map_find_value(global.characterDataMap, \"EAO_encountered_N2\")) return 1;\n" +
            "return 0;\n};\n";
    }
    private static string StillResume(string id)
    {
        return "eao_n2_" + id + "_resume = function() {\nreturn 0;\n};\n";
    }

    private static string AinaFlow()
    {
        var f = new Flow("eao_n2_aina", "EAO_Aina");
        f.N("N2_aina_intro", "没有人把他从水里捞出来。可收债的肯承认他死，只要我也承认营里不再欠他工钱。", "No one pulled him out of the water. The collectors will admit he is dead — as long as I also admit the camp owes him no more wages.", "N2_question_pc");
        f.P("N2_question_pc", "你要的不是葬礼？", "You are not asking for a funeral?", "N2_aina_intro2");
        f.N("N2_aina_intro2", "我要能活到下一次葬礼。他要真活着，我也得先吃饭。", "I need to live until the next funeral. If he is truly alive, I still have to eat first.", "instruction_N2_entry");
        f.A("instruction_N2_entry", "eao_n2_entry", "N2_aina_offer");
        f.N("N2_aina_offer", "棺是空的，营里要的只是一份签了字的死亡登记。答应之前，先去堤上看看；接不接，今天的话都别带出这间棚子。", "The coffin is empty; the camp only wants a signed death register. Look at the dike before you promise anything — and either way, keep today's words inside this shed.", "N2_accept_pc", "N2_leave_pc");
        f.P("N2_accept_pc", "我去看那口棺材和那段堤。我不先替任何人认下死亡。", "I'll look at the coffin and the dike. I promise no one his death.", "N2_aina_pending");
        f.P("N2_leave_pc", "我之后再谈。", "Another time.");
        f.N("N2_aina_pending", "塌堤上那台绞盘只拆了一半，看堤的人还在外头；旧渠有间检修侧间，本来该是锁着的。", "The winch on the broken dike is only half dismantled, and the watchers stay out there. The old drain has a maintenance room that is supposed to stay locked.", "N2_report_pc", "N2_aina_leave_pc");
        f.P("N2_report_pc", "我在旧渠的检修侧间找到了纳拉。他活着，腿用木片固定着。", "I found Nara in the drain maintenance room. He is alive, his leg splinted with wood.", "N2_aina_terms");
        f.N("N2_aina_terms", "他们会问他住哪。", "They will ask him where he lives.", "N2_terms_pc");
        f.P("N2_terms_pc", "可以只纠正死亡和欠薪，不公开藏身点；也可以要求他到听审处作证。", "You can correct the death and the wages without exposing where he hides — or ask him to testify at the hearing in person.", "N2_aina_terms2");
        f.N("N2_aina_terms2", "他是我丈夫，不是我的赔偿凭据。让他自己选。", "He is my husband, not my compensation voucher. Let him choose himself.", "N2_carry_pc");
        f.P("N2_carry_pc", "我会把话带到。", "I'll carry him your words.");
        f.P("N2_aina_leave_pc", "我去堤上看看。", "I'll walk the dike.");
        f.N("N2_aina_refused", "你不肯接，我不怪你。丧事照办，账照欠。你去吧。", "You would not take it. I don't blame you. The funeral goes on, the debt stands. Go.", "N2_refused_end_pc");
        f.P("N2_refused_end_pc", "让她安静办完丧事。", "Leave her to finish the funeral in peace.");
        f.N("N2_aina_after_protected", "封存的核验递上去了。欠薪会回来，只是慢一些。外套我从棺里收了出来——等他能再用自己名字的那天，还给他。", "The sealed verification is filed. The wages will come back, only slower. I took his coat out of the coffin — he can have it back the day he can use his own name again.", "N2_after_end_pc");
        f.N("N2_aina_after_public", "他要用自己的名字去听审。棺是空着下葬的，名字得活着回来。你把他带到了能说话的地方。", "He will testify under his own name. The coffin went into the ground empty; the name must come back alive. You brought him somewhere he can speak.", "N2_after_end_pc");
        f.P("N2_after_end_pc", "告辞。", "Farewell.");
        return f.Code("eao_n2_aina_resume", "N2_aina_intro", "N2_aina_pending", "N2_aina_pending", "N2_aina_after_protected", "N2_aina_after_public", "N2_aina_refused");
    }
    private static string WatcherFlow()
    {
        var f = new Flow("eao_n2_watcher", "EAO_Watcher");
        f.N("N2_watcher_idle", "堤上风大。要找说话的人，去坡上的棚子——那里在办一场没有尸体的丧事。", "The wind bites on the dike. If you are looking for someone to talk to, try the shed up the slope — they are holding a funeral without a body there.", "N2_idle_end_pc");
        f.P("N2_idle_end_pc", "我这就去。", "On my way.");
        f.N("N2_watcher_intro", "堤上风大。来看绞盘的？办丧事那家在坡上棚子里。", "The wind bites on the dike. Here for the winch? The mourning family is up in the shed.", "N2_marks_pc", "N2_watcher_leave_pc");
        f.P("N2_marks_pc", "事故之后，有人还用过他的刻刀。", "After the accident, someone still used his graver.", "N2_watcher_answer");
        f.N("N2_watcher_answer", "刻记不能证明是他。可拆绞盘那天，工头说死人不用领停工钱。", "A carved mark proves nothing by itself. But the day they took the winch apart, the foreman said dead men draw no layoff pay.", "N2_marks2_pc");
        f.P("N2_marks2_pc", "一件工具不能证明人活着。那就找用工具的人。", "One tool does not prove a man alive. Then find the man who used the tool.", "N2_watcher_hint");
        f.N("N2_watcher_hint", "旧渠那间检修侧间常年上锁。上个月锁叫人撬开了——里头的灯芯是新的。", "The maintenance room off the old drain stays locked all year. Someone forced that lock last month — and the lamp wick inside is new.", "N2_watcher_end_pc");
        f.P("N2_watcher_end_pc", "小心松动的石块。", "Mind the loose stones.");
        f.P("N2_watcher_leave_pc", "只是路过堤上。", "Just passing the dike.");
        return f.Code("eao_n2_watcher_resume", "N2_watcher_idle", "N2_watcher_intro");
    }
    private static string NaraFlow()
    {
        var f = new Flow("eao_n2_nara", "EAO_Nara");
        f.N("N2_nara_guarded", "……检修的？工营的人不下来这儿。出去把门带上。", "...Maintenance? The camp's men don't come down here. Close the door on your way out.", "N2_guarded_leave_pc");
        f.P("N2_guarded_leave_pc", "先退出去。", "Step back out.");
        f.N("N2_nara_intro", "他们把我的死填好了。再回去，欠薪没了，欠债倒会回来。", "They filed my death away neat. Go back, and the back pay is gone — the debts come back instead.", "N2_burial_pc");
        f.P("N2_burial_pc", "艾娜在替你办葬礼。", "Aina is holding your funeral.", "N2_nara_intro2");
        f.N("N2_nara_intro2", "告诉她我活着。但别替我签回营的纸。我修得了轴，已经爬不上堤。", "Tell her I am alive. But do not sign me back into the camp. I can still true an axle; I can no longer climb the dike.", "N2_nara_terms");
        f.N("N2_nara_terms", "那就两条路：封存证言去讨欠薪，或者我实名去听审。你带的是哪一句？", "Two roads, then: a sealed testimony to claim the wages, or my real name at the hearing. Which word did you bring me?", "N2_protected_pc", "N2_public_pc", "N2_refuse_pc", "N2_leave_pc");
        f.P("N2_protected_pc", "提交匿名工伤核验，保留住址，追讨欠薪。", "File an anonymous injury verification, keep the address sealed, and claim the unpaid wages.", "N2_nara_confirm_protected");
        f.N("N2_nara_confirm_protected", "封存核验……签名是官家的，轴是我的。慢是慢，命还是我的。就这么办？", "A sealed verification... the signature belongs to the office, the axle to me. Slow, but the life stays mine. Do it?", "N2_confirm_p_pc", "N2_reconsider_pc");
        f.P("N2_confirm_p_pc", "确认执行，递交核验。", "Confirmed. File it.", "instruction_N2_choice_protected");
        f.P("N2_reconsider_pc", "先不定，我回棚里再谈谈。", "Not yet. I'll talk it over back at the shed.");
        f.A("instruction_N2_choice_protected", "eao_n2_choice_protected", "N2_nara_after_protected");
        f.P("N2_public_pc", "纳拉同意实名作证，安排短程安全转移。", "Nara testifies under his real name; arrange a short, safe transfer.", "N2_nara_confirm_public");
        f.N("N2_nara_confirm_public", "实名……那买了他债的人也会知道我在哪。转移得快。你确定？", "My real name... then the men who bought the debts will know where I sit. The transfer must be quick. Are you certain?", "N2_confirm_u_pc", "N2_swap_pc", "N2_reconsider_pc");
        f.P("N2_confirm_u_pc", "确认执行，用他的名字上听审。", "Confirmed. His name, at the hearing.", "instruction_N2_choice_public");
        f.P("N2_swap_pc", "改走匿名核验那条路。", "Take the anonymous route instead.", "N2_nara_confirm_protected");
        f.A("instruction_N2_choice_public", "eao_n2_choice_public", "N2_nara_after_public");
        f.N("N2_nara_after_protected", "证言封存，欠薪照讨。听审开场的是纸和轴座，不是我。这样也好——我还修得起下一根轴。", "Testimony sealed, wages still claimed. The hearing opens with papers and the axle seat, not with me. So be it — I can still mend the next axle.", "N2_after_end_pc");
        f.N("N2_nara_after_public", "名字还给他们了。听审那天我到场，追索的人要问就来问。谢谢你把艾娜的话带到了。", "They have my name back. I will stand at the hearing, and let the collectors come and ask. Thank you for carrying Aina's words.", "N2_after_end_pc");
        f.P("N2_after_end_pc", "保重。", "Stay whole.");
        f.P("N2_refuse_pc", "这两条我都不走，也不替你传话。", "I'll take neither road, and carry no message.", "N2_nara_refusal");
        f.N("N2_nara_refusal", "……也好。死人不多话。把门带上。", "...So be it. Dead men talk little. Close the door behind you.", "instruction_N2_refusal");
        f.A("instruction_N2_refusal", "eao_n2_refusal", "N2_nara_refused_end_pc");
        f.P("N2_nara_refused_end_pc", "把安静留给他。", "Leave him the quiet he chose.");
        f.P("N2_leave_pc", "让我再想想。", "Let me think on it.");
        return f.Code("eao_n2_nara_resume", "N2_nara_guarded", "N2_nara_intro", "N2_nara_after_protected", "N2_nara_after_public", "N2_nara_refusal");
    }
    private static string CoffinFlow()
    {
        var f = new Flow("eao_n2_coffin", "EAO_Coffin");
        f.N("N2_coffin_intro", "棺盖没有钉死。里面是一件男人的旧外套，叠得方正。这口棺材称不出多少分量。", "The lid is not nailed down. Inside is a man's old coat, folded square. This coffin carries little weight.", "N2_coffin_inspect_pc", "N2_coffin_leave_pc");
        f.P("N2_coffin_inspect_pc", "记住外套和没钉死的棺盖。", "Note the coat and the unnailed lid.", "N2_coffin_done");
        f.N("N2_coffin_done", "营里肯出丧事的钱，条件是死亡登记签字。棺材什么都不说，说了话的是纸。", "The camp will pay for the burial only if the death register is signed. The coffin says nothing; the paper would speak.", "N2_coffin_end_pc");
        f.P("N2_coffin_end_pc", "从棺前退开。", "Step back from the coffin.");
        f.P("N2_coffin_leave_pc", "不去动它。", "Leave it closed.");
        return f.Code("eao_n2_coffin_resume", "N2_coffin_intro");
    }
    private static string WinchFlow()
    {
        var f = new Flow("eao_n2_winch", "EAO_Winch");
        f.N("N2_winch_intro", "泥线以下是事故的旧划痕，锈死了；泥线以上是新的座痕——轴座是事故后拆走的。修好的架子上刻着与外套同一个名字。", "Below the mud line: accident scratches, rusted old. Above it: fresh socket marks — the axle seat was unbolted after the flood. A repaired frame carries the same carved name as the coat.", "N2_winch_inspect_pc", "N2_winch_leave_pc");
        f.P("N2_winch_inspect_pc", "比对两套痕迹。", "Compare the two sets of marks.", "N2_winch_done");
        f.N("N2_winch_done", "工具是被活人的手用过的，而且不久。拆走轴座的人，还修得动一根轴。", "The tool was used by a living hand, and not long ago. Whoever unbolted the seat can still true an axle.", "N2_winch_end_pc");
        f.P("N2_winch_end_pc", "离开绞盘。", "Leave the winch.");
        f.P("N2_winch_leave_pc", "先不看。", "Not now.");
        return f.Code("eao_n2_winch_resume", "N2_winch_intro");
    }

    internal static void Prepare()
    {
        PrepareRooms();
        foreach (var n in new[] { "aina", "watcher", "nara", "coffin", "winch" }) Msl.AddObject("o_eao_n2_" + n, parentName: "o_simple_NPC", isVisible: true);
        foreach (var n in new[] { "entry", "home", "to_winch", "camp_back", "to_side", "side_back" }) Msl.AddObject("o_eao_n2_" + n, parentName: "o_Doors_all_small", isVisible: true);
        foreach (var n in new[] { "camp_in", "camp_back", "winch_in", "winch_back", "side_in" }) Msl.AddObject("o_eao_n2_start_" + n, parentName: "o_position_starter", isVisible: false);
        Msl.AddObject("o_eao_n2_floor", isVisible: true);
    }
    internal static void Configure(Action<UndertaleGameObject, string, EventType, uint> set, ModFile files)
    {
        N2Art();
        var stubs = files.GetCode("n2_entry.gml") + files.GetCode("n2_hub.gml") + files.GetCode("n2_choice_protected.gml") + files.GetCode("n2_choice_public.gml") + files.GetCode("n2_refusal.gml");
        var npcs = new[] {
            ("aina", "灰堤遗属艾娜", "Aina the widow", "s_peasantfemale_06", "s_peasantfemale_06P", AinaResume() + AinaFlow()),
            ("watcher", "看堤老工", "Old dike watcher", "s_peasantmale_13", "s_peasantmale_13P", WatcherResume() + WatcherFlow()),
            ("nara", "纳拉", "Nara", "s_peasantmale_13", "s_peasantmale_13P", NaraResume() + NaraFlow()),
            ("coffin", "空棺", "The empty coffin", "s_woodcoffin04", "s_eao_n2_coffinP", StillResume("coffin") + CoffinFlow()),
            ("winch", "旧绞盘", "The old winch", "s_loot_caravan_wheels2", "s_eao_n2_winchP", StillResume("winch") + WinchFlow())
        };
        foreach (var n in npcs) {
            var obj = Msl.AddObject("o_eao_n2_" + n.Item1, spriteName: n.Item4, parentName: "o_simple_NPC", isVisible: true);
            // AddObject reuses allocated resources without updating properties.
            obj.Sprite = Msl.GetSprite(n.Item4); obj.ParentId = Msl.GetObject("o_simple_NPC"); obj.Visible = true;
            var create = files.GetCode("courier_create.gml").Replace("路誓行会信使", n.Item2).Replace("Roadsworn courier", n.Item3).Replace("eao_mq01", "eao_n2_" + n.Item1).Replace("s_peasantmale_13P", n.Item5);
            set(obj, create + stubs + n.Item6, EventType.Create, 0);
            set(obj, "event_inherited();", EventType.Draw, 0);
            set(obj, "event_inherited();", EventType.Mouse, 4);
        }
        foreach (var n in new[] { "entry", "home", "to_winch", "camp_back", "to_side", "side_back" }) {
            var obj = Msl.AddObject("o_eao_n2_" + n, parentName: "o_Doors_all_small", isVisible: true);
            obj.Sprite = Msl.GetObject("o_Doors_all_small").Sprite;
        }
        void Door(string id, string target, string tag, string cn, string en)
        {
            var obj = Msl.GetObject("o_eao_n2_" + id);
            set(obj, "event_inherited(); target = " + target + "; position_tag = " + NativeDocuments.Quote(tag) + "; is_lock = false; is_crime_door = false; is_quest = false; dungeon_level_incr = 0; name = global.language == 3 ? " + NativeDocuments.Quote(cn) + " : " + NativeDocuments.Quote(en) + "; scr_locationRoomEntityInitSavable(id, false);", EventType.Create, 0);
            set(obj, files.GetCode("night_door_draw.gml"), EventType.Draw, 0);
        }
        Door("entry", Camp, "EAO_N2_camp_in", "灰堤堤道", "Ash embankment path");
        Door("home", "r_DockStore1floor", "NA", "返回来路", "Return the way you came");
        Door("to_winch", Winch, "EAO_N2_winch_in", "去塌堤", "To the broken dike");
        Door("camp_back", Camp, "EAO_N2_camp_back", "返回雇工棚", "Back to the labor shed");
        Door("to_side", Side, "EAO_N2_side_in", "旧渠侧间", "Drain maintenance room");
        Door("side_back", Winch, "EAO_N2_winch_back", "返回塌堤", "Back to the dike");
        set(Msl.GetObject("o_eao_n2_entry"), files.GetCode("night_entry_alarm.gml"), EventType.Alarm, 7);
        set(Msl.GetObject("o_eao_n2_home"), "event_inherited(); if (ds_map_exists(global.characterDataMap, \"EAO_N1_origin_room\")) { var _r = asset_get_index(ds_map_find_value(global.characterDataMap, \"EAO_N1_origin_room\")); if (room_exists(_r)) target = _r; }", EventType.Step, 0);
        set(Msl.GetObject("o_eao_n2_home"), files.GetCode("night_return_alarm.gml"), EventType.Alarm, 7);
        foreach (var marker in new[] { ("camp_in", "EAO_N2_camp_in"), ("camp_back", "EAO_N2_camp_back"), ("winch_in", "EAO_N2_winch_in"), ("winch_back", "EAO_N2_winch_back"), ("side_in", "EAO_N2_side_in") }) {
            var obj = Msl.AddObject("o_eao_n2_start_" + marker.Item1, parentName: "o_position_starter", isVisible: false);
            set(obj, "event_inherited(); position_tag = " + NativeDocuments.Quote(marker.Item2) + ";", EventType.Create, 0);
        }
        var floor = Msl.AddObject("o_eao_n2_floor", isVisible: true);
        set(floor, "depth = 100;", EventType.Create, 0);
        set(floor, FloorDraw(), EventType.Draw, 0);
        BuildRooms();
    }
}
