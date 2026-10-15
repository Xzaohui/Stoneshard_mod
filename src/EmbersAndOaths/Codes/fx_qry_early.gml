// evt_FX_QRY_field_early · engine event 71925 · on_state_read · once
// Registry: order-early while linked task still open (resolve_N7 default none).
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_early", 71925);
eao_fx_qry_early = function() {
    var _r = "none";
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_N7")) _r = ds_map_find_value(global.characterDataMap, "EAO_resolve_N7");
    return _r == "none" && variable_global_exists("EAO_fx_qry_seen") && global.EAO_fx_qry_seen;
};
