from abc import ABC, abstractmethod
import asyncio


class ModelCient(ABC):
    """
    Serves as base class through inheritance

    Note: Template Method Pattern
    """

    @abstractmethod
    async def generate_code(self, model, problem):
        """
        Every Class that inherits ModelClient must implement.

        :param model: The name of the LLM to generate code from.
        :param problem: The coding problem.
        """
        pass

    async def generate_from_many(self, models, problem):
        tasks = {
            model: asyncio.create_task(self.generate_code(model, problem))
            for model in models
        }

        results = {}
        for model, task in tasks.items():
            try:
                results[model] = {"success": True, "error": None, "output": await task}
            except Exception as e:
                results[model] = {"success": False, "error": str(e), "output": None}

        return results
