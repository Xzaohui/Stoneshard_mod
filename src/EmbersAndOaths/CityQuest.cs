using System;
using System.Collections.Generic;
using System.Linq;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Pilot batch P2 (MGMT-PILOT-BRY01-S156): the city system layer. Fourteen
// registry stubs and ten registered state keys for the lease case, plus the
// SVC-BRY service desk, the S87 Brynn trust band and the split town/band
// gossip pools. Actors spawn inside the native Brynn quarters; the physical
// case interiors stay open (OI-06).
internal static class CityQuest
{
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

    // Registry-driven resume selectors; reads never mutate and a settled case
    // is only appended to (BRY01-T02/T03/T05). All bodies are fully inlined:
    // bare eao_* static calls caused the 0.1.1 runner crash, so only pushed
    // dialogue callbacks may reference helper methods.
    private static string PelanResume() =>
        "eao_cs_pelan_resume = function() {\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_presence_CS_BRY_01\")) { var _p = ds_map_find_value(global.characterDataMap, \"EAO_presence_CS_BRY_01\"); if (_p == \"absent\" || _p == \"dead\" || _p == \"refused\") return 4; }\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_resolve_CS_BRY_01\")) { var _r = ds_map_find_value(global.characterDataMap, \"EAO_resolve_CS_BRY_01\"); if (_r == \"continuity\") return 2; if (_r == \"exit\") return 3; }\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_encountered_CS_BRY_01\") && ds_map_find_value(global.characterDataMap, \"EAO_encountered_CS_BRY_01\")) return 1;\n" +
        "return 0;\n};\n";
    private static string RenaResume() =>
        "eao_cs_rena_resume = function() {\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_resolve_CS_BRY_01\")) { var _r = ds_map_find_value(global.characterDataMap, \"EAO_resolve_CS_BRY_01\"); if (_r == \"continuity\") return 1; if (_r == \"exit\") return 2; }\n" +
        "return 0;\n};\n";
    private static string LukanResume() =>
        "eao_cs_lukan_resume = function() {\n" +
        "if (variable_global_exists(\"EAO_cs_runtime_witness\") && global.EAO_cs_runtime_witness) return 2;\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_encountered_CS_BRY_01\") && ds_map_find_value(global.characterDataMap, \"EAO_encountered_CS_BRY_01\")) return 1;\n" +
        "return 0;\n};\n";
    private static string MalerResume() =>
        "eao_cs_maler_resume = function() {\n" +
        "if (ds_map_exists(global.characterDataMap, \"EAO_resolve_CS_BRY_01\") && ds_map_find_value(global.characterDataMap, \"EAO_resolve_CS_BRY_01\") == \"exit\") return 1;\n" +
        "return 0;\n};\n";
    private static string MiloResume() =>
        "eao_svc_milo_resume = function() {\n" +
        "var _b = 0;\n" +
        "if (global.EAO_dev_enabled && variable_global_exists(\"EAO_dev_trust_override\") && global.EAO_dev_trust_override != -9) _b = global.EAO_dev_trust_override;\n" +
        "else if (ds_map_exists(global.characterDataMap, \"EAO_trust_BRY\")) _b = clamp(ds_map_find_value(global.characterDataMap, \"EAO_trust_BRY\"), -2, 2);\n" +
        "if (_b >= 2) return 2;\n" +
        "if (_b == 1) return 1;\n" +
        "return 0;\n};\n";
    private static string StreetResume() =>
        "eao_cs_street_resume = function() {\n" +
        "var _b = 0;\n" +
        "if (global.EAO_dev_enabled && variable_global_exists(\"EAO_dev_trust_override\") && global.EAO_dev_trust_override != -9) _b = global.EAO_dev_trust_override;\n" +
        "else if (ds_map_exists(global.characterDataMap, \"EAO_trust_BRY\")) _b = clamp(ds_map_find_value(global.characterDataMap, \"EAO_trust_BRY\"), -2, 2);\n" +
        "if (_b >= 2) return 2;\n" +
        "if (_b <= -1) return 1;\n" +
        "return 0;\n};\n";

