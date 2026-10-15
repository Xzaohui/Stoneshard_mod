// System-layer helper callbacks for the city pilot (CS-BRY-01). Only these
// three globals exist, referenced solely as pushed dialogue callbacks; their
// bodies are fully inlined (no helper calls at all — bare eao_* static calls
// caused the 0.1.1 runner crash). EAO_trust_BRY is the S87 town-trust band
// (-2..+2, default 0); the dev override is a runtime observation value only.
// The settlement gate requires the bounded shift witness (场2) first.
global.eao_cs_route_gate = function() {
    if (variable_global_exists("EAO_cs_runtime_witness") && global.EAO_cs_runtime_witness) return 0;
    return 1;
};
// Receipt selector: only the taken route's callback is re-asserted and order
// lands as early when the city chapter closes after this case.
global.eao_cs_receipt_pick = function() {
    if (!ds_map_exists(global.characterDataMap, "EAO_resolve_CS_BRY_01")) return 0;
    var _r = ds_map_find_value(global.characterDataMap, "EAO_resolve_CS_BRY_01");
    if (_r == "none") return 0;
    if (!ds_map_exists(global.characterDataMap, "EAO_order_CS_BRY_01")) ds_map_set(global.characterDataMap, "EAO_order_CS_BRY_01", "early");
    if (_r == "continuity") ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_continuity", 1);
    else ds_map_set(global.characterDataMap, "EAO_callback_CS_BRY_01_exit", 1);
    return 1;
};
// Town pool (TG-BRY-01..04): 0/1 any (alternating), 2 night, 3 after the
// city chapter. Night reads the native timeDataMap hours (21:00–05:00).
// Pools never write state keys.
global.eao_pool_town_bry = function() {
    if (ds_map_exists(global.characterDataMap, "EAO_resolve_CM_BRY")) return 3;
    if (variable_global_exists("timeDataMap") && is_real(global.timeDataMap) && ds_exists(global.timeDataMap, ds_type_map)) {
        var _h = ds_map_find_value(global.timeDataMap, "hours");
        if (_h >= 21 || _h < 5) return 2;
    }
    if (!variable_global_exists("EAO_pool_cursor_town")) global.EAO_pool_cursor_town = 0;
    global.EAO_pool_cursor_town = 1 - global.EAO_pool_cursor_town;
    return global.EAO_pool_cursor_town;
};
