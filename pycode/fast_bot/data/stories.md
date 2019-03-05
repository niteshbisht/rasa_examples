## story_00914561
* greet
 - utter_ask_howcanhelp
* inform{"useraction":"open account"}
 - utter_ask_accounttype
* inform{"accounttype":"trade"}
 - utter_inform_user_account_type
* affirm
 - utter_just_a_minute
 - action_search_relevance
 - utter_display_relevantaccount
* affirm
 - action_search_product_type
 - utter_ask_product_type
* inform{"prodtype":"equity"}
 - action_search_adjustments
 - utter_ask_adjustments
* inform{"adjustment":"Account Type Change"}
 - utter_ask_confirmation
* affirm
 -utter_ack_workflow_details 
    
## story_00914561
* greet
 - utter_ask_howcanhelp
* inform{"useraction":"open account"}
 - utter_ask_accounttype
* inform{"accounttype":"trade"}
 - utter_inform_user_account_type
* affirm
 - utter_just_a_minute
 - action_search_relevance
 - utter_display_relevantaccount
* noinfo
 - action_search_other_account_types
 - utter_list_other_account_types
  
## story forms happy path  
* greet
 - utter_greet
* account_closure
 - account_closure_form
 - form{"name": "account_closure_form"}
 - form{"name": null}
 - utter_slots_values
* thankyou
 - utter_noworries