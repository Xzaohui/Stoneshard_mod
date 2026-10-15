// evt_FX_QRY_field_night · engine event 71921 · on_interaction_if_night · repeatable
// Registry: reads nothing, writes nothing. Night reads the native
// global.timeDataMap hours; the pilot window is 21:00–05:00. Inlined.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_night", 71921);
eao_fx_qry_night = function() {
    if (!variable_global_exists("timeDataMap") || !is_real(global.timeDataMap) || !ds_exists(global.timeDataMap, ds_type_map)) return 0;
    var _h = ds_map_find_value(global.timeDataMap, "hours");
    return _h >= 21 || _h < 5;
};
