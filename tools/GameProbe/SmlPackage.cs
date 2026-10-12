using System;
using System.IO;
using System.Linq;
using System.Text;
using ModShardLauncher;
using ModShardLauncher.Mods;

internal static class SmlPackage
{
    public static void Pack(string assembly, string codes, string destination)
    {
        var output = ProjectPaths.Output(destination, "artifacts");
        var files = Directory.GetFiles(codes, "*.gml").OrderBy(p => p, StringComparer.Ordinal).ToArray();
        var chunks = files.Select(File.ReadAllBytes).ToArray();
        var icon = ModIcon.Render(Path.GetFullPath(Path.Combine(codes, "..", "Assets")));
        using (var stream = File.Create(output))
        using (var writer = new BinaryWriter(stream, Encoding.UTF8)) {
            writer.Write(Encoding.ASCII.GetBytes("MSLM"));
            writer.Write(Encoding.ASCII.GetBytes("v0.13.2.0"));
            writer.Write(1); // UI icon; MSL excludes this exact path from game sprite import.
            var iconName = Encoding.UTF8.GetBytes("EmbersAndOaths\\icon.png");
            writer.Write(iconName.Length); writer.Write(iconName); writer.Write(0); writer.Write(icon.Length);
            writer.Write(0); // scripts
            writer.Write(files.Length); // GML files
            int offset = icon.Length;
            for (int i = 0; i < files.Length; i++) {
                var name = Encoding.UTF8.GetBytes("EmbersAndOaths\\Codes\\" + Path.GetFileName(files[i]));
                writer.Write(name.Length); writer.Write(name); writer.Write(offset); writer.Write(chunks[i].Length);
                offset = checked(offset + chunks[i].Length);
            }
            writer.Write(0); // assembly text resources
            writer.Write(icon);
            foreach (var bytes in chunks) writer.Write(bytes);
            var dll = File.ReadAllBytes(assembly);
            writer.Write(dll.Length); writer.Write(dll);
        }
        // Verify with the actual installed MSL reader, not just our own serialization.
        var mod = FileReader.Read(output) ?? throw new InvalidDataException("MSL rejected the package.");
        if (!mod.Icon.SequenceEqual(icon)) throw new InvalidDataException("Packed icon missing or changed.");
        ModIcon.Verify(mod.Icon);
        foreach (var file in files)
            if (mod.GetCode(Path.GetFileName(file)) != File.ReadAllText(file)) throw new InvalidDataException("Packed GML mismatch.");
        var modType = mod.Assembly.GetTypes().Single(t => t.IsSubclassOf(typeof(Mod)));
        var instance = (Mod)Activator.CreateInstance(modType)!;
        Console.WriteLine($"MSL reader verified: {instance.Name}, {instance.Version}, {files.Length} GML resources, 128x128 PNG icon ({mod.Icon.Length} bytes), {mod.Version}.");
    }

    public static void Verify(string path)
    {
        var mod = FileReader.Read(path) ?? throw new InvalidDataException("MSL rejected the package.");
        ModIcon.Verify(mod.Icon);
        Console.WriteLine($"MSL reads {mod.Name}: 128x128 PNG icon, {mod.Icon.Length} bytes.");
    }
}
