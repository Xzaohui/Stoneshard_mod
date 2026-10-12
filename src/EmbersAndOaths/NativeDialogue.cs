using System.Text;
using System.Text.Encodings.Web;
using System.Text.Json;

namespace EmbersAndOaths;

internal static class NativeDialogue
{
    internal static string ActionsCode()
    {
        const string state = "var _state = 0;\nif (ds_map_exists(global.characterDataMap, \"EAO_MQ01\")) _state = ds_map_find_value(global.characterDataMap, \"EAO_MQ01\");\n";
        var code = new StringBuilder();
        code.AppendLine("eao_resume = function() {" + state +
            "if (_state >= 2) return 3; if (_state == 0) return 0;\n" +
            "if (" + NativeDocuments.ReadCheck + ") return 2; return 1;\n};");
        code.AppendLine("eao_accept = function() {" + state +
            "if (_state != 0) return 0;\n" + NativeDocuments.GiveCode(NativeDocuments.Originals, 1) +
            "ds_map_set(global.characterDataMap, \"EAO_schema\", 2);\n" +
            "ds_map_set(global.characterDataMap, \"EAO_MQ01\", 1); return 0;\n};");
        foreach (var choice in new[] { "verren", "copy_first" }) {
            var method = choice == "verren" ? "eao_register_verren" : "eao_register_copy";
            code.AppendLine(method + " = function() {" + state +
                "if (_state >= 2) return 0; if (_state != 1) return 2;\n" +
                "if (!(" + NativeDocuments.ReadCheck + ")) return 1;\n" +
                "if (!(" + NativeDocuments.CarryCheck + ")) return 2;\n" +
                NativeDocuments.GiveCode("[o_inv_eao_copy]", 3) +
                "ds_map_set(global.characterDataMap, \"EAO_schema\", 2);\n" +
                "ds_map_set(global.characterDataMap, \"EAO_E01\", \"copied\");\n" +
                "ds_map_set(global.characterDataMap, \"EAO_register_lead\", \"outer_harbor\");\n" +
                "ds_map_set(global.characterDataMap, \"EAO_MQ01_choice\", " + NativeDocuments.Quote(choice) + ");\n" +
                "ds_map_set(global.characterDataMap, \"EAO_MQ01_reward\", 1);\n" +
                "ds_map_set(global.characterDataMap, \"EAO_MQ01\", 2); return 0;\n};");
        }
        code.AppendLine("eao_recover = function() {" + state +
            "if (_state == 0) return 1;\n" +
            NativeDocuments.GiveCode("(_state >= 2 ? [o_inv_eao_letter, o_inv_eao_enclosure, o_inv_eao_receipt, o_inv_eao_copy] : " + NativeDocuments.Originals + ")", 1) +
            "ds_map_set(global.characterDataMap, \"EAO_schema\", 2); return 0;\n};");
        return code.ToString();
    }

