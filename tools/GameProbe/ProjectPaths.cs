using System;
using System.IO;

internal static class ProjectPaths
{
    public static string Root()
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir != null) {
            if (File.Exists(Path.Combine(dir.FullName, "AGENTS.md")) && Directory.Exists(Path.Combine(dir.FullName, "design")) && Directory.Exists(Path.Combine(dir.FullName, "research"))) return dir.FullName;
            dir = dir.Parent;
        }
        throw new InvalidOperationException("Cannot locate project root.");
    }

    public static string Output(string path, string allowedDirectory)
    {
        var allowed = Path.GetFullPath(Path.Combine(Root(), allowedDirectory));
        var full = Path.GetFullPath(path);
        if (!full.StartsWith(allowed + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("Output must be inside " + allowed);
        for (var dir = new DirectoryInfo(Path.GetDirectoryName(full)!); dir != null; dir = dir.Parent)
            if (dir.Exists && (dir.Attributes & FileAttributes.ReparsePoint) != 0)
                throw new InvalidOperationException("Output ancestor is a reparse point: " + dir.FullName);
        if (File.Exists(full) && (File.GetAttributes(full) & FileAttributes.ReparsePoint) != 0)
            throw new InvalidOperationException("Output file is a reparse point.");
        Directory.CreateDirectory(Path.GetDirectoryName(full)!);
        return full;
    }
}
