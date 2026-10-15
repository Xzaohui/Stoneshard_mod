// evt_CS_BRY_01_absent · engine event 50587 · on_presence_check · repeatable
// Registry: reads presence_CS_BRY_01, writes nothing. Returns whether only
// proxy statements may play (absent or dead). No proxy may fabricate a new
// consent for the missing party.
ds_map_set(global.EAO_event_stubs, "evt_CS_BRY_01_absent", 50587);
eao_cs_bry_01_absent = function() {
    if (!ds_map_exists(global.characterDataMap, "EAO_presence_CS_BRY_01")) return 0;
    var _p = ds_map_find_value(global.characterDataMap, "EAO_presence_CS_BRY_01");
    return _p == "absent" || _p == "dead";
};
