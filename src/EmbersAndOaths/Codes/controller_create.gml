courier_id = noone;
state_map = -1;
test_guide_id = noone;
// Runtime registry of assigned engine event numbers (OI-02); stubs only
// ds_map_set into it. A plain variable, never a characterDataMap save key.
global.EAO_event_stubs = ds_map_create();
if (!instance_exists(o_eao_devtools)) instance_create_depth(0, 0, -100000, o_eao_devtools);