    private static string PelanFlow()
    {
        var f = new Flow("eao_cs_pelan", "EAO_Pelan");
        f.N("CS_pl_intro", "差几天？你昨天还说差几天，今天说换个门就重算。", "A few days short? Yesterday you said a few days; today you say a new door restarts the count.", "CS_pl_q_pc", "CS_pl_pass_pc");
        f.P("CS_pl_q_pc", "另立租金，和抹掉已经住过的日子是一件事？", "A new rent — is that the same as erasing the days already lived?", "CS_pl_intro2");
        f.N("CS_pl_intro2", "我想问以后去哪时不用求他。我不想你们先替我说我准能当什么城里人。", "I want to ask where I'll go without begging him. Don't decide for me that I'm bound to become some townswoman.", "CS_pl_offer_pc", "CS_pl_refuse_pc");
        f.P("CS_pl_offer_pc", "我先弄清这份租约的来龙去脉。", "I'll untangle this lease first.", "instruction_CS_entry");
        f.A("instruction_CS_entry", "eao_cs_bry_01_entry", "CS_pl_pending");
        f.N("CS_pl_pending", "我没请你替我说这一年都做对了，只问那些天有没有。", "I didn't ask you to vouch I did everything right this year — only whether those days happened.", "CS_pl_visit_pc", "CS_pl_stop_pc");
        f.P("CS_pl_visit_pc", "只记这户、这段见过的日期，愿意吗？", "Only the dates you saw, for this household — will you stand by that?", "CS_pl_consent");
        f.N("CS_pl_consent", "愿意。家里谁来过，不在里边。", "I agree. Who came to my home is not part of it.", "CS_pl_guide");
        f.N("CS_pl_guide", "鲁坎在城外堤段带工。他签过的日子，登记处才认。", "Lukan leads the crew on the dike outside. Only days he has signed count at the registry.", "CS_pl_stop_pc");
        f.P("CS_pl_refuse_pc", "我两边都不替你们选。", "I'll choose neither side for you.", "instruction_CS_refusal");
        f.A("instruction_CS_refusal", "eao_cs_bry_01_refusal", "CS_pl_refusal");
        f.N("CS_pl_refusal", "可以。我得知道新短租贵多少，旧押金又能拿回哪一块。", "Fine. I need to know how much dearer a new short lease is, and which part of the old deposit comes back.", "CS_pl_ref_end_pc");
        f.P("CS_pl_ref_end_pc", "让她自己算清再谈。", "Leave her to reckon it herself.");
        f.N("CS_pl_after_c", "我搬了门。没被搬回第一天。", "I changed doors. I wasn't moved back to day one.", "CS_pl_bye_pc");
        f.N("CS_pl_after_e", "贵一点。我认自己选的贵，不认从前那一年没住。", "Dearer. I own the price I chose — not the claim I never lived that year.", "CS_pl_bye_pc");
        f.P("CS_pl_bye_pc", "告辞。", "Farewell.");
        f.P("CS_pl_pass_pc", "只是路过。", "Just passing.");
        f.P("CS_pl_stop_pc", "先停在这里。", "Stop here for now.");
        return f.Code("eao_cs_pelan_resume", "CS_pl_intro", "CS_pl_pending", "CS_pl_after_c", "CS_pl_after_e", "CS_pl_refusal");
    }
    private static string RenaFlow()
    {
        var f = new Flow("eao_cs_rena", "EAO_Rena");
        f.N("CS_re_idle", "我两次搬牌时只留了新房号。那不是你从没住过。", "Both times I moved the plate I kept only the new number. That is not the same as your never having lived there.", "CS_re_trace_pc", "CS_re_terms_pc", "CS_re_receipt_pc", "CS_re_bye_pc");
        f.P("CS_re_trace_pc", "先看公共门框和旧补钉日期。", "Look at the public doorframe and the old patch dates.", "CS_re_trace");
        f.N("CS_re_trace", "认住用不必开她卧房；屋损另核，不能把押金都叫作日期费。", "Proving residence needs no look into her bedroom; wear is assessed apart. The whole deposit isn't a date fee.", "CS_re_idle");
        f.P("CS_re_terms_pc", "预览连续性见证与独立短租。", "Preview the bounded witness and the independent short lease.", "instruction_CS_route_gate");
        f.A("instruction_CS_route_gate", "global.eao_cs_route_gate", "CS_re_routes", "CS_re_notready");
        f.N("CS_re_notready", "我去认我改牌时漏掉的一段。别让工人给我补一张更漂亮的全营表。", "I'll own the stretch my renumbering skipped. Don't let the crew draw me a prettier roster than the truth.", "CS_re_bye_pc");
        f.N("CS_re_routes", "限定见证让租期接着记；另一路封旧争议、签真实短租。两路都认你过去住过。", "A bounded witness lets the lease run on; the other seals the dispute and signs an honest short lease. Both admit you lived there.", "CS_re_route_c_pc", "CS_re_route_e_pc", "CS_re_stop_pc");
        f.P("CS_re_route_c_pc", "确认执行：跨巷限定居住见证。", "Confirm: the cross-lane bounded residence witness.", "instruction_CS_route_continuity");
        f.A("instruction_CS_route_continuity", "eao_cs_bry_01_route_continuity", "CS_re_after_c");
        f.N("CS_re_after_c", "我删的那段有补记，还有我的名字；错不能只写成旧本子坏了。", "The stretch I erased now has a re-entry — with my name on it. The fault can't be written off as an old book rotting.", "CS_re_bye_pc");
        f.P("CS_re_route_e_pc", "确认执行：撤争议租约，独立短租与申诉。", "Confirm: withdraw the disputed lease; independent short lease and appeal.", "instruction_CS_route_exit");
        f.A("instruction_CS_route_exit", "eao_cs_bry_01_route_exit", "CS_re_after_e");
        f.N("CS_re_after_e", "这一户的两种安排都归档了。看条款不写完成，办完的也不再重选。", "Both arrangements for this household are filed. Reading terms wrote nothing finished, and a finished case is never re-chosen.", "CS_re_bye_pc");
        f.P("CS_re_receipt_pc", "追问近来的公事。", "Ask about recent public business.", "instruction_CS_receipt_pick");
        f.A("instruction_CS_receipt_pick", "global.eao_cs_receipt_pick",
            "CS_re_civic_undone", "CS_re_civic_done", "CS_re_sep_undone", "CS_re_sep_done", "CS_re_patron_undone", "CS_re_patron_done");
        f.N("CS_re_civic_undone", "有地方见证席，不等这户日期已经认过；我们只补她这一段。", "A local witness seat exists; it doesn't wait on this household's dates being acknowledged. We mend her stretch only.", "CS_re_bye_pc");
        f.N("CS_re_civic_done", "下一户的日期我再独查，不用这一户办完的见证省掉询问。", "The next household I query from scratch; one finished witness case doesn't spare the asking.", "CS_re_bye_pc");
        f.N("CS_re_sep_undone", "两份合同分别办。她退不退租，不与赫林那户绑一份钱。", "Two contracts, handled apart. Whether she stays isn't knotted into Herring's purse.", "CS_re_bye_pc");
        f.N("CS_re_sep_done", "她已有自己的租约，后来再谈费用也不和另一家押金并袋。", "She holds her own lease now; later costs won't share a pouch with the other house's deposit.", "CS_re_bye_pc");
        f.N("CS_re_patron_undone", "赞助保的那几门不管她这份旧日子。用公共痕，不拿她进名单换日期。", "The patron's protected gates don't cover her old days. Use the public traces; don't trade her name on a list for dates.", "CS_re_bye_pc");
        f.N("CS_re_patron_done", "旧名单影响过谁留着，后来租客不靠重新进那名单才能认日子。", "Who the old list touched stays on record; later tenants needn't re-enter it to prove their days.", "CS_re_bye_pc");
        f.P("CS_re_bye_pc", "告辞。", "Farewell.");
        f.P("CS_re_stop_pc", "先停在这里。", "Stop here for now.");
        return f.Code("eao_cs_rena_resume", "CS_re_idle", "CS_re_after_c", "CS_re_after_e");
    }
    private static string LukanFlow()
    {
        var f = new Flow("eao_cs_lukan", "EAO_Lukan");
        f.N("CS_ru_idle", "这段堤我看得见。你说他们都答应，我看不见。", "I can see this stretch of dike. That they all agreed — that I can't see.", "CS_ru_bye_pc");
        f.N("CS_ru_intro", "这段完时她还住旧巷。后一段，她每天从新巷来。", "When this stretch ended she still lived in the old lane. In the next, she came each day from the new one.", "CS_ru_ask_pc", "CS_ru_bye_pc");
        f.P("CS_ru_ask_pc", "只记这户、这段见过的日期，愿意吗？", "Only the dates you saw, for this household — will you sign to that?", "CS_ru_answer");
        f.N("CS_ru_answer", "有。你少做过那半班也有，欠你的工钱不是拿这半班全抹。", "They happened. You skipped half a shift and they still did; the wages owed you aren't wiped by that half.", "CS_ru_witness_pc");
        f.P("CS_ru_witness_pc", "把有限亲历与门框痕分别保存。", "Keep the bounded witness and the doorframe marks apart.", "instruction_CS_witness");
        f.A("instruction_CS_witness", "eao_cs_bry_01_witness_mark", "CS_ru_signed");
        f.N("CS_ru_signed", "我签我见过的日子。中间不知道的，不替她编满。", "I'll sign the days I saw. What I don't know in between, I won't fill in for her.", "CS_ru_bye_pc");
        f.P("CS_ru_bye_pc", "回头见。", "Until later.");
        return f.Code("eao_cs_lukan_resume", "CS_ru_idle", "CS_ru_intro", "CS_ru_signed");
    }
    private static string MalerFlow()
    {
        var f = new Flow("eao_cs_maler", "EAO_Maler");
        f.N("CS_ma_idle", "新屋不漏雨。我换给你还吃了修房钱，难道不能另立租约？", "The new room doesn't leak. I swapped it at my repair cost — can't we simply sign afresh?", "CS_ma_wear_pc", "CS_ma_days_pc", "CS_ma_trade_pc", "CS_ma_bye_pc");
        f.P("CS_ma_wear_pc", "过去的押金怎么算？", "What happens to the old deposit?", "CS_ma_wear");
        f.N("CS_ma_wear", "过去的押金仍要算屋损，不能只挑对你好的字。", "The old deposit still owes for wear. You can't keep only the words that suit you.", "CS_ma_idle");
        f.P("CS_ma_days_pc", "你认她住过的那段日子吗？", "Do you acknowledge the days she lived there?", "CS_ma_days");
        f.N("CS_ma_days", "我可以认那段日子。坏门铰的钱还得另算。", "I can acknowledge those days. The broken hinge is billed separately.", "CS_ma_idle");
        f.P("CS_ma_trade_pc", "她若搬走呢？", "And if she moves out?", "CS_ma_trade");
        f.N("CS_ma_trade", "她若走，我少一户熟客。我认少赚，不让这笔少赚变成她多住的债。", "If she leaves I lose a steady tenant. I'll take the smaller earning — not turn it into a debt she pays by staying.", "CS_ma_idle");
        f.N("CS_ma_after_e", "钥回来了，日期没归我收回去。", "The key came back. The dates were never mine to reclaim.", "CS_ma_bye_pc");
        f.P("CS_ma_bye_pc", "告辞。", "Farewell.");
        return f.Code("eao_cs_maler_resume", "CS_ma_idle", "CS_ma_after_e");
    }
    private static string MiloFlow()
    {
        var f = new Flow("eao_svc_milo", "EAO_Milo");
        f.N("SVC_milo_base", "为小批港货核对样扣、布样与纸样并誊写普通运单；不触原银行、海关与货栈账。", "Small harbour lots checked — buckles, cloth, paper — and ordinary waybills copied. The bank, customs and warehouse ledgers are not touched.", "CS_svc_stock_pc", "CS_svc_bounds_pc", "CS_svc_bye_pc");
        f.N("SVC_milo_plus1", "为小批港货核对样扣、布样与纸样并誊写普通运单。今天起给你留一个优先时段。", "Small harbour lots checked and ordinary waybills copied. A priority time slot is kept for you from today.", "CS_svc_stock_pc", "CS_svc_bounds_pc", "CS_svc_bye_pc");
        f.N("SVC_milo_plus2", "为小批港货核对样扣、布样与纸样并誊写普通运单。可以约一次旁听位，不代投票。", "Small harbour lots checked and ordinary waybills copied. One listening seat may be booked — no proxy voting.", "CS_svc_stock_pc", "CS_svc_bounds_pc", "CS_svc_bye_pc");
        f.P("CS_svc_stock_pc", "看本班的有限库存。", "See this desk's limited stock.", "SVC_milo_stock");
        f.N("SVC_milo_stock", "样扣核验：每批3件；布样核验：每批2幅；运单誊写：每案1份。一批案件结束前不刷新样料，缺额如实待办。", "Buckle checks: three a lot. Cloth checks: two bolts. Waybills: one per case. Samples don't restock before a case batch closes; shortfalls stay listed.", "CS_svc_bye_pc");
        f.P("CS_svc_bounds_pc", "这班不能做什么？", "What won't this desk do?", "SVC_milo_bounds");
        f.N("SVC_milo_bounds", "不借原督工或银行名义；不代写欠据；负声望也保港口基本通行。", "No guild or bank name lent; no debt notes written; low standing still keeps basic harbour passage.", "CS_svc_bye_pc");
        f.P("CS_svc_bye_pc", "告辞。", "Farewell.");
        return f.Code("eao_svc_milo_resume", "SVC_milo_base", "SVC_milo_plus1", "SVC_milo_plus2");
    }
    private static string StreetFlow()
    {
        var f = new Flow("eao_cs_street", "EAO_Street");
        f.N("CS_street_hub", "想听布林今天说什么？街面上的话，听过就算。", "Want to hear what Brynn says today? Street talk — hear it and let it go.", "CS_town_pc", "CS_street_bye_pc");
        f.P("CS_town_pc", "听听街上的说法。", "Hear the street.", "instruction_CS_town_pool");
        f.A("instruction_CS_town_pool", "global.eao_pool_town_bry", "TG_BRY_01", "TG_BRY_02", "TG_BRY_03", "TG_BRY_04");
        f.N("TG_BRY_01", "新会定了工价以后，手艺好的和手艺差的拿一样的钱。有人欢喜有人骂。", "Since the Guild set the rates, good hands and clumsy hands earn the same. Some cheer, some curse.", "CS_town_again_pc");
        f.N("TG_BRY_02", "布林的买卖看码头，码头看风向。风向一变，价就跟着变。", "Brynn's trade watches the docks, and the docks watch the wind. Wind shifts, prices follow.", "CS_town_again_pc");
        f.N("TG_BRY_03", "夜里巡的是老楼那几条巷子。灯亮着的地方反而少去。", "Night patrols stick to the old-tower lanes. The well-lit spots we visit least.", "CS_town_again_pc");
        f.N("TG_BRY_04", "城墙之内的事办完以后，工班换了两次人。换人不换活。", "After the matter inside the walls, the crew changed twice. The work did not.", "CS_town_again_pc");
        f.P("CS_town_again_pc", "再听一句。", "One more.", "instruction_CS_town_pool");
        f.N("CS_street_cold", "布林人不记仇，只记账。你那笔，最近没人替你划。", "Brynn folk keep no grudges, only ledgers. Lately nobody strikes your entry.", "CS_street_hub");
        f.N("CS_street_hot", "你走这条街，摊主会先点头。点头不算折扣，算熟。", "Walk this street and the stalls nod first. A nod is not a discount - it is being known.", "CS_street_hub");
        f.P("CS_street_bye_pc", "先这样。", "That's all for now.");
        return f.Code("eao_cs_street_resume", "CS_street_hub", "CS_street_cold", "CS_street_hot");
    }

