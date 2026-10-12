using System.Collections.Generic;
using System.Linq;

namespace EmbersAndOaths;

internal static class WarehouseQuest
{
    internal const string Papers = "[o_inv_eao_manifest, o_inv_eao_packing, o_inv_eao_seal]";
    internal static string ReadGate => string.Join(" && ", new[] { "manifest", "packing", "seal" }.Select(id =>
        "ds_map_exists(global.characterDataMap, \"EAO_read_eao_" + id + "\") && ds_map_find_value(global.characterDataMap, \"EAO_read_eao_" + id + "\") == 1"));
    internal static string CarryGate => string.Join(" && ", new[] { "manifest", "packing", "seal" }.Select(id =>
        "scr_instance_exists_item(o_inv_eao_" + id + ", \"count\", false, 8) > 0"));
    private const string State = "var _state = 0; if (ds_map_exists(global.characterDataMap, \"EAO_MQ02\")) _state = ds_map_find_value(global.characterDataMap, \"EAO_MQ02\");\n";
    internal static string ActionsCode() =>
        "eao_mq02_resume = function() {\n" + State +
        "if (_state >= 2) return 3; if (_state == 0) return 0; if (" + ReadGate + ") return 2; return 1;\n};\n" +
        "eao_mq02_accept = function() {\n" + State +
        "if (_state != 0) return 0;\n" +
        "if (!ds_map_exists(global.characterDataMap, \"EAO_MQ01\") || ds_map_find_value(global.characterDataMap, \"EAO_MQ01\") < 2 || !ds_map_exists(global.characterDataMap, \"EAO_read_eao_copy\") || ds_map_find_value(global.characterDataMap, \"EAO_read_eao_copy\") != 1 || scr_instance_exists_item(o_inv_eao_copy, \"count\", false, 8) <= 0) return 2;\n" +
        NativeDocuments.GiveCode("[o_inv_eao_permit]", 1) +
        "ds_map_set(global.characterDataMap, \"EAO_MQ02\", 1); ds_map_set(global.characterDataMap, \"EAO_schema\", 3); return 0;\n};\n" +
        "eao_mq02_submit = function() {\n" + State +
        "if (_state >= 2) return 0; if (_state != 1 || !(" + ReadGate + ")) return 1;\n" +
        "if (!(" + CarryGate + ")) return 2;\n" +
        "if (!ds_map_exists(global.characterDataMap, \"EAO_D01_archive_visited\") || ds_map_find_value(global.characterDataMap, \"EAO_D01_archive_visited\") != 1) return 1;\n" +
        "ds_map_set(global.characterDataMap, \"EAO_MQ02\", 2); ds_map_set(global.characterDataMap, \"EAO_cargo_trace\", 1); ds_map_set(global.characterDataMap, \"EAO_register_lead\", \"old_canal\"); ds_map_set(global.characterDataMap, \"EAO_D01_status\", \"investigated\"); return 0;\n};\n" +
        "eao_mq02_recover = function() {\n" + State +
        "if (_state == 0) return 2;\n" + NativeDocuments.GiveCode("[o_inv_eao_permit]", 1) +
        "if (ds_map_exists(global.characterDataMap, \"EAO_D01_archive_visited\") && ds_map_find_value(global.characterDataMap, \"EAO_D01_archive_visited\") == 1) {\n" +
        NativeDocuments.GiveCode(Papers, 1) + "}\nreturn 0;\n};\n";

