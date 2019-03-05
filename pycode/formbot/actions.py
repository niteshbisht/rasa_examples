# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT


class RestaurantForm(FormAction):
    """Example of a custom form action"""

    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""

        return "account_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["account", "accounttype", "producttype",
                "adjustmenttype", "feedback"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"account": self.from_entity(entity="account",
                                            not_intent="chitchat"),
                "accounttype": [self.from_entity(entity="accounttype",
                                                 intent=["inform",
                                                         "open_account"]),
                                self.from_text()],
                "producttype": [self.from_entity(entity="producttype",
                                                 not_intent="chitchat"),
                                self.from_text()],
                "adjustmenttype": [self.from_entity(entity="adjustmenttype"),
                                   self.from_text()],
                "feedback": [self.from_entity(entity="feedback"),
                             self.from_text()]}

    @staticmethod
    def account_db():
        # type: () -> List[Text]
        """Database of supported cuisines"""
        return ["trade",
                "trust",
                "retirements",
                "trading",
                "529k"
                ]

    @staticmethod
    def accounttype():
        # type: () -> List[Text]
        """Database of supported account types"""
        return ["advisory",
                "non advisory",
                ]

    @staticmethod
    def prodtype():
        # type: () -> List[Text]
        """Database of supported product types"""
        return ["equity",
                "mutual",
                ]

    @staticmethod
    def adjtype():
        # type: () -> List[Text]
        """Database of supported adjustment types"""
        return ["account type change",
                "account number change",
                ]

    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        # we'll check when validation failed in order
        # to add appropriate utterances
        for slot, value in slot_values.items():
            if slot == 'account':
                if value.lower() not in self.account_db():
                    dispatcher.utter_template('utter_wrong_account', tracker)
                    dispatcher.utter_message('Here are few Types which you can '+ ", ".join(self.account_db()))
                    # validation failed, set slot to None
                    slot_values[slot] = None

            elif slot == 'accounttype':
                if value.lower() not in self.accounttype():
                    dispatcher.utter_template('utter_wrong_account_type', tracker)
                    dispatcher.utter_message('Here are few Types which you can '+", ".join(self.accounttype()))
                    # validation failed, set slot to None
                    slot_values[slot] = None

            elif slot == 'producttype':
                if value.lower() not in self.prodtype():
                    dispatcher.utter_template('utter_wrong_product_type', tracker)
                    dispatcher.utter_message('you can enter one of these '+", ".join(self.prodtype()))
                    # validation failed, set slot to None
                    slot_values[slot] = None

            elif slot == 'adjustmenttype':
                if value.lower() not in self.adjtype():
                    dispatcher.utter_template('utter_wrong_adjustment_type', tracker)
                    dispatcher.utter_message('below are the few options '+", ".join(self.adjtype()))
                    # validation failed, set slot to None
                    slot_values[slot] = None

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []
