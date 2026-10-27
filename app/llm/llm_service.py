from ollama import chat
import time
import json


class LLMService:
    def __init__(self, model):
        self.model = model

    def generate(self, prompt):
        try:
            start_time = time.perf_counter()
            response = chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                think=False,
                format={
                    "type": "object",
                    "properties": {
                        "match": {
                            "type": "boolean"
                        },
                        "resume_skill": {
                            "type": ["string", "null"]
                        }
                    },
                    "required": ["match", "resume_skill"]
                },
                options={
                    "temperature": 0,
                    "seed": 365,
                    "num_predict": 64
                }
            )

            elapsed_time = time.perf_counter() - start_time
            print(f"Total LLM time: {elapsed_time:.2f} seconds")
            return json.loads(response["message"]["content"])

        except Exception as e:
            print(f"LLM error: {e}")
            return {
                "match": False,
                "resume_skill": None
            }