    internal static string DataCode()
    {
        var fragments = new Dictionary<string, object> {
            ["eao_mq01"] = "instruction_EAO_resume",
            ["instruction_EAO_resume"] = new[] { "EAO_intro", "EAO_pending", "EAO_evidence", "EAO_done" },
            ["EAO_intro"] = new[] { "EAO_accept_pc", "EAO_later_pc" },
            ["EAO_accept_pc"] = "instruction_EAO_accept",
            ["instruction_EAO_accept"] = new[] { "EAO_pending", "EAO_full" },
            ["EAO_later_pc"] = "@dialogue_end",
            ["EAO_pending"] = new[] { "EAO_recover_pending_pc", "EAO_leave_pending_pc" },
            ["EAO_recover_pending_pc"] = "instruction_EAO_recover",
            ["EAO_leave_pending_pc"] = "@dialogue_end",
            ["instruction_EAO_recover"] = new[] { "EAO_delivered", "EAO_full" },
            ["EAO_delivered"] = new[] { "EAO_delivered_close_pc" },
            ["EAO_delivered_close_pc"] = "@dialogue_end",
            ["EAO_evidence"] = new[] { "EAO_verren_pc", "EAO_copyfirst_pc", "EAO_defer_pc" },
            ["EAO_verren_pc"] = "instruction_EAO_verren",
            ["instruction_EAO_verren"] = new[] { "EAO_done", "EAO_pending", "EAO_missing", "EAO_full" },
            ["EAO_copyfirst_pc"] = "instruction_EAO_copy",
            ["instruction_EAO_copy"] = new[] { "EAO_done", "EAO_pending", "EAO_missing", "EAO_full" },
            ["EAO_defer_pc"] = "@dialogue_end",
            ["EAO_missing"] = new[] { "EAO_recover_missing_pc", "EAO_leave_missing_pc" },
            ["EAO_recover_missing_pc"] = "instruction_EAO_recover",
            ["EAO_leave_missing_pc"] = "@dialogue_end",
            ["EAO_done"] = new[] { "EAO_recover_done_pc", "EAO_close_pc" },
            ["EAO_recover_done_pc"] = "instruction_EAO_recover",
            ["EAO_close_pc"] = "@dialogue_end",
            ["EAO_full"] = new[] { "EAO_leave_full_pc" },
            ["EAO_leave_full_pc"] = "@dialogue_end"
        };
        var lines = new Dictionary<string, string[]> {
            ["EAO_intro"] = new[] { "Toman told me to find Verren's caravan. I have a delayed letter, an enclosed extract and a freight receipt. Will you take them?", "托曼叫我来找维伦的商队。这里有一封迟送的信、一张附纸和一张货运收条，你愿意收下吗？" },
            ["EAO_pending"] = new[] { "Read all three papers in your inventory, then bring them back for comparison. If any are missing, I can supply a copy.", "先从背包读完迟信、附纸和收条，再带来核对。文书缺失的话，我可以补给你一份。" },
            ["EAO_evidence"] = new[] { "You've read all three? Their dates and numbers match. Shall we register the lead for Verren or make your copy first?", "三份都读过了？日期和编号对得上。我们登记供维伦核对，还是先留好你的抄本？" },
            ["EAO_done"] = new[] { "The lead is registered. Keep the comparison copy in your inventory for the warehouse inquiry. I can replace missing papers.", "货运线索已登记。把核对抄本留在背包里，查仓库档案时还用得上。文书缺失的话可以来补领。" },
            ["EAO_missing"] = new[] { "Bring the three papers from your inventory or bag. If they are in the caravan stash, retrieve them first; lost papers can be replaced.", "把三份文书带在背包或随身袋里再来。存在商队箱里的先取出来；丢失的可以补领。" },
            ["EAO_full"] = new[] { "There isn't enough inventory space for this handover. Make room and return; the handover has not been recorded.", "背包放不下这次交付的文书。腾出位置再来，这次交接还没有登记。" },
            ["EAO_delivered"] = new[] { "Keep the papers safe. Read them from your inventory, then return when you are ready.", "文书收好。从背包打开阅读，核对好后再来找我。" },
            ["EAO_accept_pc"] = new[] { "Take the three papers.", "收下三份文书。" },
            ["EAO_later_pc"] = new[] { "I'll come back later.", "以后再来。" },
            ["EAO_recover_pending_pc"] = new[] { "Collect any missing papers.", "领取缺失的文书。" },
            ["EAO_leave_pending_pc"] = new[] { "I'll read them first.", "我先去阅读。" },
            ["EAO_delivered_close_pc"] = new[] { "Put the papers away.", "收好文书。" },
            ["EAO_verren_pc"] = new[] { "Register the lead for Verren.", "登记供维伦核对。" },
            ["EAO_copyfirst_pc"] = new[] { "Make my copy first.", "先留好我的抄本。" },
            ["EAO_defer_pc"] = new[] { "I'll decide later.", "稍后再决定。" },
            ["EAO_recover_missing_pc"] = new[] { "Replace the lost papers.", "补领丢失的文书。" },
            ["EAO_leave_missing_pc"] = new[] { "I'll retrieve them.", "我去取文书。" },
            ["EAO_recover_done_pc"] = new[] { "Collect missing papers and the comparison copy.", "补领缺失文书和核对抄本。" },
            ["EAO_close_pc"] = new[] { "Farewell.", "告辞。" },
            ["EAO_leave_full_pc"] = new[] { "I'll make room.", "我去腾位置。" }
        };
        var player = lines.Keys.Where(k => k.EndsWith("_pc")).ToArray();
        var npc = lines.Keys.Where(k => !k.EndsWith("_pc")).ToArray();
        var specs = new Dictionary<string, object> { ["eao_mq01"] = new { hub = true } };
        foreach (var key in player) specs[key] = new { technical = true };
        foreach (var key in new[] { "instruction_EAO_accept", "instruction_EAO_verren", "instruction_EAO_copy", "instruction_EAO_recover" }) specs[key] = new { action = true };
        var flow = new { RootFragment = "eao_mq01", Monologue = false, Fragments = fragments,
            Speakers = new Dictionary<string, string[]> { ["EAO_Courier"] = npc, ["Player"] = player }, Specs = specs, Scripts = new Dictionary<string, string>() };
        return Register(flow, lines, new Dictionary<string, string> {
            ["instruction_EAO_resume"] = "eao_resume", ["instruction_EAO_accept"] = "eao_accept",
            ["instruction_EAO_verren"] = "eao_register_verren", ["instruction_EAO_copy"] = "eao_register_copy",
            ["instruction_EAO_recover"] = "eao_recover"
        });
    }

    internal static string Register(object flow, object lines, Dictionary<string, string> callbacks)
    {
        var jsonOptions = new JsonSerializerOptions { Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping };
        string Quote(object value) => JsonSerializer.Serialize(JsonSerializer.Serialize(value, jsonOptions), jsonOptions);
        return "\nvar _flow = json_parse(" + Quote(flow) + ");\n" +
            "var _scripts = variable_struct_get(_flow, \"Scripts\");\n" +
            string.Concat(callbacks.Select(pair => "variable_struct_set(_scripts, " + NativeDocuments.Quote(pair.Key) + ", " + pair.Value + ");\n")) +
            "variable_struct_set(global.__dialogue_flow_data, variable_struct_get(_flow, \"RootFragment\"), _flow);\n" +
            "var _lines = json_parse(" + Quote(lines) + ");\n" +
            "var _keys = variable_struct_get_names(_lines);\n" +
            "for (var _i = 0; _i < array_length(_keys); _i++) {\n" +
            "    var _key = array_get(_keys, _i);\n" +
            "    var _texts = variable_struct_get(_lines, _key);\n" +
            "    var _row = json_parse(\"[{\\\"can_skip_checks\\\":true}]\");\n" +
            "    var _line = array_get(_row, 0);\n" +
            "    variable_struct_set(_line, \"key\", _key);\n" +
            "    variable_struct_set(_line, \"sex\", undefined);\n" +
            "    variable_struct_set(_line, \"occupation\", undefined);\n" +
            "    variable_struct_set(_line, \"playertype\", undefined);\n" +
            "    variable_struct_set(_line, \"faction\", undefined);\n" +
            "    variable_struct_set(_line, \"settlement\", undefined);\n" +
            "    variable_struct_set(_line, \"any_playertype\", true);\n" +
            "    variable_struct_set(_line, \"line_text\", array_get(_texts, global.language == 3 ? 1 : 0));\n" +
            "    ds_map_set(global.npc_lines_map, _key, _row);\n" +
            "}\n";
    }
}
