using System.IO;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Decompiler;

internal static class EaoDocuments
{
    public static void Validate(UndertaleData data)
    {
        string Assembly(string name) {
            var code = data.Code.Single(c => c.Name.Content == name);
            return code.Disassemble(data.Variables, data.CodeLocals.For(code));
        }
        var portrait = data.Sprites.Single(s => s.Name.Content == "s_peasantmale_13P");
        if (portrait.OriginX != 0 || portrait.OriginY != 0 || portrait.Width > 64 || portrait.Height > 64)
            throw new InvalidDataException("Courier portrait is not the native dialogue portrait geometry.");
        var courier = Assembly("gml_Object_o_eao_courier_Create_0");
        if (!Regex.IsMatch(courier, @"push(?:i\.e|\.i) " + data.Sprites.IndexOf(portrait) + @"\s+pop\.v\.i self\.avatar"))
            throw new InvalidDataException("Courier still assigns its world sprite to the portrait.");
        foreach (var id in new[] { "eao_letter", "eao_enclosure", "eao_receipt", "eao_copy", "eao_permit", "eao_manifest", "eao_packing", "eao_seal" }) {
            var inventory = data.GameObjects.Single(o => o.Name.Content == "o_inv_" + id);
            var loot = data.GameObjects.Single(o => o.Name.Content == "o_loot_" + id);
            if (inventory.ParentId?.Name.Content != "o_inv_book" || loot.ParentId?.Name.Content != "o_consument_loot" ||
                inventory.Sprite?.Name.Content != "s_inv_note" || loot.Sprite?.Name.Content != "s_loot_note")
                throw new InvalidDataException("Native document inventory/drop/pickup family mismatch: " + id);
            var create = Assembly("gml_Object_o_inv_" + id + "_Create_0");
            var read = Assembly("gml_Object_o_inv_" + id + "_Other_24");
            var lootCreate = Assembly("gml_Object_o_loot_" + id + "_Create_0");
            foreach (var required in new[] { "book_content", "book_name", "book_desc", "book_type", "consum_stat_data", "ds_map_clone", "scr_consum_atr", "event_inherited", id })
                if (!create.Contains(required)) throw new InvalidDataException("Incomplete readable document: " + id + "/" + required);
            if (create.IndexOf("consum_stat_data") > create.IndexOf("event_inherited") || lootCreate.IndexOf("consum_stat_data") > lootCreate.IndexOf("event_inherited"))
                throw new InvalidDataException("Document restore depends on a later Step event: " + id);
            if (!read.Contains("event_inherited") || !read.Contains("EAO_read_" + id) || !read.Contains("instance_exists") || read.Contains("read_diary"))
                throw new InvalidDataException("Document does not use native reading or touches original diary progress: " + id);
            if (inventory.Events[(int)EventType.Mouse].Count != 0 || inventory.Events[(int)EventType.Draw].Count != 0)
                throw new InvalidDataException("Document has a custom input or drawing path.");
        }
        foreach (var required in new[] { "scr_inventory_add_item", "scr_inventory_add", "scr_instance_exists_item", "scr_item_destroy", "EAO_read_eao_letter", "EAO_read_eao_enclosure", "EAO_read_eao_receipt" })
            if (!courier.Contains(required)) throw new InvalidDataException("Document handover/read gate missing: " + required);
        // Every added method must use native calls / callv, checked by EaoLinkage.
        foreach (var entry in data.Code.Where(c => c.ParentEntry == null && (c.Name.Content.StartsWith("gml_Object_o_inv_eao_") || c.Name.Content.StartsWith("gml_Object_o_loot_eao_")))) {
            var asm = Assembly(entry.Name.Content);
            if (Regex.IsMatch(asm, @"conv\.v\.i\s+pop\.v\.v \[stacktop\]")) throw new InvalidDataException("Unsafe document struct receiver.");
        }
    }
}
