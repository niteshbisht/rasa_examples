from rasa_nlu.model import Interpreter
import json
interpreter = Interpreter.load("../../../../models/models/current/nlu")
message = "we can eat dinner"
result = interpreter.parse(message)
print(json.dumps(result, indent=2))