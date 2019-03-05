#!/bin/bash
python -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
python -m rasa_nlu.train -c nlu_config.yml --data train_data/nlu_data -o models --fixed_model_name nlu --project current --verbose
rasa-nlu-trainer