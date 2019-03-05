import argparse
import logging
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.memoization import MemoizationPolicy

from com.ms.policy.policy import FastSearchPolicy

logger = logging.getLogger(__name__)


class FastSearchAPI(object):
    def search(self, info):
        return "fast search app"


def train_dialogue(domain_file="../../../models/domain.yml",
                   model_path="../../../models/models/dialogue",
                   training_data_file="../../../models/stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            FastSearchPolicy(batch_size=100, epochs=400,
                                             validation_split=0.2)])

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

    training_data = load_data('../../../models/train_data/nlu_data/training_data.json')
    trainer = Trainer(config.load("../../../models/nlu_config.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('../../../models/models/nlu/',
                                      fixed_model_name="current")

    return model_directory


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
        description='starts the bot')

    parser.add_argument(
        'task',
        choices=["train-nlu", "train-dialogue", "run"],
        help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
