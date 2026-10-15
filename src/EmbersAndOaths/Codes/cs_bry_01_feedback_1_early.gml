// evt_CS_BRY_01_feedback_1_early · engine event 50580 · on_state_change · once
// Registry: reads resolve_CS_BRY_01, writes the callback of the taken route
// (receipt-recorded). Implementation also lands order_CS_BRY_01 = early when
// the city chapter settles while this case is already closed. The untaken
// route's group is never written (registered delta: no blanket write).
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_feedback_1_early", 50580);
eao_cs_bry_01_feedback_1_early = function() {
    if (!ds_map_exists(global.characterDataMap, "EAO_resolve_CS_BRY_01")) return 0;
    var _r = ds_map_find_value(global.characterDataMap, "EAO_resolve_CS_BRY_01");
    if (_r == "none") return 0;
    if (!ds_map_exists(global.characterDataMap, "EAO_order_CS_BRY_01")) ds_map_set(global.characterDataMap, "EAO_order_CS_BRY_01", "early");
    if (_r == "continuity") ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_continuity", 1);
    else ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_exit", 1);
    return 1;
};
