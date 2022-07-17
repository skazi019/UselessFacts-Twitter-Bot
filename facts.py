import os, json, random
import pandas as pd

BASE_URL = os.path.abspath(os.getcwd())


class Facts:
    def read_facts(self) -> dict:
        with open(os.path.join(BASE_URL, "facts.json"), "rb") as data:
            facts = json.load(data)
        return facts

    def save_facts(self, fact: dict) -> bool:
        day = self.get_post_day()
        fact_id = fact["id"]
        all_facts = self.read_facts()
        all_facts["day"] = day
        all_facts_df = pd.DataFrame.from_records(all_facts["facts"])
        all_facts_df.loc[all_facts_df["id"] == fact_id, "posted"] = 1
        all_facts["facts"] = json.loads(all_facts_df.to_json(orient="records"))

        with open(os.path.join(BASE_URL, "facts.json"), "w") as data:
            json.dump(all_facts, data, ensure_ascii=False, indent=4)

        return True

    def random_fact(self) -> dict:
        facts: dict = self.read_facts()
        fact: dict = random.choice(facts["facts"])
        while fact["posted"] != 0:
            fact: dict = random.choice(facts["facts"])
        return fact

    def get_post_day(self) -> int:
        facts: dict = self.read_facts()
        day: int = facts["day"]
        day += 1
        return day
