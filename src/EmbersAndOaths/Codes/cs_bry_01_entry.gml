// evt_CS_BRY_01_entry · engine event 50576 · on_first_interaction · once
// Registry: reads encountered_CS_BRY_01, writes encountered_CS_BRY_01 (encounter, false/true).
// Pilot batch CS-BRY-01 (MGMT-PILOT-BRY01-S156): the case opens on the first
// talk about the moved lease plate.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_entry", 50576);
eao_cs_bry_01_entry = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_encountered_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_encountered_CS_BRY_01")) return 0;
    ds_map_set(global.characterDataMap, "EAO_encountered_CS_BRY_01", 1);
    return 0;
};
