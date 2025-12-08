from fastapi import FastAPI
from routers.evaluate import router as eval_router

from util.questions import load_questions

app = FastAPI(title="Multi-agent Evaluator")
app.include_router(eval_router)



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/questions")
async def get_questions():
    questions = load_questions()
    return questions

@app.get("/questions/{id}")
async def get_question():

    pass