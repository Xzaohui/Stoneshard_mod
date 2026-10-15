using System.Text;
using System.Text.Encodings.Web;
using System.Text.Json;

namespace EmbersAndOaths;

internal static class NativeDocuments
{
    internal sealed record Document(string Id, string NameCn, string NameEn, string TextCn, string TextEn);
    private static readonly Document[] Core = {
        new("eao_letter", "迟送的信", "Delayed Letter",
            "致维伦：\n\n离开的器具不是第二颗晶石。有人把部件装进木箱，随船运走。我没有看见箱内全貌，无法断言它们的用途。\n\n货单上的名字被盐痕盖住，日期和编号还可辨认。随信附上一张摘录和货运收条，请先比日期，再比印章。\n\n托曼知道怎样找到你的商队。原修院的档案仍值得查；这笔货运也许能补上另一段记录。\n\n——未署名",
            "To Verren,\n\nThe departed instruments are not another shard. Parts left by ship in wooden crates. I did not see their contents and cannot establish their purpose.\n\nSalt obscures the consignee's name, but the date and number remain. I enclose an extract and a freight receipt. Compare the date, then the seal.\n\nToman can find your caravan. The monastery archives remain a lead; this shipment may supply another record.\n\nUnsigned"),
        new("eao_enclosure", "随信附纸", "Enclosed Extract",
            "货单摘录\n\n日期：十二日（月名模糊）。\n批次：外港·四十七。\n货物：拆分器具，密封木箱。\n收货人：字迹被盐痕遮住。\n\n摘录边缘留着半枚仓库印章。另一张纸上若有同日、同号的记录，便可交叉核对。\n\n摘录只说明有人登记过这批货物，不能证明箱内器具的用途，也不能替葛文涅尔免责。",
            "Manifest extract\n\nDate: the twelfth (month illegible).\nConsignment: Outer Harbor, forty-seven.\nCargo: disassembled instruments, sealed wooden crates.\nConsignee: obscured by salt.\n\nHalf a warehouse seal survives at the margin. Match a record bearing the same date and number.\n\nThis is a shipment record, not proof of the instruments' purpose or Gwynnel's innocence."),
        new("eao_receipt", "货运收条", "Freight Receipt",
            "运费收讫\n\n日期：十二日（月名模糊）。\n批次：外港·四十七。\n暂存地点：布林外港旧仓。\n货物：密封木箱，拆分器具。\n晶石：未列入本单。\n\n印章残角与附纸相合，完整印记仍需到仓库档案中查证。\n\n此单仅为运费凭证，货物是否如实申报尚未核实。",
            "Freight paid\n\nDate: the twelfth (month illegible).\nConsignment: Outer Harbor, forty-seven.\nHolding site: the old warehouse at Brynn's outer harbor.\nCargo: sealed crates of disassembled instruments.\nShard: not listed.\n\nThe surviving seal matches the extract. The complete seal awaits inspection in warehouse records.\n\nA freight receipt does not establish whether the cargo declaration was truthful."),
        new("eao_copy", "货运核对抄本", "Shipment Comparison Copy",
            "迟信、附纸与收条核对记录\n\n两份货运记录的日期与编号一致，印章残角相合。\n线索地点：布林外港旧仓。\n登记货物：密封木箱中的拆分器具；收条未列晶石。\n\n后续调查应先查仓库档案，复核完整印章、收货人及箱内实物。现有纸张尚不能证明器具的用途，也不能替葛文涅尔免责。\n\n原件与本抄本均可保存，作为共同调查的依据。",
            "Comparison of letter, extract and receipt\n\nThe two shipment records share a date and number; their surviving seals match.\nLead: the old warehouse at Brynn's outer harbor.\nDeclared cargo: disassembled instruments in sealed crates; no shard listed.\n\nConsult warehouse records to verify the full seal, consignee and contents. These papers establish neither the instruments' purpose nor Gwynnel's innocence.\n\nKeep the originals and this copy for the investigation.")
    };
    internal static readonly Document[] All = Core.Concat(new Document[] {
        new("eao_permit", "封账仓查档许可", "Sealed Warehouse Permit",
            "外港封账仓·有限查档许可\n\n持货运核对抄本者可查阅外港四十七号的留存档案。许可不授权打开未登记货箱，不免除盗窃或伤人责任。\n\n取回日期相符的盐封货单、装箱记录与印章对照纸，读过后交仓务员登记。档案室在仓库楼上；调查完成后原路离开。\n\n本许可由本仓签发，并非布林城议会的通行令。",
            "Limited archive permit\n\nThe bearer of the comparison copy may inspect records for Outer Harbor forty-seven. This does not authorize opening other crates or excuse theft or violence.\n\nRetrieve and read the salt-stained manifest, packing record and seal comparison, then register them with the clerk. The archives are upstairs; return by the same route.\n\nIssued by this warehouse, not Brynn's council."),
        new("eao_manifest", "盐封货单", "Salt-stained Manifest",
            "留存货单·外港四十七\n\n日期：十二日（月名模糊）。\n货物：三个木箱，器具部件。\n费用：已付；付款人一栏被刮去。\n暂存：外港旧仓，封账后移入档案室。\n后段运输：旧渠卸货点，夜班第二次交接。\n\n完整仓印与收条残角可互相核对。货单没有记载第二颗晶石，也没有说明这些器具的用途。收货人缺失仍不能据此归罪任何势力。",
            "Retained manifest: Outer Harbor forty-seven\n\nDate: the twelfth, month illegible.\nCargo: three crates of instrument parts.\nFreight paid; payer erased.\nHeld at the old warehouse, then archived.\nNext transfer: the old canal unloading point, second night-shift handover.\n\nThe full warehouse seal can be compared with the receipt. No second shard or instrument purpose is recorded. An absent consignee does not establish any faction's guilt."),
        new("eao_packing", "器具装箱记录", "Instrument Packing Record",
            "装箱记录·外港四十七\n\n一号箱：黄铜架与固定环。\n二号箱：拆下的镜片支座，镜片未登记。\n三号箱：包裹好的导管，未注明用途。\n\n验收只检查箱数与外封；记录员没有打开全部包裹。不得把部件名称当作完整器具的证明。\n\n边注：下一段由旧渠搬运班接手。若正本缺页，可向搬运者索取交接副件。",
            "Packing record: Outer Harbor forty-seven\n\nCrate one: brass frames and retaining rings.\nCrate two: detached lens mounts; no lenses recorded.\nCrate three: wrapped conduits, purpose unspecified.\n\nThe clerk checked crate counts and outer seals, not every package. Part names do not establish a complete instrument.\n\nMargin: next transfer handled by the canal crew. Obtain their duplicate if pages are missing."),
        new("eao_seal", "仓印对照纸", "Warehouse Seal Comparison",
            "仓印对照纸\n\n仓库留存完整印记与货运收条残角一致；盐封货单与装箱记录都记外港四十七、十二日。\n\n这证明三份记录指向同一批货，不证明申报内容属实。付款人被刮去，收货人未能确认。\n\n下一步：旧渠卸货点；询问搬运者，寻找第二次夜班交接的副件。在其他来源交叉核验前，迟信仍只是一条线索。",
            "Seal comparison\n\nThe retained seal matches the receipt fragment. Manifest and packing record both state Outer Harbor forty-seven, the twelfth.\n\nThis links the records to one shipment; it does not prove the declared contents. The payer was erased and the consignee remains unknown.\n\nNext: the canal unloading point and the second night-shift handover duplicate. The delayed letter remains a lead pending independent corroboration.")
    }).Concat(new Document[] {
        new("eao_notice_plg", "封条与撒灰公告", "Seal and Lime Notice",
            "此地封存，外人不得入内。石灰每七日一撒，由看守记数。代领遗物者，先在篱笆外报名，名字写在木牌背面。\n\n（阅读只给封存与报名规矩，不给通行，也不开启任何房屋。）",
            "This place is sealed; outsiders may not enter. Lime is spread every seventh day and counted by the keeper. Those claiming effects for others first give their names on the back of the board.\n\n(Reading covers the seal and the claiming rule only; it grants no passage and opens no house.)")
    }).ToArray();
    internal static string Quote(string value) => JsonSerializer.Serialize(value, new JsonSerializerOptions { Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping });
    private static string Localized(string cn, string en) => "(global.language == 3 ? " + Quote(cn) + " : " + Quote(en) + ")";

