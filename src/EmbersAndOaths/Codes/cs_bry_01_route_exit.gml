// evt_CS_BRY_01_route_exit · engine event 50579 · on_route_selected · once
// Registry: reads resolve_CS_BRY_01; writes callback/consent/paid of the exit
// group. Implementation also lands resolve_CS_BRY_01 = exit here. The two
// routes are mutually exclusive; the untaken group is never written.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_route_exit", 50579);
eao_cs_bry_01_route_exit = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_resolve_CS_BRY_01") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_resolve_CS_BRY_01", "exit");
    ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_exit", 1);
    ds_map_set(global.characterDataMap, "EAO_consent_CS_BRY_01_exit", 1);
    ds_map_set(global.characterDataMap, "EAO_paid_CS_BRY_01_exit", 1);
    return 0;
};
