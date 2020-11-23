## are you hiring
* ask_are_you_hiring OR heard_you_are_hiring
  - utter_ask_schedule_call_discuss

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

## send resume
* send_resume
  - utter_sure
  - Nou_form
  - form{"name": "Nou_form"}
  - form{"name": null}
  - email_form
  - form{"name": "email_form"}
  - form{"name": null}
  - utter_confirm_best_email
* affirm
  - action_send_res
  - utter_anything_else

## request cv
* make_request {"res": "cv"}
  - utter_confirm_best_email
  - action_send_res  
  - utter_smiley

## request jd
* make_request {"res": "jd"}
  - utter_confirm_best_email
  - action_send_res
  - utter_smiley