    // Run before inherited item Create, including when the native loader restores
    // inventory or ground loot. Registration cannot depend on a later Step event.
    internal static string RegistrationCode()
    {
        var code = new StringBuilder();
        foreach (var doc in All) {
            var key = Quote(doc.Id);
            code.AppendLine("if (!ds_map_exists(global.consum_stat_data, " + key + ")) {");
            code.AppendLine("    var _eao_stat = ds_map_clone(ds_map_find_value(global.consum_stat_data, \"bern_letter\"));");
            code.AppendLine("    ds_map_set(_eao_stat, \"Price\", 0); ds_map_set(_eao_stat, \"Weight\", 0.1);");
            code.AppendLine("    ds_map_add_map(global.consum_stat_data, " + key + ", _eao_stat);");
            code.AppendLine("}");
            var name = Localized(doc.NameCn, doc.NameEn);
            var description = Localized("可阅读的调查文书。", "A readable investigation document.");
            code.AppendLine("ds_map_set(global.consum_name, " + key + ", " + name + ");");
            code.AppendLine("ds_map_set(global.consum_desc, " + key + ", " + description + ");");
            code.AppendLine("ds_map_set(global.book_name, " + key + ", " + name + ");");
            code.AppendLine("ds_map_set(global.book_desc, " + key + ", " + description + ");");
            code.AppendLine("ds_map_set(global.book_type, " + key + ", " + Localized("信件", "Document") + ");");
            code.AppendLine("ds_map_set(global.book_mid_text, " + key + ", \"\");");
            var textCn = doc.TextCn + (doc.Id == "eao_copy" ? "\n\n查档路线：布林港区海关一楼，进门右侧标有“封账仓入口”的小门。完成迟信核对并读完本抄本后才能通过；随身带着它找仓务员领取许可。档案室在封账仓楼上，不在海关二楼。" : "");
            var textEn = doc.TextEn + (doc.Id == "eao_copy" ? "\n\nArchive route: the door marked Warehouse to the right of the entrance on the ground floor of Brynn's Customs House. Complete the delayed letter comparison and read this copy to unlock it; carry it when requesting a permit. The archives are upstairs in the warehouse, not on the Customs House's second floor." : "");
            code.AppendLine("ds_map_set(global.book_content, " + key + ", " + Localized(textCn, textEn) + ");");
        }
        return code.ToString();
    }

