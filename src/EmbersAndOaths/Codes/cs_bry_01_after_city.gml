// evt_CS_BRY_01_after_city · engine event 50589 · on_state_read · repeatable
// Registry: reads order_CS_BRY_01, writes nothing. True when the city chapter
// was already closed when this case settled (order = late); the independent
// lease can still be handled, no chapter protection is assumed.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_after_city", 50589);
eao_cs_bry_01_after_city = function() {
    return ds_map_exists(global.characterDataMap, "EAO_order_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_order_CS_BRY_01") == "late";
};
