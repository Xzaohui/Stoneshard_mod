// evt_CS_BRY_01_before_city · engine event 50588 · on_state_read · repeatable
// Registry: reads order_CS_BRY_01, writes nothing. True while this case was
// settled before the city chapter (order = early); only future lines change.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_before_city", 50588);
eao_cs_bry_01_before_city = function() {
    return ds_map_exists(global.characterDataMap, "EAO_order_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_order_CS_BRY_01") == "early";
};