    internal static void Prepare()
    {
        foreach (var n in new[] { "cs_pelan", "cs_maler", "cs_rena", "cs_lukan", "cs_street" })
            Msl.AddObject("o_eao_" + n, parentName: "o_simple_NPC", isVisible: true);
        Msl.AddObject("o_eao_svc_milo", parentName: "o_simple_NPC", isVisible: true);
    }
    internal static void Configure(Action<UndertaleGameObject, string, EventType, uint> set, ModFile files)
    {
        var stubs = string.Concat(new[] {
            files.GetCode("cs_bry_01_entry.gml"), files.GetCode("cs_bry_01_hub.gml"),
            files.GetCode("cs_bry_01_route_continuity.gml"), files.GetCode("cs_bry_01_route_exit.gml"),
            files.GetCode("cs_bry_01_feedback_1_early.gml"), files.GetCode("cs_bry_01_feedback_1_late.gml"),
            files.GetCode("cs_bry_01_feedback_2_early.gml"), files.GetCode("cs_bry_01_feedback_2_late.gml"),
            files.GetCode("cs_bry_01_feedback_3_early.gml"), files.GetCode("cs_bry_01_feedback_3_late.gml"),
            files.GetCode("cs_bry_01_refusal.gml"), files.GetCode("cs_bry_01_absent.gml"),
            files.GetCode("cs_bry_01_before_city.gml"), files.GetCode("cs_bry_01_after_city.gml"),
            files.GetCode("cs_system_helpers.gml")
        });
        var npcs = new[] {
            ("cs_pelan", "租客佩兰", "Pelan the tenant", "s_peasantfemale_06", "s_peasantfemale_06P", PelanResume() + PelanFlow()),
            ("cs_maler", "房东麦勒", "Maler the landlord", "s_peasantmale_13", "s_peasantmale_13P", MalerResume() + MalerFlow()),
            ("cs_rena", "登记员蕾娜·维尔", "Rena Verl the registrar", "s_peasantfemale_03", "s_peasantfemale_03P", RenaResume() + RenaFlow()),
            ("cs_lukan", "灰堤领班鲁坎", "Lukan the dike foreman", "s_peasantmale_13", "s_peasantmale_13P", LukanResume() + LukanFlow()),
            ("svc_milo", "核验班米罗·账", "Milo the ledger clerk", "s_peasantmale_13", "s_peasantmale_13P", MiloResume() + MiloFlow()),
            ("cs_street", "布林街坊", "A Brynn street voice", "s_peasantfemale_06", "s_peasantfemale_06P", StreetResume() + StreetFlow())
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
        // A refused tenant keeps her bounded refusal line; a dead or absent
        // tenant stops new lines entirely (her instance leaves the quarter).
        set(Msl.GetObject("o_eao_cs_pelan"), "event_inherited(); if (!instance_exists(o_dialogue) && ds_map_exists(global.characterDataMap, \"EAO_presence_CS_BRY_01\")) { var _p = ds_map_find_value(global.characterDataMap, \"EAO_presence_CS_BRY_01\"); if (_p == \"absent\" || _p == \"dead\") instance_destroy(); }", EventType.Step, 0);
    }
}
