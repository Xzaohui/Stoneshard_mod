// Dev-only observation toggle (F4), requires the F6 master switch. Cycles a
// runtime override of the Brynn trust band (-2..+2, then back to live). The
// override never touches the save; clear it by cycling back to "live" or
// turning F6 off. Real writes still come only from registered sources.
if (!global.EAO_dev_enabled) exit;
if (!variable_global_exists("EAO_dev_trust_override")) global.EAO_dev_trust_override = -9;
if (global.EAO_dev_trust_override == -9) global.EAO_dev_trust_override = -2;
else if (global.EAO_dev_trust_override >= 2) global.EAO_dev_trust_override = -9;
else global.EAO_dev_trust_override += 1;
var _label = global.EAO_dev_trust_override == -9 ? (global.language == 3 ? "实时值" : "live") : string(global.EAO_dev_trust_override);
scr_actionsLogAddMessage((global.language == 3 ? "开发观察：布林信任档覆盖 → " : "DEV: Brynn trust override -> ") + _label);
