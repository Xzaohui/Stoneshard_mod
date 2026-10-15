// evt_CS_BRY_01_feedback_3_late · engine event 50585 · on_state_read · once
// Registry: reads order_CS_BRY_01, writes nothing. Late variant selector for
// the patron receipt; inlined (no helper calls).
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_feedback_3_late", 50585);
eao_cs_bry_01_feedback_3_late = function() {
    return ds_map_exists(global.characterDataMap, "EAO_order_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_order_CS_BRY_01") == "late";
};
