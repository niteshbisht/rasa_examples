help:
	@echo "    run"
	@echo "        Runs the bot on the command line."
	@echo "    run-actions"
	@echo "        Runs the action server."
	@echo "    run-core"
	@echo "        Runs the core server."
	@echo "    run-vis"
	@echo "        Runs Visualization."
	@echo "    train-nlu"
	@echo "        Train the natural language understanding using Rasa NLU."
	@echo "    train-core"
	@echo "        Train a dialogue model using Rasa core."

run:
	make run-actions&
	make run-core

run-actions:
	python -m rasa_core_sdk.endpoint --actions actions

run-vis:
	python bot.py run-vis

run-core:
	python -m rasa_core.run --nlu models/nlu/default/current --core models/dialogue --endpoints endpoints.yml

train-nlu:
	python bot.py train-nlu

train-core:
	python bot.py train-dialogue
