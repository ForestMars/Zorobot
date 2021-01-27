## greet with name
* thisis
  - utter_greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - action_update_contacts
  - utter_ask_howcanihelp

### ~~~~~~~~~~~~~~~~~~~~~ Discuss Day and Time ~~~~~~~~~~~~~~~~~~~~

## greet + lets do
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_ask_howcanihelp
* lets_do OR ask_availability
  - action_preprocess_when  
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - action_check_time
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm  
* affirm OR confirm_call
  - action_send_invite

## availability OR lets do
* lets_do
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - action_check_time
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}  
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm  
* affirm OR confirm_call
  - action_send_invite
* affirm OR ok OR thanks OR thx
  - utter_looking_forward
* bye OR bye_fancy
  - utter_bye


### ~~~~~~~~~~~~~~~~~~~~~ Availability ~~~~~~~~~~~~~~~~~~~~

## suggest day/time - HP + yes
* ask_availability OR suggest_availability
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - action_check_time
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm  
* affirm OR confirm_call
  - utter_heres_my_number
  - action_send_invite
* affirm OR ok OR thanks OR thx
  - utter_looking_forward
* bye OR bye_fancy
  - utter_bye

### ~~~~~~~~~~~~~~~~~~~~~ Suggest Date ~~~~~~~~~~~~~~~~~~~~

## suggest date
* suggest_date
  - action_check_date
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}

## suggest date/time - HP + email correction
* suggest_date
  - action_check_date
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_ask_time_date
* suggest_time
  - action_check_time
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* deny
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm
* affirm OR thanks
  - utter_final_confirm
  - utter_heres_my_number
  - action_send_invite
* thanks OR thx
  - utter_np

## don't confirm >  change date  > don't confirm
* suggest_date
  - action_check_date
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_ask_time_date
* suggest_time
  - action_check_time
  - utter_heres_my_number
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "date"}
  - utter_confirm_change_date_or_time
* affirm  
  - action_reset_date
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}  
  - utter_shall_we_confirm
* suggest_different_date OR suggest_date
  - action_check_date
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "date"}
  - utter_confirm_change_date_or_time
* affirm  
  - utter_ask_date
* suggest_different_date OR suggest_date
  - action_check_date
  - utter_shall_we_confirm  
* affirm OR confirm_call
  - utter_final_confirm
  - utter_heres_my_number
  - action_send_invite



## don't confirm >  change date  > don't confirm
* suggest_date
  - action_check_date
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_ask_time_date
* suggest_time
  - action_check_time
  - utter_heres_my_number
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "date"}
  - utter_confirm_change_date_or_time
* affirm  
  - utter_ask_date
* suggest_different_date OR suggest_date
  - action_check_date
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "day"}
  - utter_confirm_change_date_or_time
* affirm  
  - action_reset_date
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_shall_we_confirm  
* suggest_availability
  - action_check_day
  - utter_shall_we_confirm  
* affirm OR confirm_call
  - utter_final_confirm
  - utter_heres_my_number
  - action_send_invite

## don't confirm >  change date  > don't confirm
* suggest_date
  - action_check_date
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_ask_time_date
* suggest_time
  - action_check_time
  - utter_heres_my_number
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "time"}
  - utter_confirm_change_date_or_time
  - action_reset_time
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "time"}
  - utter_confirm_change_date_or_time


## don't confirm > change date + email correction
* suggest_date
  - action_check_date
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_ask_time_date
* suggest_time
  - action_check_time
  - utter_heres_my_number
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* deny
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "date"}
  - utter_confirm_change_date_or_time
* affirm  
  - action_reset_date
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - utter_shall_we_confirm  
* suggest_different_date OR suggest_date
  - action_check_date
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what
* change_day_or_time {"date_or_time": "date"}
  - utter_confirm_change_date_or_time
* affirm  
  - utter_ask_date
* suggest_date  
  - utter_shall_we_confirm


## check email
* do_you_have_my_email
  - utter_give_email_again

## confirm email
* best_email_is
  - utter_confirm_best_email

## check confirm email
* do_you_have_my_email
  - utter_give_email_again
* best_email_is
  - utter_confirm_best_email

## confirm call
* ask_to_confirm_call
  - action_confirm_event

## goodbye
* bye OR bye_fancy
  - utter_bye
