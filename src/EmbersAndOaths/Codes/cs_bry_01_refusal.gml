// evt_CS_BRY_01_refusal · engine event 50586 · on_refusal · repeatable
// Registry: reads presence_CS_BRY_01. Implementation writes presence =
// refused once the player explicitly declines the case (same registered
// delta as evt_N2_refusal). A refusal never rolls back a settlement and
// never resolves the case; basic city services stay untouched.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_refusal", 50586);
eao_cs_bry_01_refusal = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_CS_BRY_01") && ds_map_find_value(global.characterDataMap, "EAO_resolve_CS_BRY_01") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_presence_CS_BRY_01", "refused");
    return 0;
};
