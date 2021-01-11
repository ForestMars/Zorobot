## lets do
* lets_do OR can_we_do_something
  - utter_sure_we_can
  - utter_ask_day
* suggest_availability
  - action_check_day
  - utter_ask_time_day

## when is good
* when_is_good
  - utter_ask_day

## multi intent (with name)
* multi_intent
  - utter_nicetohearfromu
  - action_update_contacts
  - utter_ask_schedule_call_discuss
* affirm or ask_which_day
  - utter_ask_day  
* ask_availability or ask_which_day
  - utter_pick_a_day

## can u schedule this (with name)
* ask_call_with_name
  - utter_nicetohearfromu
  - action_update_contacts
  - utter_sure_we_can
* affirm or ask_which_day
  - utter_ask_day  
* ask_availability or ask_which_day
  - utter_pick_a_day  

## greet with name
* greet_with_name
  - utter_greet
  - utter_nicetohearfromu
  - action_update_contacts
  - utter_ask_schedule_call

## greet no name
* greet
  - utter_greet
  - utter_ask_who
* thisis
  - utter_nicetohearfromu
  - action_update_contacts
  - utter_ask_schedule_call
* affirm or ask_which_day
  - utter_ask_day
* ask_availability or ask_which_day
  - utter_pick_a_day

## who and time
* thisis
  - utter_nicetohearfromu
  - action_update_contacts
  - utter_ask_schedule_call
* affirm or ask_which_day
  - utter_ask_day
* ask_availability or ask_which_day
  - utter_pick_a_day  

## is this you forest
* forest
  - utter_zoro_greet
  - utter_ask_who

## schedule call
* schedule_call
  - utter_sure_we_can
  - utter_ask_who
* thisis
  - utter_ask_day

## availability follow up
* ask_availability OR following_up
  - nou_form
  - form{"name": "nou_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_sure_we_can
  - utter_ask_day
  - utter_sorry
* ask_availability or ask_which_day
  - utter_wunderbar
  - utter_sorry
  - utter_pick_a_day
* suggest_day
  - action_check_day
  - utter_ask_time_day  


## who and time
* thisis
  - utter_nicetohearfromu
  - action_update_contacts
  - utter_ask_schedule_call
* deny
  - utter_im_a_scheduling_agent

## goodbye
* bye OR bye_fancy
  - utter_bye

## test fragment - WTF / REMOVE
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
* deny
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email



### ~~~~~~~~~~~~~~~~~~~~~ Discuss Day and Time ~~~~~~~~~~~~~~~~~~~~

## suggest day
* suggest_day OR suggest_day_forest
  - action_check_day
  - utter_ask_time_day

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
* suggest_day OR when
  - action_check_day
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

## suggest time of day - pick time + yes
* suggest_day OR when
  - action_check_day
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
