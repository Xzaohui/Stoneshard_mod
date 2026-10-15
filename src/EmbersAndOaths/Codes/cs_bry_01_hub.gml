// evt_CS_BRY_01_hub · engine event 50577 · on_interaction · repeatable
// Registry: reads encountered_CS_BRY_01, writes nothing. The hub only selects
// repeatable lines: 1 = case opened, 3 = the shift-witness scene (场2) has
// been played this session. The witness flag is a runtime gate, not a save key.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_hub", 50577);
eao_cs_bry_01_hub = function() {
    if (!(ds_map_exists(global.characterDataMap, "EAO_encountered_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_encountered_CS_BRY_01"))) return 0;
    if (variable_global_exists("EAO_cs_runtime_witness") && global.EAO_cs_runtime_witness) return 3;
    return 1;
};
eao_cs_bry_01_witness_mark = function() {
    global.EAO_cs_runtime_witness = true;
    return 0;
};
