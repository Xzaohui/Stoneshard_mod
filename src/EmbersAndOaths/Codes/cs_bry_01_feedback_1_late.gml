// evt_CS_BRY_01_feedback_1_late · engine event 50581 · on_state_read · once
// Registry: reads order_CS_BRY_01, writes nothing. Selects the late variant
// of the civic receipt when the city chapter was closed before this case.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_feedback_1_late", 50581);
eao_cs_bry_01_feedback_1_late = function() {
    return ds_map_exists(global.characterDataMap, "EAO_order_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_order_CS_BRY_01") == "late";
};
