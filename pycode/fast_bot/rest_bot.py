import argparse
import logging
import http.client

from policy import FastSeacrhBotPolicy
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.form_policy import FormPolicy
import json
logger = logging.getLogger(__name__)


class AccountSearchAPI(object):
    def search(self, info):
        connection = http.client.HTTPConnection("localhost",3000)
        connection.request("GET", "/getFeed?param="+info)
        response = connection.getresponse()
        respObject = json.loads(response.read())
        logger.debug("Status: {} and reason: {} and response: {} and value: {}".format(response.status, response.reason, respObject, respObject['data']))
        return respObject['data']

class AccountTypeSearchAPI(object):
    def search(self, info):
        return "Trade"

def visualize(domain_file="domain.yml",
              training_data_file="data/stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            FastSeacrhBotPolicy(batch_size=100, epochs=400,
                                                validation_split=0.2), FormPolicy()])
    agent.visualize(training_data_file,
                    output_file="graph.html", max_history=2)

def train_dialogue(domain_file="domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            FastSeacrhBotPolicy(batch_size=100, epochs=400,
                                                validation_split=0.2), FormPolicy()])

    training_data = agent.load_data(training_data_file)
    agent.train(
        training_data
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data('data/nlu_data.md')
    trainer = Trainer(config.load("nlu_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/',
                                      fixed_model_name="current")

    return model_directory


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
        description='starts the bot')

    parser.add_argument(
        'task',
        choices=["train-nlu", "train-dialogue", "run", "run-vis"],
        help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run-vis":
        visualize()
