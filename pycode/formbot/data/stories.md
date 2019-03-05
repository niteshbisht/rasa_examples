## happy path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## unhappy path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
* chitchat
    - utter_chitchat
    - account_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## very unhappy path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
* chitchat
    - utter_chitchat
    - account_form
* chitchat
    - utter_chitchat
    - account_form
* chitchat
    - utter_chitchat
    - account_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop but continue path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
* stop
    - utter_ask_continue
* affirm
    - account_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop and really stop path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## chitchat stop but continue path
* open_account
    - account_form
    - form{"name": "account_form"}
* chitchat
    - utter_chitchat
    - account_form
* stop
    - utter_ask_continue
* affirm
    - account_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## stop but continue and chitchat path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
* stop
    - utter_ask_continue
* affirm
    - account_form
* chitchat
    - utter_chitchat
    - account_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## chitchat stop but continue and chitchat path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
* chitchat
    - utter_chitchat
    - account_form
* stop
    - utter_ask_continue
* affirm
    - account_form
* chitchat
    - utter_chitchat
    - account_form
    - form{"name": null}
    - utter_slots_values
* thankyou
    - utter_noworries

## chitchat, stop and really stop path
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
* chitchat
    - utter_chitchat
    - account_form
* stop
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}

## Generated Story 3490283781720101690 (example from interactive learning, "form: " will be excluded from training)
* greet
    - utter_greet
* open_account
    - account_form
    - form{"name": "account_form"}
    - slot{"requested_slot": "account"}
* chitchat
    - utter_chitchat  <!-- restaurant_form was predicted by FormPolicy and rejected, other policy predicted utter_chitchat -->
    - account_form
    - slot{"requested_slot": "account"}
* form: inform{"account": "trade"}
    - slot{"account": "trade"}
    - form: account_form
    - slot{"account": "trade"}
    - slot{"requested_slot": "accounttype"}
* form: inform{"text": "advisory"}
    - form: account_form
    - slot{"accounttype": "advisory"}
    - slot{"requested_slot": "producttype"}
* chitchat
    - utter_chitchat
    - account_form
    - slot{"requested_slot": "producttype"}
* stop
    - utter_ask_continue
* affirm
    - account_form  <!-- FormPolicy predicted FormValidation(False), other policy predicted restaurant_form -->
    - slot{"requested_slot": "producttype"}
* form: affirm
    - form: account_form
    - slot{"producttype": "mutual"}
    - slot{"requested_slot": "adjustmenttype"}
* form: inform
    - form: account_form
    - slot{"adjustmenttype": "/inform"}
    - slot{"requested_slot": "feedback"}
* form: inform{"feedback": "great"}
    - slot{"feedback": "great"}
    - form: account_form
    - slot{"feedback": "great"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_slots_values
* thankyou
    - utter_noworries
