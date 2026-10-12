using System.Collections;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Decompiler;

internal static class EaoRooms
{
    // Hash room metadata, complete layer data and instance order, referencing
    // external resources by name. No original layout/source is exported.
    public static string Fingerprint(UndertaleRoom room)
    {
        object? Snapshot(object? value, bool root=false) {
            if (value == null || value is string || value.GetType().IsPrimitive || value is decimal || value.GetType().IsEnum) return value;
            if (value is UndertaleString text) return text.Content;
            if (value is IEnumerable items) return items.Cast<object?>().Select(v => Snapshot(v)).ToArray();
            var type = value.GetType();
            if (!root && type.DeclaringType != typeof(UndertaleRoom) && type.DeclaringType?.DeclaringType != typeof(UndertaleRoom) && type.GetProperty("Name")?.GetValue(value) is UndertaleString name) return name.Content;
            var result = new SortedDictionary<string,object?>();
            foreach (var property in type.GetProperties(BindingFlags.Instance | BindingFlags.Public)) {
                if (!property.CanRead || property.GetIndexParameters().Length != 0 || property.Name.StartsWith("Parent") || property.Name is "BGColorLayer" or "ZIndex") continue;
                result[property.Name] = Snapshot(property.GetValue(value));
            }
            return result;
        }
        return Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(JsonSerializer.Serialize(Snapshot(room,true)))));
    }
    public static string[] Validate(UndertaleData data)
    {
        var passed = new List<string>();
        string Asm(string name) { var c=data.Code.Single(c=>c.Name.Content==name); return c.Disassemble(data.Variables,data.CodeLocals.For(c)); }
        foreach (var (name, template, marker) in new[] { ("r_eao_d01_warehouse","r_DockStore1floor","o_eao_d01_start"), ("r_eao_d01_archive","r_DockStore2floor","o_eao_d01_archive_start") }) {
            var room=data.Rooms.Single(r=>r.Name.Content==name); var source=data.Rooms.Single(r=>r.Name.Content==template);
            if (room.Width!=source.Width || room.Height!=source.Height || room.Views.Count!=source.Views.Count || room.Persistent || room.CreationCodeId!=null) throw new InvalidDataException("Annex room metadata mismatch: "+name);
            var instances=room.Layers.Where(l=>l.LayerType==UndertaleRoom.LayerType.Instances).SelectMany(l=>l.InstancesData.Instances).ToArray();
            if (instances.Length!=room.GameObjects.Count || instances.Distinct().Count()!=instances.Length || instances.Any(i=>!room.GameObjects.Contains(i))) throw new InvalidDataException("Annex instance/layer mapping mismatch.");
            if (room.GameObjects.Any(i=>i.ObjectDefinition.Name.Content.StartsWith("o_npc_") || i.ObjectDefinition.Name.Content is "o_chest" or "o_NPC_target" or "o_loot_marker")) throw new InvalidDataException("Original quest/trader/loot entities leaked into annex.");
            if (room.GameObjects.IndexOf(room.GameObjects.Single(i=>i.ObjectDefinition.Name.Content==marker)) >= room.GameObjects.IndexOf(room.GameObjects.Single(i=>i.ObjectDefinition.Name.Content=="o_abstract_player"))) throw new InvalidDataException("Landing marker initialized after native player.");
            foreach(var instance in room.GameObjects)
                if (data.Rooms.SelectMany(r=>r.GameObjects).Count(i=>i.InstanceID==instance.InstanceID)!=1) throw new InvalidDataException("Duplicate annex instance ID.");
            passed.Add(name+"-native-house-layout-layers-unique-ids-marker-before-player");
        }
        foreach (var (name,target,tag) in new[] {
            ("o_eao_d01_entry","r_eao_d01_warehouse","EAO_D01_enter"), ("o_eao_d01_return","r_DockStore1floor","DockStore01_01"),
            ("o_eao_d01_archive_door","r_eao_d01_archive","EAO_D01_archive"), ("o_eao_d01_down","r_eao_d01_warehouse","EAO_D01_down") }) {
            var obj=data.GameObjects.Single(o=>o.Name.Content==name);
            var asm=Asm("gml_Object_"+name+"_Create_0");
            var index=data.Rooms.IndexOf(data.Rooms.Single(r=>r.Name.Content==target));
            if (!asm.Contains("event_inherited") || !asm.Contains(tag) || !System.Text.RegularExpressions.Regex.IsMatch(asm,@"push(?:i\.e|\.i) "+index+@"\s+pop\.v\.i self.target")) throw new InvalidDataException("Native door target/tag missing: "+name);
            if (obj.Events[(int)EventType.Mouse].Count!=0 || obj.Events[(int)EventType.Other].Count!=0 || (name=="o_eao_d01_return" ? obj.Events[(int)EventType.Alarm].Any(e=>e.EventSubtype!=7) : obj.Events[(int)EventType.Alarm].Count!=0)) throw new InvalidDataException("Custom transition lifecycle introduced.");
            passed.Add(name+"-native-transition-target-and-return-tag");
        }
        var clerk=Asm("gml_Object_o_eao_d01_clerk_Create_0"); EaoInteraction.ValidateStructReceiver(clerk);
        var objClerk=data.GameObjects.Single(o=>o.Name.Content=="o_eao_d01_clerk");
        if(objClerk.ParentId?.Name.Content!="o_simple_NPC") throw new InvalidDataException("Clerk bypasses native NPC.");
        var literals=data.Code.Single(c=>c.Name.Content=="gml_Object_o_eao_d01_clerk_Create_0").Instructions.Select(i=>i.Value).OfType<UndertaleResourceById<UndertaleString,UndertaleChunkSTRG>>().Select(s=>s.Resource.Content).ToArray();
        using var flow=JsonDocument.Parse(literals.Single(s=>s.StartsWith("{\"RootFragment\":\"eao_mq02\"")));
        using var lines=JsonDocument.Parse(literals.Single(s=>s.StartsWith("{\"EAO2_intro\":")));
        var fragments=flow.RootElement.GetProperty("Fragments"); var specs=flow.RootElement.GetProperty("Specs");
        foreach(var fragment in fragments.EnumerateObject()) {
            var edges=fragment.Value.ValueKind==JsonValueKind.Array?fragment.Value.EnumerateArray().Select(v=>v.GetString()!):new[]{fragment.Value.GetString()!};
            if(edges.Any(e=>e!="@dialogue_end"&&!fragments.TryGetProperty(e,out _))) throw new InvalidDataException("MQ02 dialogue has a broken edge.");
            if(!fragment.Name.StartsWith("instruction_")&&fragment.Name!="eao_mq02"&&!lines.RootElement.TryGetProperty(fragment.Name,out _)) throw new InvalidDataException("MQ02 dialogue localization missing.");
            if(fragment.Name.EndsWith("_pc")&&!specs.GetProperty(fragment.Name).GetProperty("technical").GetBoolean()) throw new InvalidDataException("MQ02 repeatable option missing.");
        }
        foreach(var action in new[]{"instruction_EAO2_accept","instruction_EAO2_submit","instruction_EAO2_recover"}) if(!specs.GetProperty(action).GetProperty("action").GetBoolean()) throw new InvalidDataException("MQ02 action can run during preview.");
        if(lines.RootElement.EnumerateObject().Any(l=>l.Value[1].GetString()!.Length>100)) throw new InvalidDataException("MQ02 document content leaked into dialogue.");
        passed.Add("mq02-native-clerk-dialogue-linked-localized-action-preview-safe");
        var entry=data.GameObjects.Single(o=>o.Name.Content=="o_eao_d01_entry");
        var draw=Asm("gml_Object_o_eao_d01_entry_Draw_0");
        var gate=Asm("gml_Object_o_eao_d01_entry_Step_0");
        var spawn=Asm("gml_Object_o_eao_controller_Other_14");
        if(!entry.Visible || !draw.Contains("draw_sprite_ext") || !draw.Contains("event_inherited") || !draw.Contains("封账仓入口") || !draw.Contains("draw_set_font") || !gate.Contains("-1100") || !gate.Contains("EAO_read_eao_copy")) throw new InvalidDataException("Customs entrance needs persistent door art, label, foreground depth and native prerequisite lock.");
        if(spawn.Contains("EAO_MQ01")||spawn.Contains("__dialogue_flow_data")||!spawn.Contains("instance_create_depth")) throw new InvalidDataException("Physical entrance incorrectly depends on courier/story state.");
        if(entry.Events[(int)EventType.Mouse].Count!=0 || entry.Events[(int)EventType.Alarm].Count!=0 || entry.Events[(int)EventType.Other].Count!=0) throw new InvalidDataException("Customs entrance replaced native click/approach/transition logic.");
        passed.Add("customs-entrance-persistent-visible-door-art-label-and-native-lock-interaction");
        return passed.ToArray();
    }
}
