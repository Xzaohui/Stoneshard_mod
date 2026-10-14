// evt_N2_entry · engine event 10640 · on_first_interaction · once
// Registry: reads encountered_N2, writes encountered_N2 (encounter, false/true).
// Pilot batch N2 (MGMT-PILOT-N2-S153): the case is taken by talking it through once.
ds_map_set(global.EAO_event_stubs, "evt_N2_entry", 10640);
eao_n2_entry = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_encountered_N2") && ds_map_find_value(global.characterDataMap, "EAO_encountered_N2")) return 0;
    ds_map_set(global.characterDataMap, "EAO_encountered_N2", 1);
    return 0;
};
