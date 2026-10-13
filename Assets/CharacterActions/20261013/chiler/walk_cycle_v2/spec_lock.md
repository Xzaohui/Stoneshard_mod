# Chiler idle concept keyframe lock

Stable ID: ALD-NPC-CHILER. Role: old-wall storyteller / guide. No supported combat ability. His wooden pointer is not a weapon.
Source: expressive/chiler/chiler_raw_imagegen.png. Approved scope: independent concept review, not user-approved animation.
Style: current STYLE_DIRECTION.md; preserve mature distinctive face, messy brown hair, moustache and goatee, ochre shoulder cape, gray-green tunic, brown trousers/boots, crossbody bag.
Canvas: 1536 x 1536 transparent RGBA concept display canvas, NOT native game resolution. Foot anchor: (768,1380) working registration marker, not engine origin. Source is translated (109,176); no resize. Faint source alpha under 16 removed; raw preserved.
Single fixed three-quarter facing screen-right, same source hand on screen-left (anatomical side unverified) holds downward pointer. No mirroring, switching hands, weaponization, outfit/equipment change.
First sequence: I0 still; I1 tiny inhale (shoulders and chest lift only, slight cloak response, head and feet remain stable); I2 return is exact reuse of I0, explicitly mapped.
Palette: derive from source (brown/ochre/gray-green/skin), no global forced count. Do not quantize to mask shape drift.
Engine origin, native timing, collision, actual direction mapping unknown. runtime_verified=false; equipment compatibility not tested.

Walk-cycle override: See SEQUENCE_PLAN.md. Six alternating gait key poses, no mirroring. Identity upper region reused exactly. Source anatomical handedness unknown, preserve image-side hand. Native parameters remain unknown. Current stage K0-K2 half-step before expanding.
