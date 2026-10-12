// The physical entrance remains visible even before its paperwork is accepted.
// This needs only the native room/player state, not the courier's dialogue data.
if (room != r_DockStore1floor || !instance_exists(o_player) || instance_exists(o_smoothRoomChanger)) exit;
if (!variable_global_exists("characterDataMap") || !is_real(global.characterDataMap) || !ds_exists(global.characterDataMap, ds_type_map)) exit;
if (!instance_exists(o_eao_d01_entry)) instance_create_depth(351, 428, -1100, o_eao_d01_entry);
