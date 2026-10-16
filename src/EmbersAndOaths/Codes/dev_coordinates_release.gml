if(eao_coord_released) exit;
eao_coord_released=true;
if(eao_coord_keyboard_owned) {
    keyboard_string=eao_coord_keyboard_before;
    eao_coord_keyboard_owned=false;
}
if(instance_exists(block_gui)) instance_destroy(block_gui);
if(instance_exists(background)) instance_destroy(background);
scr_escapeButtonListRemove();
