using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Decompiler;

internal static class EaoInteraction
{
    public static void ValidateStructReceiver(string assembly)
    {
        if (Regex.IsMatch(assembly, @"conv\.v\.i\s+pop\.v\.v \[stacktop\]"))
            throw new InvalidDataException("Courier Create coerces a struct receiver to an integer instance index (0.1.4 regression).");
    }
    public static void Validate(UndertaleData data)
    {
        var courier = data.GameObjects.Single(o => o.Name.Content == "o_eao_courier");
        if (courier.ParentId?.Name.Content != "o_simple_NPC") throw new InvalidDataException("Courier does not inherit the native simple NPC.");
        string Assembly(string name) {
            var code = data.Code.Single(c => c.Name.Content == name);
            return code.Disassemble(data.Variables, data.CodeLocals.For(code));
        }
        foreach (var kind in new[] { EventType.Mouse, EventType.Draw }) {
            var subtype = kind == EventType.Mouse ? 4U : 0U;
            var evt = courier.Events[(int)kind].Single(e => e.EventSubtype == subtype);
            if (!Assembly(evt.Actions.Single().CodeId.Name.Content).Contains("event_inherited")) throw new InvalidDataException("Courier bypasses native click/rendering.");
        }
        var create = Assembly("gml_Object_o_eao_courier_Create_0");
        // A struct receiver must not be coerced to an integer object index.
        // This rejects the actual broken 0.1.4 bytecode, including after a
        // data.win roundtrip; array-index conversions are not affected.
        ValidateStructReceiver(create);
        var flowStart = create.IndexOf("push.s \"{\\\"RootFragment", StringComparison.Ordinal);
        if (flowStart < 0) throw new InvalidDataException("Compiled flow initializer missing.");
        var registration = create[flowStart..];
        if (Regex.Matches(registration, @"call\.i variable_struct_set\(argc=3\)").Count != 14 ||
            Regex.Matches(registration, @"call\.i array_get\(argc=2\)").Count != 3)
            throw new InvalidDataException("Courier dialogue registration bypasses explicit native struct/array access.");
        foreach (var required in new[] { "event_inherited", "scr_unit_interactive_init", "json_parse", "__dialogue_flow_data", "npc_lines_map", "instruction_EAO_resume", "eao_mq01" })
            if (!create.Contains(required)) throw new InvalidDataException("Missing native dialogue setup: " + required);
        var step = Assembly("gml_Object_o_eao_controller_Step_1");
        foreach (var forbidden in new[] { "mouse_clear", "mouse_check_button", "keyboard_check", "scr_guiCreateSimple", "skill_can_cast", "panel_open", "open_requested" })
            if (step.Contains(forbidden)) throw new InvalidDataException("Custom UI/input lock survived: " + forbidden);
        foreach (var native in new[] { "gml_Object_o_simple_NPC_Mouse_4", "gml_Object_o_simple_NPC_Other_23", "gml_GlobalScript_scr_npc_interact_start_dialogue", "gml_GlobalScript_scr_dialogue_start", "gml_GlobalScript_DialogueFlow" })
            if (!data.Code.Any(c => c.Name.Content == native)) throw new InvalidDataException("Required native dialogue resource missing: " + native);
        // Inspect the compiled JSON, not a source-only mirror: all edges and text
        // must survive GML quoting, compilation, and data.win serialization.
        var literals = data.Code.Single(c => c.Name.Content == "gml_Object_o_eao_courier_Create_0").Instructions
            .Select(i => i.Value).OfType<UndertaleResourceById<UndertaleString, UndertaleChunkSTRG>>().Select(s => s.Resource.Content).ToArray();
        using var flow = JsonDocument.Parse(literals.Single(s => s.StartsWith("{\"RootFragment\":\"eao_mq01\"")));
        using var lines = JsonDocument.Parse(literals.Single(s => s.StartsWith("{\"EAO_intro\":")));
        var fragments = flow.RootElement.GetProperty("Fragments");
        var specs = flow.RootElement.GetProperty("Specs");
        foreach (var fragment in fragments.EnumerateObject()) {
            var edges = fragment.Value.ValueKind == JsonValueKind.Array ? fragment.Value.EnumerateArray().Select(v => v.GetString()!) : new[] { fragment.Value.GetString()! };
            foreach (var edge in edges) if (edge != "@dialogue_end" && !fragments.TryGetProperty(edge, out _)) throw new InvalidDataException("Broken native dialogue edge: " + edge);
            if (!fragment.Name.StartsWith("instruction_") && fragment.Name != "eao_mq01" && !lines.RootElement.TryGetProperty(fragment.Name, out _)) throw new InvalidDataException("Missing native localization: " + fragment.Name);
            if (fragment.Name.EndsWith("_pc") && !specs.GetProperty(fragment.Name).GetProperty("technical").GetBoolean()) throw new InvalidDataException("Recovery option can disappear after being seen.");
        }
        foreach (var instruction in new[] { "instruction_EAO_accept", "instruction_EAO_verren", "instruction_EAO_copy", "instruction_EAO_recover" })
            if (!specs.GetProperty(instruction).GetProperty("action").GetBoolean()) throw new InvalidDataException("State change can execute during option preview.");
        if (flow.RootElement.GetProperty("Speakers").GetProperty("Player").GetArrayLength() != 13) throw new InvalidDataException("Player choice speaker mismatch.");
        if (!lines.RootElement.GetProperty("EAO_intro")[1].GetString()!.Contains("一张货运收条")) throw new InvalidDataException("Chinese text was corrupted by string escaping.");
        foreach (var line in lines.RootElement.EnumerateObject())
            if (line.Value[1].GetString()!.Length > 100 || line.Value[1].GetString()!.Contains('\n')) throw new InvalidDataException("A document was moved back into long dialogue: " + line.Name);
        EaoDocuments.Validate(data);
        EaoTestTeleport.Validate(data);
    }
}
