import json
from prompts.loader import load_prompt
from app.models.Evaluation import JudgeEvalRecord

class LLMJudge:
    def __init__(self, client, model, config, prompt_version):
        self.client = client
        self.model = model,
        self.config = config,
        self.prompt_version = prompt_version


    async def compare(self, question, responses):
        system_prompt = load_prompt('judge', self.prompt_version, 'system')
        user_prompt_template = load_prompt('judge', self.prompt_version, 'user')

        user_prompt = user_prompt_template.format(coding_question=question, 
                                                  model_a=responses["model_a"],
                                                  model_b=responses["model_b"])
        
        final_prompt = f"{system_prompt}\n\n{user_prompt}"

        message = await self.client.generate(self.model, final_prompt)

        text = message.content.strip()

        try: 
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {
                "winner": "A",
                "reason": "Failed Judge Evaluation",
                "confidence": 0.0
            }
        

        return JudgeEvalRecord({

        })



    
        