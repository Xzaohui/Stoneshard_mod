// evt_N2_choice_public · engine event 10643 · on_route_selected · once
// Registry: reads resolve_N2; writes resolve_N2=public + callback_N2_public.
// Settlement is exclusive and final: an already settled case is never rewritten.
ds_map_set(global.EAO_event_stubs, "evt_N2_choice_public", 10643);
eao_n2_choice_public = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_N2") && ds_map_find_value(global.characterDataMap, "EAO_resolve_N2") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_resolve_N2", "public");
    ds_map_set(global.characterDataMap, "EAO_callback_N2_public", 1);
    return 0;
};
