using System.Buffers.Binary;
using System.IO;
using System.Text;
using System.Text.Json;
using ModShardLauncher;
using ModShardLauncher.Mods;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Util;

namespace EmbersAndOaths;

// Image composition is done from independent materials at build time. Runtime
// only draws cropped native-size chunks; collision and quest state stay native.
internal static class GroundChunks
{
    internal const string WorldObject = "o_eao_ground_world";
    private static readonly JsonDocument Document = JsonDocument.Parse(
        typeof(GroundChunks).Assembly.GetManifestResourceStream("EAO.Ground.Manifest.json")
        ?? throw new InvalidDataException("Missing embedded ground chunk manifest."));
    private static IEnumerable<JsonElement> Scenes => Document.RootElement.GetProperty("scenes").EnumerateArray();
    internal static string Sprite(string id) => "s_eao_ground_" + id;

    internal static void Prepare()
    {
        if (Document.RootElement.GetProperty("cell_size").GetInt32() != 26 ||
            Document.RootElement.GetProperty("chunk_cells").GetInt32() != 30 ||
            Document.RootElement.GetProperty("gutter").GetInt32() != 2)
            throw new InvalidDataException("Unsupported terrain stitching geometry.");
        foreach (var scene in Scenes) {
            var room = Msl.GetRoom(scene.GetProperty("room").GetString()!);
            var cells = scene.GetProperty("size_cells");
            if (room.Width != cells[0].GetInt32()*26 || room.Height != cells[1].GetInt32()*26)
                throw new InvalidDataException("Ground chunks disagree with native room: " + room.Name.Content);
            foreach (var chunk in scene.GetProperty("chunks").EnumerateArray()) Add(chunk);
        }
        var floor = Msl.AddObject(WorldObject, isVisible:true);
        floor.ParentId=null; floor.Sprite=null; floor.TextureMaskId=null;
        floor.Visible=true; floor.Persistent=false; floor.Solid=false;
    }

    private static void Add(JsonElement chunk)
    {
        var id=chunk.GetProperty("id").GetString()!;
        using var input=typeof(GroundChunks).Assembly.GetManifestResourceStream("EAO.Ground."+id+".png")
            ?? throw new InvalidDataException("Missing embedded ground image: "+id);
        using var stream=new MemoryStream(); input.CopyTo(stream); var png=stream.ToArray();
        const int size=784;
        if (BinaryPrimitives.ReadInt32BigEndian(png.AsSpan(16,4))!=size || BinaryPrimitives.ReadInt32BigEndian(png.AsSpan(20,4))!=size)
            throw new InvalidDataException("Ground chunk must retain its two-pixel gutter: "+id);
        var data=DataLoader.data;
        var sprite=data.Sprites.SingleOrDefault(s=>s.Name.Content==Sprite(id));
        if (sprite!=null && (sprite.Width!=size || sprite.Height!=size || sprite.OriginX!=0 || sprite.OriginY!=0))
            throw new InvalidDataException("Owned ground sprite geometry changed: "+id);
        var texture=sprite?.Textures.Single().Texture.TexturePage;
        if (texture==null) {
            texture=new UndertaleEmbeddedTexture{Name=data.Strings.MakeString("EAO_Ground_"+id)};
            data.EmbeddedTextures.Add(texture);
        }
        texture.TextureData.Image=GMImage.FromPng(png);
        if (sprite!=null) return;
        var item=Msl.CreateTexureItem(texture,new RectTexture(0,0,size,size),new RectTexture(0,0,size,size),new BoundingData<ushort>(size,size));
        data.TexturePageItems.Add(item);
        sprite=Msl.CreateSpriteNoCollisionMasks(Sprite(id),new MarginData(0,size-1,0,size-1),new OriginData(0,0),new BoundingData<uint>(size,size));
        sprite.Textures.Add(new UndertaleSprite.TextureEntry{Texture=item}); data.Sprites.Add(sprite);
    }

    internal static string Draw(string room)
    {
        var scene=Scenes.Single(s=>s.GetProperty("room").GetString()==room);
        var code=new StringBuilder("// EAO globally sampled 26px terrain; no panorama scaling.\n");
        foreach (var chunk in scene.GetProperty("chunks").EnumerateArray()) {
            var id=chunk.GetProperty("id").GetString()!;
            var x=chunk.GetProperty("x").GetInt32(); var y=chunk.GetProperty("y").GetInt32();
            var width=chunk.GetProperty("width").GetInt32(); var height=chunk.GetProperty("height").GetInt32();
            // Gutter is sampling context only. Crop it out so adjacent images
            // never double-blend alpha, nor draw beyond their authored cores.
            code.AppendLine($"draw_sprite_part({Sprite(id)},0,2,2,{width},{height},{x},{y});");
        }
        return code.ToString();
    }

    internal static void Configure(Action<UndertaleGameObject,string,EventType,uint> set)
    {
        var floor=Msl.GetObject(WorldObject);
        set(floor,"depth=1; scr_locationRoomEntityInitSavable(id,false);",EventType.Create,0);
        set(floor,"if (room != "+EastSites.Room+" || !("+Hd2dArt.Active+")) exit;\n"+Draw(EastSites.Room),EventType.Draw,0);
    }

    // User8 covers newly generated surfaces. Native loads of an already visited
    // location may skip that pass, so the owned persistent controller restores
    // this excluded decoration after a real player exists as well.
    internal static string EnsureWorld() => "if (room == "+EastSites.Room+" && instance_exists(o_player) && !instance_exists(o_smoothRoomChanger) && !instance_exists("+WorldObject+")) instance_create_depth(0,0,1,"+WorldObject+");\n";
}
