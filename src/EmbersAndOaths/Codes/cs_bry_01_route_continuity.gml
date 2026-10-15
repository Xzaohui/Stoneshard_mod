// evt_CS_BRY_01_route_continuity · engine event 50578 · on_route_selected · once
// Registry: reads resolve_CS_BRY_01; writes callback/consent/paid of the
// continuity group. Implementation also lands resolve_CS_BRY_01 = continuity
// here (same registered delta as the N2 choice stubs). Settlement is exclusive
// and final: an already settled case is never rewritten.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_route_continuity", 50578);
eao_cs_bry_01_route_continuity = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_resolve_CS_BRY_01") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_resolve_CS_BRY_01", "continuity");
    ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_continuity", 1);
    ds_map_set(global.characterDataMap, "EAO_consent_CS_BRY_01_continuity", 1);
    ds_map_set(global.characterDataMap, "EAO_paid_CS_BRY_01_continuity", 1);
    return 0;
};
