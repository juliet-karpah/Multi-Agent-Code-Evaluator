import json
import os

file_path = os.path.join(os.path.dirname(__file__), "data/questions.json")

def load_questions(file_path, filters=None):
    try:
        with open(file_path, "r") as f:
            questions = json.load(f)

        if filters:
            for key, values in filters.items():
                questions = [q for q in questions if q.get(key) in values]

        return questions

    except Exception as e:
        raise RuntimeError(
            f"Error: An unexpected error occurred while loading JSON: {e}"
        )


def load_question(id):
    """
    Arg:
        id: the id of the question

    Return:
        A dict with the current question

    """

    questions = load_questions()
    for question in questions:
        if question["id"] == id:
            return question
        
    return None
