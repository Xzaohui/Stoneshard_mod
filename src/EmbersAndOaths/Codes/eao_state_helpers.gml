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
// Bodies are inlined (no eao_* helper calls) to match the 0.1.1 runner rule.
global.eao_write_route = function(_task, _value) {
    var _k = "EAO_route_" + _task;
    if (ds_map_exists(global.characterDataMap, _k) && ds_map_find_value(global.characterDataMap, _k) != "none") return 0;
    ds_map_set(global.characterDataMap, _k, _value);
    return 1;
};
// M1 writers. Values are always strings. Hang these on N8 / N12 / N16 /
// N17 / SQ01 choice callbacks once those quests land in src/.
global.eao_write_ferry_depot_claim = function(_value) {
    if (ds_map_exists(global.characterDataMap, "EAO_ferry_depot_claim") && ds_map_find_value(global.characterDataMap, "EAO_ferry_depot_claim") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_ferry_depot_claim", _value);
    return 1;
};
global.eao_write_n8_relief = function(_value) {
    if (ds_map_exists(global.characterDataMap, "EAO_n8_relief") && ds_map_find_value(global.characterDataMap, "EAO_n8_relief") != "unseen") return 0;
    ds_map_set(global.characterDataMap, "EAO_n8_relief", _value);
    return 1;
};
global.eao_write_toman_personnel = function(_value) {
    // _value must be the string "true" or "false".
    if (ds_map_exists(global.characterDataMap, "EAO_toman_personnel") && ds_map_find_value(global.characterDataMap, "EAO_toman_personnel") != "false") return 0;
    ds_map_set(global.characterDataMap, "EAO_toman_personnel", _value);
    return 1;
};
global.eao_write_custody_intent = function(_value) {
    if (ds_map_exists(global.characterDataMap, "EAO_custody_intent") && ds_map_find_value(global.characterDataMap, "EAO_custody_intent") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_custody_intent", _value);
    return 1;
};
global.eao_write_custody_signed = function(_value) {
    if (ds_map_exists(global.characterDataMap, "EAO_custody_signed") && ds_map_find_value(global.characterDataMap, "EAO_custody_signed") != "none") return 0;
    ds_map_set(global.characterDataMap, "EAO_custody_signed", _value);
    return 1;
};
