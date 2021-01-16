
## multi intent (with name)
* multi_intent
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_ask_schedule_call_discuss
  - action_update_contacts
* affirm OR ask_which_day
  - utter_ask_day
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - action_date_parts
  - utter_sure_we_can
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* ask_availability
  - utter_pick_a_day

## greet with name
* greet_with_name
  - utter_greet
  - action_update_contacts
  - utter_ask_howcanihelp

## greet no name
* greet
  - utter_greet
  - utter_ask_who
* thisis
  - action_update_contacts
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* affirm OR ask_which_day
  - utter_ask_day
* ask_availability
  - utter_wunderbar
  - utter_pick_a_day

## who and time
* thisis
  - action_update_contacts
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* affirm OR ask_which_day
  - utter_ask_day
* ask_availability
  - utter_pick_a_day  

## who and denial for some reason
* thisis
  - action_update_contacts
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
* deny
  - utter_im_a_scheduling_agent

## is this you forest
* forest
  - utter_ask_who
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu


### ~~~~~~~~~~~~~~~~~~~~~ Discuss Day and Time ~~~~~~~~~~~~~~~~~~~~

## lets do
* lets_do OR can_we_do_something
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_day
  - action_preprocess_when  
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - action_date_parts
  - utter_sure_we_can
  - action_check_time

## availability
* ask_availability
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
  - form{"name": null}
  - action_date_parts

  - action_check_time
  - utter_sure_we_can
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}  
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm  
* affirm OR thanks
  - action_send_invite
* affirm OR ok
  - utter_looking_forward
* bye OR bye_fancy
  - utter_bye


## availability not ping pong but exactly the same
* ask_availability
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
* ask_availability
  - utter_pick_a_day
  - form{"name": null}
  - action_date_parts
  - action_check_time
  - utter_sure_we_can
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm  
* affirm OR thanks
  - action_send_invite
* affirm OR ok
  - utter_looking_forward
* bye OR bye_fancy
  - utter_bye

## suggest date
* suggest_date
  - action_check_date
  - utter_ask_time_date

## suggest different day
* suggest_different_date
  - action_check_date
  - utter_ask_time_date

## suggest different date
* suggest_different_date
  - action_check_date
  - utter_ask_time_date

## change day
* change_day_or_time {"date_or_time": "day"}
  - utter_confirm_change_day_or_time
  - utter_ask_day

## change date
* change_day_or_time {"date_or_time": "date"}
  - utter_confirm_change_day_or_time
  - utter_ask_date

## change time
* change_day_or_time {"date_or_time": "time"}
  - utter_confirm_change_day_or_time
  - utter_ask_time_day


### ~~~~~~~~~~~~~~~~~~~~~ Suggest Time ~~~~~~~~~~~~~~~~~~~~

## suggest day/time - "happy" path + yes
* suggest_availability OR when
  - action_check_day
  - action_date_parts
  - utter_ask_time_day
* suggest_time
  - action_check_time
  - utter_heres_my_number
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm  
* affirm OR thanks
  - action_send_invite
* affirm OR ok
  - utter_looking_forward
* bye OR bye_fancy
  - utter_bye

## suggest date/time - "happy" path + thx
* suggest_date
  - action_check_date
  - action_date_parts
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
* affirm OR thanks
  - utter_final_confirm
  - action_send_invite
* thanks OR thx
  - utter_np

## suggest date/time - "happy" path + pick place
* suggest_date
  - action_check_date
  - action_date_parts
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
* where_to_meet
  - ask_where
* suggest_location
  - utter_confirm_location
  - utter_shall_we_confirm
* affirm OR thanks
  - utter_final_confirm
  - action_send_invite
* thanks OR thx
  - utter_np

## suggest time of day - pick time + yes
* suggest_availability OR when
  - action_check_day
  - action_date_parts  
  - utter_ask_time_day
* time_of_day
  - utter_ask_specific_time
* suggest_time
  - action_check_time
  - utter_heres_my_number
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks OR affirm_day
  - utter_shall_we_confirm  
* affirm OR thanks
  - action_send_invite
* affirm OR ok
  - utter_looking_forward
* bye OR bye_fancy
  - utter_bye

## suggest date/time - "happy" path + thx BUT with email correction
* suggest_date
  - action_check_date
  - action_date_parts  
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
* affirm OR thanks
  - utter_final_confirm
  - action_send_invite
* thanks OR thx
  - utter_np

## don't confirm >  change date  > don't confirm
* suggest_date
  - action_check_date
  - action_date_parts  
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

## don't confirm >  change date  > don't confirm BUT with email correction
* suggest_date
  - action_check_date
  - action_date_parts  
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
  - utter_ask_date
* suggest_different_date OR suggest_date
  - action_check_date
  - utter_shall_we_confirm
* deny
  - utter_ask_change_what


## goodbye
* bye OR bye_fancy
  - utter_bye
