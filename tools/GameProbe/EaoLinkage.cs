using UndertaleModLib;
using System.IO;

internal static class EaoLinkage
{
    public static void Validate(UndertaleData data)
    {
        // Bare eao_* static calls caused the 0.1.1 runner crash. Native dialogue
        // callbacks are instance methods, linked by SCRP and invoked via callv.
        var invalid = data.Functions.Where(f => f.Name.Content.StartsWith("eao_", StringComparison.OrdinalIgnoreCase)).Select(f => f.Name.Content).ToArray();
        if (invalid.Length != 0)
            throw new InvalidDataException("EAO prototype has unresolved static function dependencies: " + string.Join(", ", invalid));
        var callbacks = data.Code.Where(c => c.ParentEntry != null && c.ParentEntry.Name.Content.Contains("o_eao_")).ToArray();
        var night = data.GameObjects.Any(o=>o.Name.Content=="o_eao_n1_mara");
        var nightParents=new[]{"mara","tor","ivo","rhea","rope","cots"}.Select(n=>"gml_Object_o_eao_n1_"+n+"_Create_0").ToArray();
        var n2 = data.GameObjects.Any(o=>o.Name.Content=="o_eao_n2_aina");
        var n2Parents=new[]{"aina","watcher","nara","coffin","winch"}.Select(n=>"gml_Object_o_eao_n2_"+n+"_Create_0").ToArray();
        var cs = data.GameObjects.Any(o=>o.Name.Content=="o_eao_cs_rena");
        var csParents=new[]{"cs_pelan","cs_maler","cs_rena","cs_lukan","svc_milo","cs_street"}.Select(n=>"gml_Object_o_eao_"+n+"_Create_0").ToArray();
        var fx = data.GameObjects.Any(o=>o.Name.Content=="o_eao_fx_keeper");
        var fxParents=new[]{"fx_keeper","fx_sign","fx_whiteline"}.Select(n=>"gml_Object_o_eao_"+n+"_Create_0").ToArray();
        var fxDigits=new[]{16,13,13};
        if (callbacks.Length != (night ? 87 : 9) + (n2 ? 30 : 0) + (cs ? 6 * 19 : 0) + (fx ? 16 + 2 * 13 : 0) || callbacks.Count(c => c.ParentEntry!.Name.Content == "gml_Object_o_eao_courier_Create_0") != 5 || callbacks.Count(c => c.ParentEntry!.Name.Content == "gml_Object_o_eao_d01_clerk_Create_0") != 4 || callbacks.Any(c => !c.Name.Content.StartsWith("gml_Script_anon_")) || (night && nightParents.Any(n=>callbacks.Count(c=>c.ParentEntry!.Name.Content==n)!=13)) || (n2 && n2Parents.Any(n=>callbacks.Count(c=>c.ParentEntry!.Name.Content==n)!=6)) || (cs && csParents.Any(n=>callbacks.Count(c=>c.ParentEntry!.Name.Content==n)!=19)) || (fx && fxParents.Select((n,i)=>(n,i)).Any(p=>callbacks.Count(c=>c.ParentEntry!.Name.Content==p.n)!=fxDigits[p.i])))
            throw new InvalidDataException("Unexpected EAO callback layout: " + callbacks.Length + " entries: " + string.Join(", ", callbacks.Select(c => c.Name.Content)));
        foreach (var callback in callbacks) {
            if (!data.Scripts.Any(s => s.Code == callback) || !data.Functions.Any(f => f.Name.Content == callback.Name.Content))
                throw new InvalidDataException("Native dialogue callback linkage missing: " + callback.Name.Content);
            if (data.Code.IndexOf(callback.ParentEntry!) >= data.Code.IndexOf(callback)) throw new InvalidDataException("Callback precedes its parent.");
        }
        foreach(var parent in callbacks.Select(c=>c.ParentEntry!).Distinct()) {
            var index=data.Code.IndexOf(parent); var children=callbacks.Where(c=>c.ParentEntry==parent).OrderBy(c=>c.Offset).ToArray();
            if(!data.Code.Skip(index+1).Take(children.Length).SequenceEqual(children)) throw new InvalidDataException("EAO parent and child CODE group is not contiguous.");
        }
    }
}