    internal static string DataCode()
    {
        var fragments = new Dictionary<string, object> {
            ["eao_mq02"] = "instruction_EAO2_resume",
            ["instruction_EAO2_resume"] = new[] { "EAO2_intro", "EAO2_pending", "EAO2_ready", "EAO2_done" },
            ["EAO2_intro"] = new[] { "EAO2_accept_pc", "EAO2_leave_pc" },
            ["EAO2_accept_pc"] = "instruction_EAO2_accept",
            ["instruction_EAO2_accept"] = new[] { "EAO2_pending", "EAO2_full", "EAO2_missing" },
            ["EAO2_pending"] = new[] { "EAO2_recover_pc", "EAO2_read_pc" },
            ["EAO2_ready"] = new[] { "EAO2_submit_pc", "EAO2_wait_pc" },
            ["EAO2_submit_pc"] = "instruction_EAO2_submit",
            ["instruction_EAO2_submit"] = new[] { "EAO2_done", "EAO2_pending", "EAO2_missing" },
            ["EAO2_done"] = new[] { "EAO2_replace_pc", "EAO2_close_pc" },
            ["EAO2_missing"] = new[] { "EAO2_missing_recover_pc", "EAO2_missing_close_pc" },
            ["EAO2_recover_pc"] = "instruction_EAO2_recover", ["EAO2_replace_pc"] = "instruction_EAO2_recover", ["EAO2_missing_recover_pc"] = "instruction_EAO2_recover",
            ["instruction_EAO2_recover"] = new[] { "EAO2_recovered", "EAO2_full", "EAO2_missing" },
            ["EAO2_recovered"] = new[] { "EAO2_recovered_close_pc" },
            ["EAO2_full"] = new[] { "EAO2_full_close_pc" }
        };
        var lines = new Dictionary<string, string[]> {
            ["EAO2_intro"] = new[] { "You have the comparison copy? I can issue a limited archive permit. This is a warehouse inquiry, not a council order.", "带了核对抄本？我可以签一份有限查档许可。这是仓库查账，并非城议会的命令。" },
            ["EAO2_pending"] = new[] { "The archive is upstairs. Retrieve the manifest, packing record and seal comparison. Read all three, then bring them back.", "档案室在楼上。取回盐封货单、器具装箱记录和仓印对照纸，读完三份再带回来登记。" },
            ["EAO2_ready"] = new[] { "Have you compared the three records? Bring the originals with you and I will register the next transfer lead.", "三份记录都核对过了？原件带在身上，我就登记下一段运输的线索。" },
            ["EAO2_done"] = new[] { "The next transfer was at the old canal. Keep these papers: the shipment is linked, but its purpose and consignee remain unproven.", "下一段交接在旧渠。留好这些文书：货运记录对上了，器具用途和收货人仍未查明。" },
            ["EAO2_missing"] = new[] { "Retrieve the required papers from your stash, or collect replacements. The comparison copy must also be read before receiving a permit.", "先取出需要的文书，丢失的可以补领。领许可前，还需要读过并随身带着货运核对抄本。" },
            ["EAO2_recovered"] = new[] { "Missing papers have been supplied. Archive documents can only be replaced after your first visit upstairs.", "缺失文书已补给。档案材料只在你实际到过楼上档案室后补领。" },
            ["EAO2_full"] = new[] { "Make room in your inventory and return. No task completion has been recorded.", "先在背包腾出位置再来。这次没有登记任务完成。" },
            ["EAO2_accept_pc"] = new[] { "Present the copy and obtain a permit.", "出示抄本，领取查档许可。" },
            ["EAO2_leave_pc"] = new[] { "Come back later.", "稍后再来。" },
            ["EAO2_recover_pc"] = new[] { "Replace missing documents.", "补领缺失文书。" },
            ["EAO2_read_pc"] = new[] { "Inspect the archive first.", "我先去查档案。" },
            ["EAO2_submit_pc"] = new[] { "Register the compared records.", "登记核对后的记录。" },
            ["EAO2_wait_pc"] = new[] { "Check once more.", "我再核对一下。" },
            ["EAO2_replace_pc"] = new[] { "Collect missing copies.", "补领缺失的副件。" },
            ["EAO2_close_pc"] = new[] { "Farewell.", "告辞。" },
            ["EAO2_missing_recover_pc"] = new[] { "Replace lost papers.", "补领丢失的文书。" },
            ["EAO2_missing_close_pc"] = new[] { "Retrieve stored papers.", "我去取文书。" },
            ["EAO2_recovered_close_pc"] = new[] { "Put the papers away.", "收好文书。" },
            ["EAO2_full_close_pc"] = new[] { "Make room.", "我去腾位置。" }
        };
        foreach (var pc in lines.Keys.Where(k => k.EndsWith("_pc") && !fragments.ContainsKey(k))) fragments[pc] = "@dialogue_end";
        var callbacks = new Dictionary<string, string> {
            ["instruction_EAO2_resume"] = "eao_mq02_resume", ["instruction_EAO2_accept"] = "eao_mq02_accept", ["instruction_EAO2_submit"] = "eao_mq02_submit", ["instruction_EAO2_recover"] = "eao_mq02_recover"
        };
        var specs = new Dictionary<string, object> { ["eao_mq02"] = new { hub = true } };
        foreach (var pc in lines.Keys.Where(k => k.EndsWith("_pc"))) specs[pc] = new { technical = true };
        foreach (var action in callbacks.Keys.Where(k => !k.EndsWith("resume"))) specs[action] = new { action = true };
        return NativeDialogue.Register(new { RootFragment="eao_mq02", Monologue=false, Fragments=fragments,
            Speakers=new Dictionary<string,string[]> { ["EAO_Clerk"] = lines.Keys.Where(k => !k.EndsWith("_pc")).ToArray(), ["Player"] = lines.Keys.Where(k => k.EndsWith("_pc")).ToArray() }, Specs=specs, Scripts=new Dictionary<string,string>() }, lines, callbacks);
    }
}
