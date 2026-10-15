// evt_CS_BRY_01_feedback_3_early · engine event 50584 · on_state_change · once
// Registry: reads resolve_CS_BRY_01, writes the callback of the taken route.
// Patron receipt; same guarded body, inlined (no helper calls).
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_feedback_3_early", 50584);
eao_cs_bry_01_feedback_3_early = function() {
    if (!ds_map_exists(global.characterDataMap, "EAO_resolve_CS_BRY_01")) return 0;
    var _r = ds_map_find_value(global.characterDataMap, "EAO_resolve_CS_BRY_01");
    if (_r == "none") return 0;
    if (!ds_map_exists(global.characterDataMap, "EAO_order_CS_BRY_01")) ds_map_set(global.characterDataMap, "EAO_order_CS_BRY_01", "early");
    if (_r == "continuity") ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_continuity", 1);
    else ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_exit", 1);
    return 1;
};
