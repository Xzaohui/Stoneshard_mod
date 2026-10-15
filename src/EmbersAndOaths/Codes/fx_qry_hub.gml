// evt_FX_QRY_field_hub · engine event 71922 · on_interaction · repeatable
// Registry: reads nothing, writes nothing. Presence selector: 0 = present
// (new lines allowed), 1 = refused (own new lines stop), 2 = absent or dead
// (proxy only). Inlined.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_hub", 71922);
eao_fx_qry_hub = function() {
    if (!ds_map_exists(global.characterDataMap, "EAO_presence_FX_QRY")) return 0;
    var _p = ds_map_find_value(global.characterDataMap, "EAO_presence_FX_QRY");
    if (_p == "refused") return 1;
    if (_p == "absent" || _p == "dead") return 2;
    return 0;
};
