from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from com.ms.bot.bot import FastSearchAPI

class ActionSearchWorkflows(Action):
    def name(self):
        return 'action_search_applications'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("looking for applications")
        applications_api = FastSearchAPI()
        applicationNames = applications_api.search(tracker.get_slot("application"))
        return [SlotSet("matches", applicationNames)]


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
