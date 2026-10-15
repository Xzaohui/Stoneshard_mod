// evt_FX_QRY_field_refusal · engine event 71927 · on_refusal · repeatable
// Registry: reads presence_FX_QRY. Implementation writes presence = refused
// when the keeper declines to scout the pit for the player (registered
// delta, same pattern as evt_N2_refusal). Refusal keeps a replacement exit:
// the rim warning and the site lines stay available.
ds_map_set(global.EAO_event_stubs, "evt_FX_QRY_field_refusal", 71927);
eao_fx_qry_refusal = function() {
    ds_map_set(global.characterDataMap, "EAO_presence_FX_QRY", "refused");
    return 0;
};
