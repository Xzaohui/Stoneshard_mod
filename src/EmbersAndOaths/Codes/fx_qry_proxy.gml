// evt_FX_QRY_field_proxy · engine event 71928 · on_presence_check · repeatable
// Registry: reads presence_FX_QRY, writes nothing. True while the keeper is
// absent or dead: only the proxy statement may play, and the white line
// keeps its warning. No bystander may state a new decision for her.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_proxy", 71928);
eao_fx_qry_proxy = function() {
    if (!ds_map_exists(global.characterDataMap, "EAO_presence_FX_QRY")) return 0;
    var _p = ds_map_find_value(global.characterDataMap, "EAO_presence_FX_QRY");
    return _p == "absent" || _p == "dead";
};
