using System.Linq;
using ModShardLauncher;
using UndertaleModLib;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

// Native transition Create computes grid position from the sprite centre.
// The barn sprite's original y origin (32) differs from half its height (45),
// moving that computed interaction cell one row below our cell-centred doors.
// Copy only the resource metadata; native pixels, masks and objects stay intact.
internal static class SceneDoorAnchor
{
    internal const string Name = "s_eao_scene_door_anchor";
    internal static UndertaleSprite Ensure()
    {
        var data = DataLoader.data;
        var sprite = data.Sprites.SingleOrDefault(s => s.Name.Content == Name);
        if (sprite != null) return sprite;
        var source = Msl.GetObject("o_Doors_all_small").Sprite;
        sprite = NativeRooms.Copy(source);
        sprite.Name = data.Strings.MakeString(Name);
        sprite.OriginX = (int)source.Width / 2;
        sprite.OriginY = (int)source.Height / 2;
        foreach (var entry in source.Textures)
            sprite.Textures.Add(new UndertaleSprite.TextureEntry { Texture = entry.Texture });
        foreach (var mask in source.CollisionMasks) {
            var copy = sprite.NewMaskEntry();
            copy.Data = mask.Data.ToArray();
            sprite.CollisionMasks.Add(copy);
        }
        data.Sprites.Add(sprite);
        return sprite;
    }
}
