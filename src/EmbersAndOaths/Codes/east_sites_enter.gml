// Record geographical origin only after a successful native door transition.
// The character map persists through saving inside a building and restarting.
var _changing = instance_exists(o_smoothRoomChanger);
event_inherited();
if (!_changing && instance_exists(o_smoothRoomChanger))
    ds_map_set(global.characterDataMap, "EAO_geo_sites_return", room_get_name(room));
