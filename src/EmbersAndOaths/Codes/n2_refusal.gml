// evt_N2_refusal · engine event 10644 · on_refusal · repeatable
// Registry: reads presence_N2; writes presence_N2=refused once effective.
// A refusal never rolls back a settlement and never resolves the case.
ds_map_set(global.EAO_event_stubs, "evt_N2_refusal", 10644);
eao_n2_refusal = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_N2") && ds_map_find_value(global.characterDataMap, "EAO_resolve_N2") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_presence_N2", "refused");
    return 0;
};