    internal static string InventoryCreate(Document doc) => RegistrationCode() + "\nevent_inherited();\n" +
        "idName = " + Quote(doc.Id) + ";\n" +
        "skill = o_open_note; skill_sprite = s_opened_note;\n" +
        "start_width = 195; font_type = global.f_dmg; line_height = -1;\n" +
        "charge = 1; i_index = 0; gain_xp = 0; script_after_close = -4;\n" +
        "delete_after_use = false; can_stack = false; max_charge = 1;\n" +
        "over_sprite = -4; shift_x = 0; identified = true;\n" +
        "scr_consum_atr(idName);\n";

    internal static string ReadCode(Document doc) =>
        "event_inherited();\n" +
        "if (instance_exists(o_open_note)) {\n" +
        "    ds_map_set(global.characterDataMap, " + Quote("EAO_read_" + doc.Id) + ", 1);\n" +
        "    ds_map_set(data, \"EAO_document_read\", 1);\n" +
        "}\n";

    internal static string LootCreate(Document doc) => RegistrationCode() + "\nevent_inherited();\n" +
        "inv_object = o_inv_" + doc.Id + "; identified = true; image_speed = 0; image_index = 0; number = 0;\n";

    // Native placement, with auto-drop disabled. Roll back only items newly
    // created in this transaction; existing papers and quest state stay intact.
    internal static string GiveCode(string objects, int failureResult) => "\n" +
        "var _inventory = instance_find(o_inventory, 0);\n" +
        "if (!instance_exists(_inventory)) return " + failureResult + ";\n" +
        "var _documents = " + objects + ";\n" +
        "var _created = array_create(0);\n" +
        "var _failed = false;\n" +
        "for (var _d = 0; _d < array_length(_documents); _d++) {\n" +
        "    var _object = array_get(_documents, _d);\n" +
        "    if (scr_instance_exists_item(_object, \"count\", false, 0) > 0) continue;\n" +
        "    var _paper = scr_inventory_add_item(_object, _inventory, -4, true, -4, false, false, false);\n" +
        "    if (!instance_exists(_paper)) { _failed = true; break; }\n" +
        "    array_push(_created, _paper);\n" +
        "    if (!scr_inventory_add(_inventory, _paper)) { _failed = true; break; }\n" +
        "}\n" +
        "if (_failed) {\n" +
        "    for (var _r = 0; _r < array_length(_created); _r++) {\n" +
        "        var _rollback = array_get(_created, _r);\n" +
        "        if (instance_exists(_rollback)) scr_item_destroy(_rollback, false);\n" +
        "    }\n" +
        "    return " + failureResult + ";\n" +
        "}\n";

    internal const string Originals = "[o_inv_eao_letter, o_inv_eao_enclosure, o_inv_eao_receipt]";
    internal static string ReadCheck => string.Join(" && ", All.Take(3).Select(d =>
        "ds_map_exists(global.characterDataMap, " + Quote("EAO_read_" + d.Id) + ") && ds_map_find_value(global.characterDataMap, " + Quote("EAO_read_" + d.Id) + ") == 1"));
    internal static string CarryCheck => string.Join(" && ", All.Take(3).Select(d =>
        "scr_instance_exists_item(o_inv_" + d.Id + ", \"count\", false, 8) > 0"));
}
