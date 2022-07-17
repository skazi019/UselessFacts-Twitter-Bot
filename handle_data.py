import json
import ast

with open("./facts.json", "rb") as f:
    facts = ast.literal_eval(json.load(f))

for id, fact in enumerate(facts):
    fact["id"] = id
    print(id)

with open("./facts.json", "w", encoding="utf-8") as f:
    json.dump(fact, f, ensure_ascii=False, indent=4)
