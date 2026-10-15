// Shared save-key helpers (HX01-26 / M3).
// Missing keys return the declared default. All boolean saves use the
// strings "true" / "false". Callers that run inside an already-pushed
// dialogue callback should prefer the inlined form below — bare eao_*
// calls from nested method entries crashed the 0.1.1 runner.
global.eao_state_get = function(_key, _default) {
    if (!ds_map_exists(global.characterDataMap, _key)) return _default;
    return ds_map_find_value(global.characterDataMap, _key);
};
global.eao_state_set = function(_key, _value) {
    ds_map_set(global.characterDataMap, _key, _value);
    return 1;
};
// Write once while the key is still at its unset sentinel (or absent).
global.eao_state_set_once = function(_key, _value, _unset) {
    if (ds_map_exists(global.characterDataMap, _key)) {
        if (ds_map_find_value(global.characterDataMap, _key) != _unset) return 0;
    }
    ds_map_set(global.characterDataMap, _key, _value);
    return 1;
};
// S62 route keys. Never write the new route vocabulary into EAO_resolve_*.
global.eao_write_route = function(_task, _value) {
    return eao_state_set_once("EAO_route_" + _task, _value, "none");
};
// M1 writers. Values are always strings. Hang these on N8 / N12 / N16 /
// N17 / SQ01 choice callbacks once those quests land in src/.
global.eao_write_ferry_depot_claim = function(_value) {
    return eao_state_set_once("EAO_ferry_depot_claim", _value, "none");
};
global.eao_write_n8_relief = function(_value) {
    return eao_state_set_once("EAO_n8_relief", _value, "unseen");
};
global.eao_write_toman_personnel = function(_value) {
    // _value must be the string "true" or "false".
    return eao_state_set_once("EAO_toman_personnel", _value, "false");
};
global.eao_write_custody_intent = function(_value) {
    return eao_state_set_once("EAO_custody_intent", _value, "none");
};
global.eao_write_custody_signed = function(_value) {
    return eao_state_set_once("EAO_custody_signed", _value, "none");
};
