from typing import Dict, Text, Any, List, Union

from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT


class AccountClosureForm(FormAction):
    def name(self):
        return "account_closure_form"

    @staticmethod
    def required_slots(tracker):
        # type: () -> List[Text]
        """A list of required slots that the form has to fill"""
        return ["account_type", "account_category", "account_number",
                "branch", "feedback"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"account_type": self.from_entity(entity="account_type",
                                                 not_intent="chitchat"),
                "account_category": [self.from_entity(entity="account_category", intent=["inform",
                                                                                         "open account"]),
                                     self.from_text()],
                "account_number": [self.from_entity(entity="account_number",
                                                    intent=["inform",
                                                            "request_accountnumber"]),
                                   self.from_entity(entity="number")],
                "branch": [self.from_entity(entity="branch",
                                            intent=["inform",
                                                    "request_branch"]),
                           self.from_entity(entity="number")],
                "feedback": [self.from_entity(entity="feedback"),
                             self.from_text()]}

    @staticmethod
    def account_db():
        # type: () -> List[Text]
        """Database of supported cuisines"""
        return ["trade",
                "IRA",
                "529K"
                ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

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
            if slot == 'account_type':
                if value.lower() not in self.account_db():
                    dispatcher.utter_template('utter_wrong_account', tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None

            elif slot == 'account_number':
                if not self.is_int(value) or int(value) <= 0:
                    dispatcher.utter_template('utter_wrong_account',
                                              tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None

            elif slot == 'branch':
                if not self.is_int(value) or int(value) <= 0:
                    dispatcher.utter_template('utter_wrong_branch',
                                              tracker)
                    # validation failed, set slot to None
                    slot_values[slot] = None

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        return []
