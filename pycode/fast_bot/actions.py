from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rest_bot import AccountSearchAPI, AccountTypeSearchAPI
import logging
from forms import fast_bot_form

logger = logging.getLogger(__name__)

class SearchRelevantAccountType(Action):
    def name(self):
        return 'action_search_relevance'

    def run(self,dispatcher, tracker, domain):
        return [SlotSet("relevantaccount", "Advisory")]

class SearchAdjustments(Action):
    def name(self):
        return 'action_search_adjustments'

    def run(self,dispatcher, tracker, domain):
        return [SlotSet("adjustmentlist", "Account Number Change, Account Type Change")]


class SearchProductTypes(Action):
    def name(self):
        return 'action_search_product_type'

    def run(self,dispatcher, tracker, domain):
        #dispatcher.utter_message("looking for Account types")
        return [SlotSet("producttypeslist", "Equity, Mutual")]


class ActionSearchAccountType(Action):
    def name(self):
        return 'action_search_other_account_types'

    def run(self,dispatcher, tracker, domain):
        dispatcher.utter_message("looking for other Account types")
        # accountTypeSearchAPI = AccountTypeSearchAPI()
        # probaccount = tracker.get_slot("probaccount")
        # logger.debug("probaccount = {}",probaccount)
        # accountType = accountTypeSearchAPI.search(probaccount)
        return [SlotSet("matches", "Retirements, 521K, Traditional")]

class ActionSearchAccounts(Action):
    def name(self):
        return 'action_search_queue'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for queue")
        queueSearch_api = AccountSearchAPI()
        queueTypes = queueSearch_api.search(tracker.get_slot("account"))
        return [SlotSet("matches", queueTypes)]


class ActionSuggest(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("here's what I found:")
        dispatcher.utter_message(tracker.get_slot("matches"))
        dispatcher.utter_message("is it ok for you? "
                                 "hint: I'm not going to "
                                 "find anything else :)")
        return []
