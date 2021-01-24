## are you hiring
* ask_are_you_hiring OR heard_you_are_hiring
  - utter_ask_schedule_call_discuss
* affirm
  -  when_form
  - form{"name": "when_form"}
  - form{"name": null}

## are you hiring
* ask_are_you_hiring OR heard_you_are_hiring
  - utter_ask_schedule_call_discuss
* deny
  - utter_ask_howcanihelp

## are you open to
* ask_are_you_open_to
  - utter_affirm
  - utter_ask_schedule_call_discuss

## did you get candidates
* did_you_get_candidates
  - utter_ask_schedule_call_discuss

## did you send resume
* did_you_send_resume
  - utter_ask_schedule_call_discuss

## greet + are you hiring
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* ask_are_you_hiring OR heard_you_are_hiring
  - utter_ask_schedule_call_discuss

## greet + are you open to
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* ask_are_you_open_to
  - utter_affirm
  - utter_ask_schedule_call_discuss

## greet + did you get candidates
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* did_you_get_candidates
  - utter_ask_schedule_call_discuss

## greet + did you send resume
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* did_you_send_resume
  - utter_ask_schedule_call_discuss

## greet + send resume
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* send_resume
  - utter_sure
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks
  - action_send_res
  - utter_anything_else
* affirm  
  - utter_ask_howcanihelp

## greet + send resume + change email
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* send_resume
  - utter_sure
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* deny OR best_email_is
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks  
  - action_send_res
  - utter_anything_else
* affirm  
  - utter_ask_howcanihelp

## send resume + change email
* send_resume
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* deny OR best_email_is
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks
  - action_send_res
  - utter_anything_else
* affirm
  - utter_ask_howcanihelp

## send resume
* send_resume
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* deny OR best_email_is
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks
  - action_send_res
  - utter_anything_else
* affirm
  - utter_ask_howcanihelp

## send latest resume
* is_resume_current
  - utter_lm_send_it
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks  
  - action_send_res  
  - utter_anything_else  
* affirm  
  - utter_ask_howcanihelp

## send latest resume
* is_resume_current
  - utter_lm_send_it
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* deny OR best_email_is
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks  
  - action_send_res  
  - utter_anything_else
* affirm  
  - utter_ask_howcanihelp

## send latest resume
* is_resume_current
  - utter_lm_send_it
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* deny OR best_email_is
  - utter_sorry
  - action_reset_email
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks  
  - action_send_res  
  - utter_anything_else
* deny  
  - utter_ok
  - utter_thanks

## request cv
* make_request {"res": "cv"}
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks  
  - action_send_res  
  - utter_anything_else
* affirm  
  - utter_ask_howcanihelp

## request jd
* make_request {"res": "jd"}
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks  
  - action_send_res
  - utter_anything_else
* affirm  
  - utter_ask_howcanihelp


## cross-domain
* greet
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - utter_ask_howcanihelp
* send_resume
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm OR thanks
  - action_send_res
  - utter_anything_else
* affirm  
  - utter_ask_howcanihelp
* ask_availability
  - who_form
  - form{"name": "who_form"}
  - form{"name": null}
  - utter_nicetohearfromu
  - action_preprocess_when
  - when_form
  - form{"name": "when_form"}
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
