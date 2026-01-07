import os
from huggingface_hub import InferenceClient
import asyncio
from base import ModelCient

HF_API_KEY = os.getenv("HF_API_KEY")


class HuggingClient(ModelCient):
    def __init__(self, api_key=None):
        self.api_key = api_key or HF_API_KEY

        if not self.api_key:
            raise RuntimeError("No API KEY")
        
        self.client = InferenceClient(
            api_key=self.api_key,
        )

    def _query_model(self, model, query):
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
        )
        return completion.choices[0].message
    
    async def generate_code(self, model, prompt):
        """
        Calls the inference api for the specified model(s)
        with the problem.
        
        :param model: The LLM agent name.
        :param problem: The coding problem to be solved.
        """
        return await asyncio.to_thread(self._query_model, model, prompt)
