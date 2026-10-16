if(eao_coord_closing || !instance_exists(eao_coord_owner)) exit;
// Read the buffer here as well: a focused mouse click can precede Begin Step.
eao_coord_text=keyboard_string;
with(eao_coord_owner) {
    dev_coord_text=other.eao_coord_text;
    dev_coord_submitting=true;
    event_user(1);
    dev_coord_submitting=false;
}
eao_coord_error=eao_coord_owner.dev_coord_error;
if(eao_coord_owner.dev_coord_queued) {
    eao_coord_queued=true;
    eao_coord_closing=true;
}
