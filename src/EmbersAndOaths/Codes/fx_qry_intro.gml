// evt_FX_QRY_field_intro · engine event 71920 · on_first_interaction · once
// Registry: reads presence_FX_QRY, writes nothing (the FX layer keeps only
// the presence key). First-meet is tracked with a session-scope flag so the
// save stays untouched; the first greeting replays after a game restart.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_intro", 71920);
eao_fx_qry_intro = function() {
    if (!variable_global_exists("EAO_fx_qry_seen") || !global.EAO_fx_qry_seen) {
        global.EAO_fx_qry_seen = true;
        return 1;
    }
    return 0;
};
