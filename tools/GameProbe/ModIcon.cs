using System.IO;
using System.Windows.Markup;
using System.Windows.Media;
using System.Windows.Media.Imaging;

internal static class ModIcon
{
    public static byte[] Render(string assets)
    {
        byte[]? result = null;
        Exception? failure = null;
        var worker = new Thread(() => {
            try {
                var drawing = (DrawingGroup)XamlReader.Parse(File.ReadAllText(Path.Combine(assets, "icon.xaml")));
                var visual = new DrawingVisual();
                using (var context = visual.RenderOpen()) context.DrawDrawing(drawing);
                var bitmap = new RenderTargetBitmap(128, 128, 96, 96, PixelFormats.Pbgra32);
                bitmap.Render(visual);
                var encoder = new PngBitmapEncoder();
                encoder.Frames.Add(BitmapFrame.Create(bitmap));
                using var stream = new MemoryStream();
                encoder.Save(stream);
                result = stream.ToArray();
            } catch (Exception error) { failure = error; }
        });
        worker.SetApartmentState(ApartmentState.STA);
        worker.Start();
        worker.Join();
        if (failure != null) throw new InvalidDataException("Icon rendering failed.", failure);
        File.WriteAllBytes(ProjectPaths.Output(Path.Combine(assets, "icon.png"), "src/EmbersAndOaths/Assets"), result!);
        return result!;
    }

    public static void Verify(byte[] bytes)
    {
        using var stream = new MemoryStream(bytes);
        var image = BitmapFrame.Create(stream, BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.OnLoad);
        if (image.PixelWidth != 128 || image.PixelHeight != 128) throw new InvalidDataException("Unexpected icon dimensions.");
    }
}
