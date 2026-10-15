using System;
using System.Collections.Generic;
using System.Linq;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// A new story namespace; historical MQ01/MQ02 states are never prerequisites.
internal static class NightQuest
{
    private const string Stage = "var _s = 0; if (ds_map_exists(global.characterDataMap, \"EAO_N1_stage\")) _s = ds_map_find_value(global.characterDataMap, \"EAO_N1_stage\");\n";
    private const string Clues = "ds_map_exists(global.characterDataMap, \"EAO_N1_rope\") && ds_map_find_value(global.characterDataMap, \"EAO_N1_rope\") == 1 && ds_map_exists(global.characterDataMap, \"EAO_N1_cots\") && ds_map_find_value(global.characterDataMap, \"EAO_N1_cots\") == 1";
    private const string Plan = "var _p = \"\"; if (ds_map_exists(global.characterDataMap, \"EAO_N1_plan\")) _p = ds_map_find_value(global.characterDataMap, \"EAO_N1_plan\");\n";
    internal static string ActionsCode()
    {
        var code = "eao_n1_mara_resume = function() {\n" + Stage + Plan + "if (_s == 0) return 0; if (_s >= 5) return (_p == \"audit\" ? 4 : 3); if (_s >= 4) return 2; return 1;\n};\n" +
            "eao_n1_accept = function() {\n" + Stage + "if (_s != 0) return 0; ds_map_set(global.characterDataMap, \"EAO_N1_stage\", 1); ds_map_set(global.characterDataMap, \"EAO_N1_schema\", 1); return 0;\n};\n";
        foreach (var clue in new[] { ("rope", NightRooms.Yard), ("cots", NightRooms.Bellhouse) })
            code += "eao_n1_" + clue.Item1 + " = function() {\n" + Stage + "if (_s < 1 || room != " + clue.Item2 + ") return 1; ds_map_set(global.characterDataMap, \"EAO_N1_" + clue.Item1 + "\", 1); return 0;\n};\n";
        code += "eao_n1_ivo_resume = function() {\n" + Stage + "if (_s >= 4) return 3; if (_s >= 3) return 2; if (_s >= 2) return 1; if (" + Clues + ") return 1; return 0;\n};\n" +
            "eao_n1_reveal = function() {\n" + Stage + "if (_s >= 2) return 0; if (_s != 1 || room != r_eao_n1_bellhouse || !(" + Clues + ")) return 1; ds_map_set(global.characterDataMap, \"EAO_N1_stage\", 2); return 0;\n};\n";
        foreach (var choice in new[] { "shelter", "audit" })
            code += "eao_n1_plan_" + choice + " = function() {\n" + Stage + "if (_s >= 4) return 1; if (_s < 2 || room != r_eao_n1_bellhouse) return 1; ds_map_set(global.characterDataMap, \"EAO_N1_plan\", \"" + choice + "\"); ds_map_set(global.characterDataMap, \"EAO_N1_stage\", 3); return 0;\n};\n";
        code += "eao_n1_tor_resume = function() {\n" + Stage + Plan + "if (_s >= 4 && _p == \"shelter\") return 3; if (_s >= 4) return 2; if (_s == 3 && _p == \"audit\") return 1; return 0;\n};\n" +
            "eao_n1_tor_commit = function() {\n" + Stage + Plan + "if (_s >= 4) return 0; if (_s != 3 || _p != \"audit\" || room != r_eao_n1_yard) return 1; ds_map_set(global.characterDataMap, \"EAO_N1_families\", \"registered\"); ds_map_set(global.characterDataMap, \"EAO_N1_ivo\", \"held\"); ds_map_set(global.characterDataMap, \"EAO_N1_stage\", 4); return 0;\n};\n" +
            "eao_n1_rhea_resume = function() {\n" + Stage + "if (_s >= 4) return 1; return 0;\n};\n" +
            "eao_n1_escort = function() {\n" + Stage + Plan + "if (_s >= 4) return 0; if (_s != 3 || _p != \"shelter\" || room != r_eao_n1_underpass) return 1; ds_map_set(global.characterDataMap, \"EAO_N1_families\", \"hidden\"); ds_map_set(global.characterDataMap, \"EAO_N1_ivo\", \"escaped\"); ds_map_set(global.characterDataMap, \"EAO_N1_stage\", 4); return 0;\n};\n" +
            "eao_n1_close = function() {\n" + Stage + Plan + "if (_s >= 5) return (_p == \"audit\" ? 2 : 0); if (_s != 4) return 1; ds_map_set(global.characterDataMap, \"EAO_N1_stage\", 5); ds_map_set(global.characterDataMap, \"EAO_N1_lead\", \"ash_embankment\"); return (_p == \"audit\" ? 2 : 0);\n};\n";
        return code;
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

    private static string MaraFlow()
    {
        var f = new Flow("eao_n1_mara", "EAO_Mara");
        f.N("N1_mara_intro", "昨夜渡口没有敲钟，弟弟伊沃也没回来。收债人说他偷了钟。可钟声真能替一个人作证吗？", "The ferry bell was silent and Ivo never returned. The collectors call him a thief. Can silence prove that?", "N1_accept_pc", "N1_later_pc");
        f.P("N1_accept_pc", "我去渡口看看，先不答应把他交给谁。", "I'll inspect the ferry. I promise no one his arrest.", "instruction_N1_accept"); f.P("N1_later_pc", "我暂时不接这份差事。", "Not today.");
        f.A("instruction_N1_accept", "eao_n1_accept", "N1_mara_pending");
        f.N("N1_mara_pending", "沿商队旁标出的旧渡口堤道过去。钟房在断桥那头。别只听收债人的话，也看看昨夜留下了什么。", "Take the old ferry path beside the caravan. The bellhouse is across the broken causeway. Look at what last night left behind.", "N1_mara_leave_pc"); f.P("N1_mara_leave_pc", "我会带回他的消息。", "I'll bring word of him.");
        f.N("N1_mara_return", "你回来了，却没带伊沃。告诉我你在钟房见到了什么；我想听你的话，不想再听他们的说法。", "You returned without Ivo. Tell me what happened, in your own words.", "N1_mara_question_pc", "N1_close_pc", "N1_mara_wait_pc");
        f.P("N1_mara_question_pc", "你只让我找弟弟。你真的不知道那里藏着人？", "You only asked for your brother. Did you know about the families?", "N1_mara_admission");
        f.N("N1_mara_admission", "他借绳那天，我看见了小孩。我没追问。我想雇你把他带回来，又怕你知道后也只想拿他换赏钱。", "I saw a child when he borrowed rope. I asked nothing. I wanted him back and feared you would sell him for a bounty.", "N1_close_pc", "N1_mara_wait_pc");
        f.P("N1_close_pc", "告诉她停钟、藏身者和我的处理。", "Explain the silence, the families and your decision.", "instruction_N1_close"); f.P("N1_mara_wait_pc", "让我再想想怎么说。", "Let me find the words.");
        f.A("instruction_N1_close", "eao_n1_close", "N1_mara_done", "N1_mara_pending", "N1_mara_audit");
        f.N("N1_mara_done", "他活着，却得连名字一起藏起来。我会收好他的旧围巾。伊沃找过灰堤的旧雇工营；债票的来路，或许有人在那里记得。", "He lives, hiding even his name. I'll keep his old scarf. Someone at the ash embankment's labor camp may remember who wrote the claims.", "N1_done_pc");
        f.N("N1_mara_audit", "家属能用真名回去，伊沃却还在等听审。我该去看他。灰堤旧雇工营的人或许知道这些债票是谁开出来的。", "The families can use their names again; Ivo awaits a hearing. I'll visit him. The old labor camp may know who issued the claims.", "N1_done_pc");
        f.P("N1_done_pc", "告辞。", "Farewell.");
        return f.Code("eao_n1_mara_resume", "N1_mara_intro", "N1_mara_pending", "N1_mara_return", "N1_mara_done", "N1_mara_audit");
    }
    private static string TorFlow()
    {
        var f = new Flow("eao_n1_tor", "EAO_Tor");
        f.N("N1_tor_intro", "先别过桥。守夜人欠钱，钟又不响了，巧得很。找到了把他带来；私自渡河的人，也该登记。", "The keeper owes money and the bell fell silent. Convenient. Bring him here, and register anyone crossing without leave.", "N1_tor_question_pc", "N1_tor_leave_pc");
        f.P("N1_tor_question_pc", "你要的是修钟的钱，还是昨夜过河的人？", "Do you want repair money, or last night's passengers?", "N1_tor_answer");
        f.N("N1_tor_answer", "欠账的人，总得有个名字。我只收账，不问他们以前属于谁。你若想讨价还价，先把人找出来。", "Debtors need names. I collect accounts, not allegiances. Find them before you bargain.", "N1_tor_leave_pc"); f.P("N1_tor_leave_pc", "我先看现场。", "I'll inspect the site.");
        f.N("N1_tor_terms", "你要我当众收回家属的债票？可以。但伊沃得留下听审，不能和他们一起走。你能替他答应吗？", "I can withdraw the families' debt claims in public. Ivo must stay for the hearing. Will you agree?", "N1_tor_commit_pc", "N1_tor_reconsider_pc");
        f.P("N1_tor_commit_pc", "当众撤销家属债票；伊沃留下。确认执行。", "Withdraw their claims publicly. Ivo stays. Confirm.", "instruction_N1_tor_commit"); f.P("N1_tor_reconsider_pc", "我还没决定，回钟房谈另一条路。", "I'll reconsider with Ivo.");
        f.A("instruction_N1_tor_commit", "eao_n1_tor_commit", "N1_tor_done", "N1_tor_intro");
        f.N("N1_tor_done", "家属的债票作废，伊沃的名字留下。说清楚：你替他们争到了公开听审，没有替他争到无罪。", "The families' claims are void. Ivo remains named. You secured a public hearing, not an acquittal.", "N1_tor_end_pc");
        f.N("N1_tor_hidden", "钟房空了，暗渠也空了。你替他们藏住了人，却没让债票消失。下次他们还敢用真名吗？", "The bellhouse and drain are empty. You hid the people; their claims remain. Can they ever use their names again?", "N1_tor_end_pc"); f.P("N1_tor_end_pc", "离开渡口。", "Leave the ferry.");
        return f.Code("eao_n1_tor_resume", "N1_tor_intro", "N1_tor_terms", "N1_tor_done", "N1_tor_hidden");
    }
    private static string IvoFlow()
    {
        var f = new Flow("eao_n1_ivo", "EAO_Ivo");
        f.N("N1_ivo_guarded", "你也是来抓我的？钟没丢。别动那根绳，也别掀角落的铺盖。要听收债人的话，就回桥那头去。", "Here to arrest me? The bell isn't stolen. Leave the rope and blankets alone. Believe the collector if you like.", "N1_ivo_inspect_pc"); f.P("N1_ivo_inspect_pc", "先看看钟架和铺盖，再来问你。", "Inspect the bell frame and bedding first.");
        f.N("N1_ivo_challenge", "你看见割口和小孩的铺盖了？那就别再问我偷了什么。问我昨夜为什么不敢敲钟。", "You saw the cut and the child's bedding? Ask why I dared not ring, not what I stole.", "N1_reveal_pc", "N1_ivo_leave_pc");
        f.P("N1_reveal_pc", "我不来抓你。昨夜钟响了会发生什么？", "I'm not arresting you. What would the ringing have done?", "instruction_N1_reveal"); f.P("N1_ivo_leave_pc", "我还需要考虑。", "I need time.");
        f.A("instruction_N1_reveal", "eao_n1_reveal", "N1_ivo_truth", "N1_ivo_guarded");
        f.N("N1_ivo_truth", "追索者听钟放行，过桥就查债票。那些家属来找我藏身，我割了绳。玛拉不知道——我怕她也被记进账里。", "Collectors use the bell to check debt claims at the crossing. I hid the families and cut the rope. I kept Mara out of it.", "N1_shelter_pc", "N1_audit_pc", "N1_ivo_leave_pc");
        f.P("N1_shelter_pc", "带他们走暗渠；债票仍在，今后得隐姓藏身。", "Use the drain. Their claims remain; they must live hidden.", "instruction_N1_shelter");
        f.P("N1_audit_pc", "与追索者公开交涉撤销家属债票；你可能被留置。", "Negotiate openly for the families; you may be held.", "instruction_N1_audit");
        f.A("instruction_N1_shelter", "eao_n1_plan_shelter", "N1_ivo_route", "N1_ivo_aftermath"); f.A("instruction_N1_audit", "eao_n1_plan_audit", "N1_ivo_route", "N1_ivo_aftermath");
        f.N("N1_ivo_route", "暗渠在钟房东侧，蕾雅等在那里；交涉就去桥头找托雷。真正动身或签认之前，你还可以回来换一条路。", "Rhea waits in the east drain; Tor is at the causeway. You may change plans until departure or public confirmation.", "N1_change_shelter_pc", "N1_change_audit_pc", "N1_ivo_leave_pc");
        f.P("N1_change_shelter_pc", "改走暗渠。", "Choose the drain instead.", "instruction_N1_shelter"); f.P("N1_change_audit_pc", "改为公开交涉。", "Choose open negotiation instead.", "instruction_N1_audit");
        f.N("N1_ivo_aftermath", "最后的安排已经执行。回去告诉玛拉经过吧，别让她只听见别人的版本。", "The decision has been carried out. Tell Mara what happened yourself.", "N1_ivo_leave_pc");
        return f.Code("eao_n1_ivo_resume", "N1_ivo_guarded", "N1_ivo_challenge", "N1_ivo_route", "N1_ivo_aftermath");
    }
    private static string RheaFlow()
    {
        var f = new Flow("eao_n1_rhea", "EAO_Rhea");
        f.N("N1_rhea_intro", "孩子都能走了。过了暗渠就没有人登记我们，可债票还在。我们会安全一阵，也会再没有自己的名字。现在出发吗？", "The children can walk. Beyond the drain we'll be unregistered, but the claims remain. Safe for a while, without our names. Leave now?", "N1_escort_pc", "N1_rhea_wait_pc");
        f.P("N1_escort_pc", "确认从暗渠撤离。", "Confirm departure through the drain.", "instruction_N1_escort"); f.P("N1_rhea_wait_pc", "先等我，仍可以回去谈公开交涉。", "Wait; I can still negotiate openly.");
        f.A("instruction_N1_escort", "eao_n1_escort", "N1_rhea_done", "N1_rhea_intro");
        f.N("N1_rhea_done", "我们会沿暗渠的另一端离开。玛拉若问，就说伊沃还活着。谢谢你；别替我们许诺以后。", "We'll leave through the far end. Tell Mara Ivo lives. Thank you; promise nothing about our future.", "N1_rhea_end_pc"); f.P("N1_rhea_end_pc", "返回，告诉玛拉。", "Return to Mara.");
        return f.Code("eao_n1_rhea_resume", "N1_rhea_intro", "N1_rhea_done");
    }
    private static string ClueFlow(string id, string cn, string en)
    {
        var f = new Flow("eao_n1_" + id, "EAO_Clue");
        f.N("N1_" + id + "_intro", cn, en, "N1_" + id + "_inspect_pc", "N1_" + id + "_leave_pc");
        f.P("N1_" + id + "_leave_pc", "先离开这里。", "Leave for now.");
        f.P("N1_" + id + "_inspect_pc", "查看并记住现场。", "Examine and remember the scene.", "instruction_N1_" + id);
        f.A("instruction_N1_" + id, "eao_n1_" + id, "N1_" + id + "_done", "N1_" + id + "_intro");
        f.N("N1_" + id + "_done", id == "rope" ? "绳索有整齐的刀口，钟仍在架上。这里发生的不是偷钟。" : "铺盖有大小不同的脚印，角落留着孩子的布鞋。昨夜躲在这里的不止一个守夜人。", id == "rope" ? "A clean knife cut; the bell is still here. No bell was stolen." : "Different-sized footprints and a child's cloth shoe. The keeper was not alone.", "N1_" + id + "_end_pc");
        f.P("N1_" + id + "_end_pc", "继续调查。", "Continue investigating.");
        return f.Code("eao_n1_rhea_resume", "N1_" + id + "_intro", "N1_" + id + "_done");
    }

    internal static void Prepare()
    {
        NightArt.Ensure(); NightRooms.Prepare();
        foreach(var n in new[]{"mara","tor","ivo","rhea","rope","cots"}) Msl.AddObject("o_eao_n1_"+n,parentName:"o_simple_NPC",isVisible:true);
        foreach(var n in new[]{"entry","home","to_bell","to_yard","to_drain","to_house"}) Msl.AddObject("o_eao_n1_"+n,parentName:"o_Doors_all_small",isVisible:true);
        foreach(var n in new[]{"yard_in","yard_back","house_in","house_back","drain_in"}) Msl.AddObject("o_eao_n1_start_"+n,parentName:"o_position_starter",isVisible:false);
        Msl.AddObject("o_eao_n1_floor",isVisible:true); Msl.AddObject("o_eao_n1_bell_art",isVisible:true);
    }
    internal static void Configure(Action<UndertaleGameObject, string, EventType, uint> set, ModFile files)
    {
        NightArt.Ensure();
        NightRooms.Prepare();
        var npcs = new[] {
            ("mara", "绳匠玛拉", "Mara the rope maker", "s_peasantfemale_06", "s_peasantfemale_06P", MaraFlow()),
            ("tor", "追索人托雷", "Tor the collector", "s_peasantmale_13", "s_peasantmale_13P", TorFlow()),
            ("ivo", "守夜人伊沃", "Ivo the keeper", "s_peasantmale_13", "s_peasantmale_13P", IvoFlow()),
            ("rhea", "缝衣人蕾雅", "Rhea the seamstress", "s_peasantfemale_03", "s_peasantfemale_03P", RheaFlow()),
            ("rope", "断绳的钟架", "The cut bell rope", "s_blasphemousmass_bell01", "s_eao_n1_bellP", ClueFlow("rope", "钟还在，绳却断了。近看不是磨损，像被利器切开。", "The bell is here; the rope is severed. It looks cut, not worn.")),
            ("cots", "角落的铺盖", "Bedding in the corner", "s_carpet03", "s_eao_n1_cotsP", ClueFlow("cots", "铺盖不止一份，下面藏着一只很小的布鞋。", "Several blankets and a tiny cloth shoe tucked beneath them."))
        };
        foreach (var n in npcs) {
            var obj = Msl.AddObject("o_eao_n1_" + n.Item1, spriteName:n.Item4, parentName:"o_simple_NPC", isVisible:true);
            // AddObject reuses allocated resources without updating properties.
            obj.Sprite = Msl.GetSprite(n.Item4); obj.ParentId=Msl.GetObject("o_simple_NPC"); obj.Visible=true;
            var create = files.GetCode("courier_create.gml").Replace("路誓行会信使",n.Item2).Replace("Roadsworn courier",n.Item3).Replace("eao_mq01","eao_n1_"+n.Item1).Replace("s_peasantmale_13P",n.Item5);
            set(obj, create + ActionsCode() + n.Item6, EventType.Create, 0);
            var draw = "event_inherited();";
            if(n.Item1 is "rope" or "cots") draw="if ("+Hd2dArt.Active+") { draw_sprite("+Hd2dArt.Sprite(n.Item1=="rope"?"n1_cut_rope":"n1_bedding")+",0,x,y); } else { event_inherited(); }";
            set(obj, draw, EventType.Draw, 0); set(obj, "event_inherited();", EventType.Mouse, 4);
        }
        // Resolve dialogue text as well as actual on-scene actor presence.
        set(Msl.GetObject("o_eao_n1_ivo"), "event_inherited(); if (ds_map_exists(global.characterDataMap, \"EAO_N1_ivo\")) { var _f = ds_map_find_value(global.characterDataMap, \"EAO_N1_ivo\"); if (_f == \"escaped\" && !instance_exists(o_dialogue)) instance_destroy(); if (_f == \"held\") name = global.language == 3 ? \"伊沃（等待听审）\" : \"Ivo (awaiting hearing)\"; }", EventType.Step, 0);
        set(Msl.GetObject("o_eao_n1_rhea"), "event_inherited(); if (!instance_exists(o_dialogue) && ds_map_exists(global.characterDataMap, \"EAO_N1_families\")) instance_destroy();", EventType.Step, 0);
        foreach (var n in new[] { "entry", "home", "to_bell", "to_yard", "to_drain", "to_house" }) {
            var obj=Msl.AddObject("o_eao_n1_"+n, parentName:"o_Doors_all_small", isVisible:true); obj.Sprite=Msl.GetObject("o_Doors_all_small").Sprite;
        }
        void Door(string id, string target, string tag, string cn, string en) {
            var obj=Msl.GetObject("o_eao_n1_"+id);
            set(obj,"event_inherited(); target = "+target+"; position_tag = "+NativeDocuments.Quote(tag)+"; is_lock = false; is_crime_door = false; is_quest = false; dungeon_level_incr = 0; name = global.language == 3 ? "+NativeDocuments.Quote(cn)+" : "+NativeDocuments.Quote(en)+"; scr_locationRoomEntityInitSavable(id, false); depth = -y + 1;",EventType.Create,0);
            set(obj,files.GetCode("night_door_draw.gml"),EventType.Draw,0);
        }
        Door("entry",NightRooms.Yard,"EAO_N1_yard_in","旧渡口堤道","Old ferry path");
        Door("home","r_DockStore1floor","NA","返回商队","Return to caravan");
        Door("to_bell",NightRooms.Bellhouse,"EAO_N1_house_in","旧钟房","Bellhouse");
        Door("to_yard",NightRooms.Yard,"EAO_N1_yard_back","返回桥头","Causeway");
        Door("to_drain",NightRooms.Underpass,"EAO_N1_drain_in","暗渠","Drain");
        Door("to_house",NightRooms.Bellhouse,"EAO_N1_house_back","返回钟房","Bellhouse");
        set(Msl.GetObject("o_eao_n1_entry"),files.GetCode("night_entry_alarm.gml"),EventType.Alarm,7);
        set(Msl.GetObject("o_eao_n1_home"),"event_inherited(); if (ds_map_exists(global.characterDataMap, \"EAO_N1_origin_room\")) { var _r = asset_get_index(ds_map_find_value(global.characterDataMap, \"EAO_N1_origin_room\")); if (room_exists(_r)) target = _r; }",EventType.Step,0);
        set(Msl.GetObject("o_eao_n1_home"),files.GetCode("night_return_alarm.gml"),EventType.Alarm,7);
        set(Msl.GetObject("o_eao_n1_to_drain"),"event_inherited(); is_lock = !(ds_map_exists(global.characterDataMap, \"EAO_N1_stage\") && ds_map_find_value(global.characterDataMap, \"EAO_N1_stage\") >= 3 && ds_map_exists(global.characterDataMap, \"EAO_N1_plan\") && ds_map_find_value(global.characterDataMap, \"EAO_N1_plan\") == \"shelter\"); LVL = 100; speech_key = \"door_barred\";",EventType.Step,0);
        foreach (var marker in new[] {"yard_in","yard_back","house_in","house_back","drain_in"}) {
            var obj=Msl.AddObject("o_eao_n1_start_"+marker,parentName:"o_position_starter",isVisible:false);
            set(obj,"event_inherited(); position_tag = \"EAO_N1_"+marker+"\";",EventType.Create,0);
        }
        var floor=Msl.AddObject("o_eao_n1_floor",isVisible:true);
        set(floor,"depth = 100;",EventType.Create,0); set(floor,Hd2dArt.DrawFloor()+NightRooms.FloorDraw(),EventType.Draw,0);
        var prop=Msl.AddObject("o_eao_n1_bell_art",isVisible:true);
        set(prop,"depth = -y;",EventType.Create,0);
        set(prop,"if ("+Hd2dArt.Active+") { draw_sprite("+Hd2dArt.Sprite("n1_bell")+",0,x,y); } else { draw_sprite_ext(s_eao_n1_bell, 0, x, y, 104 / sprite_get_width(s_eao_n1_bell), 104 / sprite_get_width(s_eao_n1_bell), 0, c_white, 1); }",EventType.Draw,0);
        NightRooms.Build();
    }
}
