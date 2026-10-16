using System.Reflection;
using System.IO;
using UndertaleModLib;
using UndertaleModLib.Decompiler;
using ModShardLauncher;
using ModShardLauncher.Mods;
using System.Security.Cryptography;
using System.Text.Json;

if (args.Length > 0 && args[0] == "--pack") {
    SmlPackage.Pack(args[1], args[2], args[3]);
    return;
}
if (args.Length > 0 && args[0] == "--verify-package") {
    SmlPackage.Verify(args[1]);
    return;
}
if (args.Length > 0 && args[0] == "--references") {
    foreach (var assembly in new[] { typeof(DataLoader).Assembly, typeof(UndertaleData).Assembly }) {
        Console.WriteLine(assembly.GetName());
        foreach (var reference in assembly.GetReferencedAssemblies().Where(a => !a.Name!.StartsWith("System") && !a.Name.StartsWith("Microsoft"))) Console.WriteLine(reference);
    }
    return;
}
if (args.Length > 0 && args[0] == "--settings-schema") {
    var settingsType = typeof(DataLoader).Assembly.GetTypes().Single(t => t.Name == "UserSettings");
    Console.WriteLine("Local MSL settings type: " + settingsType.FullName);
    foreach (var field in settingsType.GetFields(BindingFlags.Public | BindingFlags.Instance)) Console.WriteLine("FIELD " + field.Name);
    foreach (var property in settingsType.GetProperties(BindingFlags.Public | BindingFlags.Instance)) Console.WriteLine("PROPERTY " + property.Name);
    return;
}
if (args.Length > 0 && args[0] == "--test-paths") {
    var denied = new[] { @"D:\SteamLibrary\steamapps\common\Stoneshard\data.win", Path.Combine(ProjectPaths.Root(), "test-env", "baseline", "game", "data.win"), Path.Combine(ProjectPaths.Root(), "test-env", "work", "..", "..", "escape.win") };
    foreach (var path in denied) {
        bool refused = false;
        try { ProjectPaths.Output(path, "test-env/work"); } catch (InvalidOperationException) { refused = true; }
        if (!refused) throw new InvalidOperationException("Path guard allowed an unsafe output.");
    }
    ProjectPaths.Output(Path.Combine(ProjectPaths.Root(), "test-env", "work", "game", "data.win"), "test-env/work");
    Console.WriteLine("Path guard: formal installation, baseline and traversal refused; work output accepted.");
    return;
}

