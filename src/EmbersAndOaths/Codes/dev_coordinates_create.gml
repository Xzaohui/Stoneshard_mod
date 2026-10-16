event_inherited();
// Native adaptive positioning switches on exact object_index, so subclasses
// need the same center offset explicitly through the native layout API.
scr_guiLayoutOffsetUpdate(id,(global.cameraWidth-sprite_width)/2,(global.cameraHeight-sprite_height)/2);
eao_coord_owner=noone;
eao_coord_character=global.characterDataMap;
eao_coord_keyboard_before=keyboard_string;
eao_coord_keyboard_owned=true;
keyboard_string="";
eao_coord_text="";
eao_coord_error="";
eao_coord_closing=false;
eao_coord_queued=false;
eao_coord_armed=false;
eao_coord_released=false;
// Native buttons keep focused mouse handling. Disable their Space/Return
// shortcut (par_event==0); this editor handles Return after reading the text.
acceptButton.par_event=2;
text=(global.language==3 ? "开发传送 x,y  范围 " : "DEV teleport x,y  range ")
    +"0.."+string(global.worldWidth-1)+",0.."+string(global.worldHeight-1);
drawAddText=true;
addText=global.language==3 ? "输入坐标；Enter确认，Esc取消" : "Type coordinates; Enter accepts, Esc cancels";
