// evt_N2_choice_protected · engine event 10642 · on_route_selected · once
// Registry: reads resolve_N2; writes resolve_N2=protected + callback_N2_protected.
// Settlement is exclusive and final: an already settled case is never rewritten.
ds_map_set(global.EAO_event_stubs, "evt_N2_choice_protected", 10642);
eao_n2_choice_protected = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_N2") && ds_map_find_value(global.characterDataMap, "EAO_resolve_N2") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_resolve_N2", "protected");
    ds_map_set(global.characterDataMap, "EAO_callback_N2_protected", 1);
    return 0;
};
