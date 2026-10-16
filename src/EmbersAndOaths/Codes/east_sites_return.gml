event_inherited();
// Missing/unknown metadata means the original exterior, preserving old saves.
// The native position_tag still selects the corresponding shed/canal marker.
target = r_eao_n2_sites;
if (ds_map_exists(global.characterDataMap, "EAO_geo_sites_return") &&
    ds_map_find_value(global.characterDataMap, "EAO_geo_sites_return") == "r_eao_n2_world")
    target = r_eao_n2_world;