if(args.Length>0&&args[0]=="--image-api") {
    var type=typeof(UndertaleModLib.Util.GMImage);
    foreach(var p in type.GetProperties()) Console.WriteLine(p);
    foreach(var m in type.GetMethods(System.Reflection.BindingFlags.Public|System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.DeclaredOnly))Console.WriteLine(m.Name);
    return;
}
if (args.Length == 0) {
    foreach (var type in new[] {typeof(UndertaleIO), typeof(Decompiler), typeof(Msl), typeof(DataLoader)}) {
        Console.WriteLine("TYPE " + type.FullName);
        foreach (var m in type.GetMethods(BindingFlags.Public | BindingFlags.Static | BindingFlags.DeclaredOnly))
            Console.WriteLine(m);
    }
    return;
}
using var stream = File.OpenRead(args[0]);
var data = UndertaleIO.Read(stream);
Console.WriteLine($"Loaded: {data.Code.Count} code entries, {data.GameObjects.Count} objects, {data.Rooms.Count} rooms.");
if (args.Length > 1 && args[1] == "--sprite-shape") {
    foreach (var name in args.Skip(2)) {
        var sprite = data.Sprites.Single(s => s.Name.Content == name);
        var values = sprite.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance)
            .Where(p => p.CanRead && p.GetIndexParameters().Length == 0)
            .Select(p => (p.Name, Value:p.GetValue(sprite)))
            .Where(p => p.Value != null && (p.Value.GetType().IsPrimitive || p.Value.GetType().IsEnum))
            .ToDictionary(p => p.Name, p => p.Value);
        Console.WriteLine(JsonSerializer.Serialize(new { name, values, masks=sprite.CollisionMasks.Select(m => new { bytes=m.Data.Length, nonzeroBytes=m.Data.Count(b => b != 0) }) }));
    }
    return;
}
if (args.Length > 1 && args[1] == "--room-summary") {
    foreach (var name in args.Skip(2)) {
        var room = data.Rooms.Single(r => r.Name.Content == name);
        Console.WriteLine($"ROOM {name} {room.Width}x{room.Height} flags={room.Flags} creation={room.CreationCodeId?.Name.Content}");
        foreach (var layer in room.Layers) Console.WriteLine($"LAYER {layer.LayerId} {layer.LayerName.Content} {layer.LayerType} depth={layer.LayerDepth}");
        foreach (var obj in room.GameObjects) Console.WriteLine($"INSTANCE {obj.X},{obj.Y} {obj.ObjectDefinition?.Name.Content} create={obj.CreationCode?.Name.Content} pre={obj.PreCreateCode?.Name.Content}");
    }
    return;
}
if (args.Length > 1 && args[1] == "--eao-layout-preview") {
    var layouts = data.Rooms.Where(r=>r.Name.Content.StartsWith("r_eao_d01_")).Select(room=>new {
        name=room.Caption.Content, resource=room.Name.Content, width=room.Width, height=room.Height,
        objects=room.GameObjects.Where(i=>i.X>=0 && i.Y>=0 && i.ObjectDefinition.Sprite!=null && !i.ObjectDefinition.Name.Content.Contains("wall") && !i.ObjectDefinition.Name.Content.Contains("Barrier") && i.ObjectDefinition.Name.Content!="o_abstract_player").Select(i=> {
            var sprite=i.ObjectDefinition.Sprite; var frame=sprite.Textures[(int)Math.Clamp(i.ImageIndex,0,sprite.Textures.Count-1)].Texture;
            return new { name=i.ObjectDefinition.Name.Content, sprite=sprite.Name.Content, x=i.X, y=i.Y, originX=sprite.OriginX, originY=sprite.OriginY, page=data.EmbeddedTextures.IndexOf(frame.TexturePage), sx=frame.SourceX, sy=frame.SourceY, sw=frame.SourceWidth, sh=frame.SourceHeight, tx=frame.TargetX, ty=frame.TargetY, tw=frame.TargetWidth, th=frame.TargetHeight, mark=i.ObjectDefinition.Name.Content.Contains("eao_"), bg=i.ObjectDefinition.Name.Content.Contains("bg",StringComparison.OrdinalIgnoreCase)||i.ObjectDefinition.Name.Content.Contains("parts",StringComparison.OrdinalIgnoreCase) };
        }).OrderByDescending(i=>i.bg).ThenBy(i=>i.y).ToArray()
    }).ToArray();
    var html="<!doctype html><html lang='zh'><meta charset='utf-8'><title>外港封账仓布局预览</title><style>body{background:#18151f;color:#eee;font:16px sans-serif;margin:24px}button{padding:8px;margin:6px;background:#514065;color:white;border:0}canvas{background:#14121a;width:min(100%,1024px);image-rendering:pixelated;border:1px solid #6a547e}p{max-width:950px}</style><h1>外港封账仓 · 原素材布局预览</h1><p>显示候选包中的实际房间对象坐标，使用 stoneshard-assets-sample 原图集。黄色标记为新增人物、文书与出入口。光照、动画、碰撞及动态生成需游戏内验收。</p><nav id='tabs'></nav><h2 id='title'></h2><canvas id='map'></canvas><script>const layouts="+JsonSerializer.Serialize(layouts)+";const cache={};const canvas=document.getElementById('map'),ctx=canvas.getContext('2d');async function page(n){if(!cache[n]){cache[n]=new Promise((ok,fail)=>{let img=new Image();img.onload=()=>ok(img);img.onerror=fail;img.src='../stoneshard-assets-sample/atlas-'+String(n).padStart(3,'0')+'.png'});}return cache[n];}let revision=0;async function draw(index){const current=++revision,l=layouts[index];document.getElementById('title').textContent=l.name+' ('+l.resource+')';canvas.width=l.width;canvas.height=l.height;ctx.imageSmoothingEnabled=false;await Promise.all(l.objects.map(o=>page(o.page)));if(current!==revision)return;for(const o of l.objects){let img=await page(o.page);ctx.drawImage(img,o.sx,o.sy,o.sw,o.sh,o.x-o.originX+o.tx,o.y-o.originY+o.ty,o.tw,o.th);}for(const o of l.objects.filter(o=>o.mark)){ctx.strokeStyle='#ffd67a';ctx.lineWidth=2;ctx.strokeRect(o.x-10,o.y-18,26,26);ctx.fillStyle='#ffd67a';ctx.font='12px sans-serif';ctx.fillText(o.name.replace('o_eao_d01_','').replace('o_loot_eao_',''),o.x+18,o.y);}}layouts.forEach((l,i)=>{let b=document.createElement('button');b.textContent=l.name;b.onclick=()=>draw(i);document.getElementById('tabs').append(b)});draw(0);</script></html>";
    var path=ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","warehouse-layout.html"),"artifacts");File.WriteAllText(path,html);Console.WriteLine(path);return;
}
if (args.Length > 1 && args[1] == "--asset-summary") {
    foreach (var pattern in args.Skip(2)) {
        foreach (var sprite in data.Sprites.Where(s => s.Name.Content.Contains(pattern, StringComparison.OrdinalIgnoreCase)))
            Console.WriteLine($"SPRITE {data.Sprites.IndexOf(sprite)} {sprite.Name.Content} {sprite.Width}x{sprite.Height} origin={sprite.OriginX},{sprite.OriginY} frames={sprite.Textures.Count}");
        foreach (var obj in data.GameObjects.Where(o => o.Name.Content.Contains(pattern, StringComparison.OrdinalIgnoreCase)))
            Console.WriteLine($"OBJECT {data.GameObjects.IndexOf(obj)} {obj.Name.Content} sprite={obj.Sprite?.Name.Content} parent={obj.ParentId?.Name.Content} events=" + string.Join(",", obj.Events.SelectMany(es => es).SelectMany(e => e.Actions).Select(a => a.CodeId?.Name.Content)));
    }
    return;
}
if (args.Length > 1 && args[1] == "--calls") {
    foreach (var pattern in args.Skip(2))
        foreach (var code in data.Code.Where(c => c.ParentEntry == null && c.Instructions.Any(i => i.Function?.Target?.Name.Content.Contains(pattern, StringComparison.OrdinalIgnoreCase) == true)))
            Console.WriteLine("CALLER " + pattern + " " + code.Name.Content);
    return;
}
if (args.Length > 1 && args[1] == "--catalog") {
    foreach (var pattern in args.Skip(2)) {
        if (int.TryParse(pattern, out var index)) Console.WriteLine("OBJECT " + index + " " + data.GameObjects[index].Name.Content);
        else foreach (var code in data.Code.Where(c => c.Name.Content.Contains(pattern, StringComparison.OrdinalIgnoreCase))) Console.WriteLine($"CODE {code.Name.Content} PARENT {code.ParentEntry?.Name.Content} OFFSET {code.Offset} LENGTH {code.Length}");
    }
    return;
}
if (args.Length > 1 && args[1] == "--function-asm") {
    foreach (var name in args.Skip(2)) {
        var code = data.Code.Single(c => c.Name.Content == name);
        Console.WriteLine("CODE " + name + " PARENT " + code.ParentEntry?.Name.Content);
        foreach (var property in code.GetType().GetProperties().Where(p => p.Name.Contains("Offset") || p.Name.Contains("Length") || p.Name.Contains("Argument"))) Console.WriteLine(property.Name + "=" + property.GetValue(code));
        var parent = code.ParentEntry ?? code;
        var asm = parent.Disassemble(data.Variables, data.CodeLocals.For(parent));
        if (code.ParentEntry != null) {
            var start = asm.IndexOf("> " + name + " ", StringComparison.Ordinal);
            if (start < 0) throw new InvalidDataException("Function marker missing: " + name);
            var sibling = data.Code.Where(c => c.ParentEntry == parent && c.Offset > code.Offset && c.Name.Content.StartsWith("gml_Script_") && !c.Name.Content.StartsWith("gml_Script_anon_") && !c.Name.Content.StartsWith("gml_Script____struct_")).OrderBy(c => c.Offset).FirstOrDefault();
            var end = sibling == null ? -1 : asm.IndexOf("\n> " + sibling.Name.Content + " ", start + 2, StringComparison.Ordinal);
            asm = end < 0 ? asm[start..] : asm[start..end];
        }
        Console.WriteLine(string.Join("\n", asm.Split('\n').Select(line => line.Length > 1500 ? line[..200] + " [large literal omitted]" : line)));
    }
    return;
}
if (args.Length > 1 && args[1] == "--font-metrics") {
    foreach (var font in data.Fonts) Console.WriteLine("FONT " + font.Name.Content + " " + string.Join(" ", font.GetType().GetProperties().Where(p => p.Name.Contains("Size") || p.Name.Contains("Scale")).Select(p => p.Name + "=" + p.GetValue(font))));
    return;
}
if (args.Length > 1 && args[1] == "--names") {
    foreach (var pattern in args.Skip(2)) {
        foreach (var code in data.Code.Where(c => c.ParentEntry == null && c.Name.Content.Contains(pattern, StringComparison.OrdinalIgnoreCase))) Console.WriteLine("CODE " + code.Name.Content);
        foreach (var obj in data.GameObjects.Where(o => o.Name.Content.Contains(pattern, StringComparison.OrdinalIgnoreCase))) Console.WriteLine("OBJECT " + obj.Name.Content + " PARENT " + obj.ParentId?.Name.Content);
    }
    return;
}
if (args.Length > 1 && args[1] == "--assert-eao-linkage") {
    EaoLinkage.Validate(data);
    EaoInteraction.Validate(data);
    Console.WriteLine("EAO prototype function linkage check passed.");
    return;
}
if (args.Length > 1 && args[1] == "--assert-eao-struct-access") {
    var entry = data.Code.Single(c => c.Name.Content == "gml_Object_o_eao_courier_Create_0");
    EaoInteraction.ValidateStructReceiver(entry.Disassemble(data.Variables, data.CodeLocals.For(entry)));
    Console.WriteLine("EAO struct receiver check passed.");
    return;
}
if (args.Length > 1 && args[1] == "--test-eao-actions") {
    var scenarios = EaoActionChecks.Validate(data);
    var report = new { date=DateTimeOffset.Now, compiledCallbackScenarios=scenarios, nativeInventoryCalls="test doubles; no GameMaker GUI/runtime execution", inputSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[0]))), runtimeVerified=false };
    File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(), "artifacts", "document-action-validation.json"), "artifacts"), JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented=true }));
    Console.WriteLine(JsonSerializer.Serialize(report));
    return;
}
if (args.Length > 1 && args[1] == "--test-eao-rooms") {
    var checks=EaoRooms.Validate(data);
    var report=new { date=DateTimeOffset.Now, checks, inputSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[0]))), runtimeVerified=false };
    File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","room-validation.json"),"artifacts"),JsonSerializer.Serialize(report,new JsonSerializerOptions { WriteIndented=true }));
    Console.WriteLine(JsonSerializer.Serialize(report)); return;
}
if (args.Length > 1 && args[1] == "--test-eao-teleport") {
    var checks=EaoTestTeleport.Validate(data);
    var report=new { date=DateTimeOffset.Now, checks, inputSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[0]))), runtimeVerified=false };
    File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","test-teleport-validation.json"),"artifacts"),JsonSerializer.Serialize(report,new JsonSerializerOptions { WriteIndented=true }));
    Console.WriteLine(JsonSerializer.Serialize(report)); return;
}
if (args.Length > 1 && args[1] == "--test-eao-dev") {
    var checks=EaoDevChecks.Validate(data);
    var report=new {date=DateTimeOffset.Now,checks,inputSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[0]))),runtimeVerified=false};
    File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","dev-validation.json"),"artifacts"),JsonSerializer.Serialize(report,new JsonSerializerOptions{WriteIndented=true}));
    Console.WriteLine(JsonSerializer.Serialize(report));return;
}
if (args.Length > 1 && args[1] == "--test-eao-story") {
    var checks=EaoStory.Validate(data);
    var report=new {date=DateTimeOffset.Now,checks,inputSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[0]))),runtimeVerified=false};
    File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(),"artifacts","story-validation.json"),"artifacts"),JsonSerializer.Serialize(report,new JsonSerializerOptions{WriteIndented=true}));
    EaoStory.Preview(data); Console.WriteLine(JsonSerializer.Serialize(report));return;
}
if (args.Length > 1 && args[1] == "--compare-combination") {
    using var baselineStream = File.OpenRead(args[2]);
    var baseline = UndertaleIO.Read(baselineStream);
    if (baseline.GameObjects.Any(o => o.Name.Content.StartsWith("o_eao_"))) throw new InvalidDataException("Baseline already contains EAO.");
    var currentCodes = data.Code.ToDictionary(c => c.Name.Content);
    var baselineCodeNames = baseline.Code.Select(c => c.Name.Content).ToHashSet();
    var baselineObjectNames = baseline.GameObjects.Select(o => o.Name.Content).ToHashSet();
    var currentObjectNames = data.GameObjects.Select(o => o.Name.Content).ToHashSet();
    int checkedCodes = 0;
    foreach (var code in baseline.Code) {
        if (code.Name.Content == "gml_Object_o_gameLoader_Create_0") continue;
        if (!currentCodes.TryGetValue(code.Name.Content, out var existing) || code.Disassemble(baseline.Variables, baseline.CodeLocals.For(code)) != existing.Disassemble(data.Variables, data.CodeLocals.For(existing)))
            throw new InvalidDataException("Combination code differs: " + code.Name.Content);
        checkedCodes++;
    }
    var addedCode = data.Code.Where(c => !baselineCodeNames.Contains(c.Name.Content)).Select(c => c.Name.Content).ToArray();
    if (addedCode.Any(name => !name.Contains("o_eao_") && !name.Contains("o_inv_eao_") && !name.Contains("o_loot_eao_"))) throw new InvalidDataException("Unexpected non-EAO code addition.");
    var newObjects = data.GameObjects.Where(o => !baselineObjectNames.Contains(o.Name.Content)).Select(o => o.Name.Content).ToArray();
    if (newObjects.Any(name => !name.StartsWith("o_eao_") && !name.StartsWith("o_inv_eao_") && !name.StartsWith("o_loot_eao_")) || baselineObjectNames.Any(name => !currentObjectNames.Contains(name))) throw new InvalidDataException("Original object set differs.");
    if (data.Rooms.Count != baseline.Rooms.Count || data.Sprites.Count != baseline.Sprites.Count || data.Sounds.Count != baseline.Sounds.Count || data.GeneralInfo.Name.Content != baseline.GeneralInfo.Name.Content) throw new InvalidDataException("Original resource counts/identity differ.");
    var report = new { currentSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[0]))), baselineSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[2]))), baseline=Path.GetFullPath(args[2]), originalCombinationCodePreserved=true, checkedCodes, addedCode, newObjects, runtimeVerified=false };
    File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(), "artifacts", "repair-combination-validation.json"), "artifacts"), JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented=true }));
    Console.WriteLine(JsonSerializer.Serialize(report));
    return;
}
if (args.Length > 1 && args[1] == "--eao-linkage") {
    foreach (var function in data.Functions.Where(f => f.Name.Content.Contains("eao", StringComparison.OrdinalIgnoreCase))) Console.WriteLine("FUNCTION " + function.Name.Content);
    foreach (var script in data.Scripts.Where(s => s.Name.Content.Contains("eao", StringComparison.OrdinalIgnoreCase) || s.Name.Content == "scr_quest_get_complete")) Console.WriteLine("SCRIPT " + script.Name.Content + " => " + script.Code?.Name.Content);
    foreach (var code in data.Code.Where(c => c.Name.Content.Contains("eao", StringComparison.OrdinalIgnoreCase))) {
        Console.WriteLine("CODE " + code.Name.Content + " PARENT " + code.ParentEntry?.Name.Content);
        if (code.ParentEntry == null) foreach (var line in code.Disassemble(data.Variables, data.CodeLocals.For(code)).Split('\n').Where(l => l.Contains("eao") || l.Contains("call") || l.Contains("pushref"))) Console.WriteLine(line);
    }
    return;
}
if (args.Length > 1 && args[1] == "--require-msl-clean") {
    var markers = new[] { "o_msl_timer", "o_msl_log", "o_eao_controller" };
    if (data.GameObjects.Any(o => markers.Contains(o.Name.Content)))
        throw new InvalidDataException("MSL packaging input is already patched. Reload the original vanilla.win, not data.win; keep existing Mods selected for the rebuild.");
    Console.WriteLine("MSL input precheck passed: no known MSL/EAO object markers. This is not an independent vanilla provenance check.");
    return;
}
if (args.Length > 1 && args[1] == "--check-msl-log") {
    DataLoader.data = data;
    bool alreadyPatched = data.GameObjects.Any(o => o.Name.Content == "o_msl_timer");
    try {
        LogUtils.InjectLog();
        if (alreadyPatched) throw new InvalidDataException("Unexpected success on already patched input.");
        Console.WriteLine("Local MSL logging injection succeeded on the clean input.");
    } catch (ArgumentException error) when (alreadyPatched && error.Message.Contains("o_msl_timer") && error.Message.Contains("Create_0")) {
        Console.WriteLine("Reproduced before calling any Mod: " + error.Message);
    }
    return;
}
if (args.Length > 1 && args[1] == "--roundtrip") {
    using var output = File.Create(ProjectPaths.Output(args[2], "test-env/work"));
    UndertaleIO.Write(output, data);
    Console.WriteLine("Unmodified roundtrip written.");
    return;
}
if (args.Length > 1 && (args[1] == "--patch" || args[1] == "--repair-eao")) {
    bool repair = args[1] == "--repair-eao";
    var allowedOutput = args.Contains("--direct") ? "artifacts" : "test-env/work";
    var output = ProjectPaths.Output(args[3], allowedOutput);
    if (string.Equals(Path.GetFullPath(args[0]), output, StringComparison.OrdinalIgnoreCase)) throw new InvalidOperationException("Input and output must differ.");
    var package = FileReader.Read(args[2]) ?? throw new InvalidDataException("Invalid SML.");
    var type = package.Assembly.GetTypes().Single(t => t.IsSubclassOf(typeof(Mod)));
    var mod = (Mod)Activator.CreateInstance(type)!;
    mod.ModFiles = package;
    DataLoader.data = data;
    var originalIdentity = new[] { data.GeneralInfo.Name.Content, data.GeneralInfo.FileName.Content, data.GeneralInfo.DisplayName.Content };
    var originalCode = data.Code.ToDictionary(c => c.Name.Content, c => c.Disassemble(data.Variables, data.CodeLocals.For(c)));
    var originalRooms = data.Rooms.Where(r=>!r.Name.Content.StartsWith("r_eao_")).ToDictionary(r=>r.Name.Content,EaoRooms.Fingerprint);
    var repairCodeNames = new HashSet<string>();
    if (repair) {
        var events = new Dictionary<string, string> {
            ["gml_Object_o_eao_controller_Create_0"] = "controller_create.gml",
            ["gml_Object_o_eao_controller_Step_1"] = "controller_step.gml",
            ["gml_Object_o_eao_controller_Draw_64"] = "controller_draw_gui.gml"
        };
        foreach (var name in events.Keys) if (!originalCode.ContainsKey(name)) throw new InvalidDataException("Missing EAO repair target: " + name);
        var children = data.Code.Where(c => c.ParentEntry != null && c.ParentEntry.Name.Content.StartsWith("gml_Object_o_eao_")).ToArray();
        int helperCount = data.Functions.Count(f => f.Name.Content.StartsWith("eao_"));
        var recognizedNight = (children.Length == 87 || children.Length == 117 || (children.Length == 273 && data.GameObjects.Any(o=>o.Name.Content=="o_eao_cs_rena") && data.GameObjects.Any(o=>o.Name.Content=="o_eao_fx_keeper"))) && helperCount == 0 && data.GameObjects.Any(o=>o.Name.Content=="o_eao_n1_mara");
        if (recognizedNight) EaoLinkage.Validate(data);
        if (!recognizedNight && !((children.Length == 7 && helperCount == 7) || (children.Length == 0 && helperCount == 0) || ((children.Length == 4 || children.Length == 5) && helperCount == 0 && children.All(c => c.ParentEntry!.Name.Content == "gml_Object_o_eao_courier_Create_0")) || (children.Length == 9 && helperCount == 0 && children.All(c => c.ParentEntry!.Name.Content is "gml_Object_o_eao_courier_Create_0" or "gml_Object_o_eao_d01_clerk_Create_0")) || (children.Length == 15 && helperCount == 0 && children.All(c => c.ParentEntry!.Name.Content is "gml_Object_o_eao_courier_Create_0" or "gml_Object_o_eao_d01_clerk_Create_0" or "gml_Object_o_eao_test_guide_Create_0")))) throw new InvalidDataException("Input is not a recognized EAO prototype layout.");
        repairCodeNames.UnionWith(originalCode.Keys.Where(name => name.StartsWith("gml_Object_o_eao_") || name.StartsWith("gml_Object_o_inv_eao_") || name.StartsWith("gml_Object_o_loot_eao_")));
        repairCodeNames.UnionWith(children.Select(c => c.Name.Content));
        // Only these newly introduced EAO bridge events may be updated on native objects.
        foreach(var hook in new[]{"gml_Object_o_globalmapInteractiveNormal_Other_20", "gml_Object_o_smoothRoomChanger_Other_20"}) {
            if(originalCode.TryGetValue(hook,out var code)) {
                if(!code.Contains("EAO_test_map_")) throw new InvalidDataException("Native User 10 collision: "+hook);
                repairCodeNames.Add(hook);
            }
        }
        // Remove only the old EAO anonymous method resources. Original Mod code
        // and the loader event stay byte-for-byte unchanged in this repair.
        foreach (var script in data.Scripts.Where(s => children.Contains(s.Code)).ToArray()) data.Scripts.Remove(script);
        foreach (var child in children) {
            child.ParentEntry!.ChildEntries.Remove(child);
            var locals = data.CodeLocals.For(child);
            if (locals != null) data.CodeLocals.Remove(locals);
            data.Code.Remove(child);
        }
        foreach (var function in data.Functions.Where(f => f.Name.Content.StartsWith("eao_") || children.Any(c => c.Name.Content == f.Name.Content)).ToArray()) data.Functions.Remove(function);
        var update = mod.GetType().GetMethod("UpdatePrototype") ?? throw new InvalidDataException("Package does not support the current prototype update.");
        update.Invoke(mod, null);
    } else mod.PatchMod();
    EaoLinkage.Validate(data);
    EaoInteraction.Validate(data);
    EaoRooms.Validate(data);
    EaoStory.Validate(data);
    // GEO-02 east pilot: the only sanctioned native room change is widening r_GlobalMap's editor layers 119 -> 127 cells.
    foreach(var room in data.Rooms.Where(r=>originalRooms.ContainsKey(r.Name.Content))) {
        if(room.Name.Content=="r_GlobalMap" && room.Width==127*52 && room.Layers.Where(l=>l.TilesData!=null).All(l=>l.TilesData.TilesX==127)) continue;
        if(EaoRooms.Fingerprint(room)!=originalRooms[room.Name.Content]) throw new InvalidDataException("Original room changed: "+room.Name.Content);
    }
    var patchedCode = data.Code.ToDictionary(c => c.Name.Content);
    foreach (var pair in originalCode) {
        if (repair ? repairCodeNames.Contains(pair.Key) : pair.Key == "gml_Object_o_gameLoader_Create_0") continue;
        var entry = patchedCode[pair.Key];
        if (pair.Key.EndsWith("scr_globalmapCacheInit") && entry.Disassemble(data.Variables, data.CodeLocals.For(entry)).Contains("EAO_east_grid")) continue; // GEO-02 east pilot hook
        if (entry.Disassemble(data.Variables, data.CodeLocals.For(entry)) != pair.Value) throw new InvalidDataException("Unexpected original code change: " + pair.Key);
    }
    var temporary = ProjectPaths.Output(output + ".building", allowedOutput);
    using (var result = File.Create(temporary)) UndertaleIO.Write(result, data);
    using (var verify = File.OpenRead(temporary)) {
        var readback = UndertaleIO.Read(verify);
        EaoLinkage.Validate(readback);
        EaoInteraction.Validate(readback);
        EaoRooms.Validate(readback);
        EaoStory.Validate(readback);
        foreach(var room in readback.Rooms.Where(r=>originalRooms.ContainsKey(r.Name.Content))) {
            if(room.Name.Content=="r_GlobalMap" && room.Width==127*52 && room.Layers.Where(l=>l.TilesData!=null).All(l=>l.TilesData.TilesX==127 && l.TilesData.TileData.All(row=>row.Length==127))) continue;
            if(EaoRooms.Fingerprint(room)!=originalRooms[room.Name.Content]) throw new InvalidDataException("Original room changed after serialization: "+room.Name.Content);
        }
        if (repair) {
            var savedCode = readback.Code.ToDictionary(c => c.Name.Content);
            foreach (var pair in originalCode.Where(p => !repairCodeNames.Contains(p.Key))) {
                var entry = savedCode[pair.Key];
                if (entry.Disassemble(readback.Variables, readback.CodeLocals.For(entry)) != pair.Value) throw new InvalidDataException("Original code changed after repair serialization: " + pair.Key);
            }
        }
        var savedIdentity = new[] { readback.GeneralInfo.Name.Content, readback.GeneralInfo.FileName.Content, readback.GeneralInfo.DisplayName.Content };
        if (!savedIdentity.SequenceEqual(originalIdentity)) throw new InvalidDataException("Original game/save identity changed.");
        foreach (var name in new[] { "o_eao_controller", "o_eao_courier" })
            if (!readback.GameObjects.Any(o => o.Name.Content == name)) throw new InvalidDataException("Object missing after serialization: " + name);
        var ctx = new GlobalDecompileContext(readback, false);
        var boot = Decompiler.Decompile(readback.Code.First(c => c.Name.Content == "gml_Object_o_gameLoader_Create_0"), ctx);
        foreach (var initialization in new[] { "scr_slotsInit()", "scr_settingsInit()" }) {
            var initializationIndex = boot.IndexOf(initialization, StringComparison.Ordinal);
            if (initializationIndex < 0) throw new InvalidDataException("Original initialization missing: " + initialization);
        }
        if (!boot.Contains("o_eao_controller")) throw new InvalidDataException("Controller creation missing.");
    }
    File.Move(temporary, output, true);
    bool duplicateRefused = false;
    try { mod.PatchMod(); } catch (InvalidOperationException) { duplicateRefused = true; }
    if (!duplicateRefused) throw new InvalidDataException("Duplicate patch was not rejected.");
    var report = new { stage=repair ? "current combination - targeted EAO prototype update" : "current installation development - offline patch", runtimeVerified=false, modVersion=mod.Version, mouseDialogueWired=true, nativeNpcInherited=true, nativeDialogueFlowRegistered=true, customInputLocksRemoved=true, targetedRepair=repair, originalCodeUnchangedExceptEao=repair, eaoFunctionLinkageChecked=true, originalCodeEntries=originalCode.Count, originalCodeUnchangedExceptBoot=!repair, saveIdentity=originalIdentity[0], originalIdentityPreserved=true, duplicatePatchRefused=true, inputSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[0]))), packageSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(args[2]))), outputSha256=Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(output))) };
    File.WriteAllText(ProjectPaths.Output(Path.Combine(ProjectPaths.Root(), "artifacts", "offline-validation.json"), "artifacts"), JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented=true }));
    Console.WriteLine(JsonSerializer.Serialize(report));
    return;
}
if (args.Contains("--inventory")) {
    foreach (var property in data.GeneralInfo.GetType().GetProperties()) {
        if (property.Name.Contains("Name") || property.Name.Contains("ID")) Console.WriteLine($"INFO {property.Name} = {property.GetValue(data.GeneralInfo)}");
    }
    foreach (var item in data.Functions.Where(f => f.Name.Content.Contains("steam", StringComparison.OrdinalIgnoreCase))) Console.WriteLine("FUNCTION " + item.Name.Content);
    foreach (var code in data.Code.Where(c => c.ParentEntry == null && c.Instructions.Any(i => i.Value is UndertaleModLib.UndertaleResourceById<UndertaleModLib.Models.UndertaleString,UndertaleModLib.UndertaleChunkSTRG> str && (str.Resource.Content.Contains("GuinnelAnswers") || str.Resource.Content.Contains("working_directory") || str.Resource.Content == "StoneShard")))) Console.WriteLine("REF " + code.Name.Content);
    return;
}
var context = new GlobalDecompileContext(data, false);
foreach (var pattern in args.Skip(1)) {
    foreach (var code in data.Code.Where(c => c.ParentEntry == null && c.Name.Content.Contains(pattern, StringComparison.OrdinalIgnoreCase))) {
        Console.WriteLine("\nCODE " + code.Name.Content);
        try { Console.WriteLine(Decompiler.Decompile(code, context)); }
        catch (Exception ex) { Console.WriteLine("DECOMPILE ERROR " + ex.Message); }
    }
}

