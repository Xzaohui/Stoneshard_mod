// evt_N2_hub · engine event 10641 · on_interaction · repeatable
// Registry: reads encountered_N2, writes nothing. A hub never settles anything;
// it only selects which repeatable lines each speaker plays.
ds_map_set(global.EAO_event_stubs, "evt_N2_hub", 10641);
eao_n2_hub = function() {
    return ds_map_exists(global.characterDataMap, "EAO_encountered_N2") && ds_map_find_value(global.characterDataMap, "EAO_encountered_N2");
};
