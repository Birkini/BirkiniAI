# model_router.py

import uuid
import time
import logging
from typing import List, Dict

from birkini.sdk import (
    BirkiniClient,
    MCPClient,
    ZKMetaValidator,
    ModelRegistry,
    TaskRouter,
    ExecutionMonitor
)

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BirkiniModelRouter")

class ModelRouterService:
    def __init__(self, api_key: str):
        self.client = BirkiniClient(api_key=api_key)
        self.mcp = MCPClient()
        self.zk_validator = ZKMetaValidator()
        self.registry = ModelRegistry(self.client)
        self.router = TaskRouter(self.mcp)
        self.monitor = ExecutionMonitor()

    def discover_models(self, task_type: str) -> List[Dict]:
        logger.info(f"Discovering models registered for task type: {task_type}")
        models = self.registry.filter_models(task_type=task_type)
        verified_models = []

        for model in models:
            if self.zk_validator.verify_metadata(model["zk_meta"]):
                verified_models.append(model)

        logger.info(f"{len(verified_models)} valid models found for routing.")
        return verified_models

    def score_models(self, models: List[Dict]) -> List[Dict]:
        logger.info("Scoring models based on historical performance and context trust.")
        for model in models:
            model["score"] = (
                model["uptime"] * 0.4 +
                model["response_rate"] * 0.3 +
                model["context_trust"] * 0.3
            )
        return sorted(models, key=lambda m: m["score"], reverse=True)

    def route_task(self, task_payload: Dict, task_type: str) -> Dict:
        models = self.discover_models(task_type)
        if not models:
            logger.warning("No valid models available for routing.")
            return {"status": "failed", "reason": "no models found"}

        ranked_models = self.score_models(models)
        best_model = ranked_models[0]

        logger.info(f"Routing task to model: {best_model['name']} (score: {best_model['score']:.2f})")

        task_id = str(uuid.uuid4())
        self.router.send_task(task_id, model_id=best_model["id"], payload=task_payload)

        logger.info("Monitoring execution...")
        result = self.monitor.await_result(task_id)
        return {
            "status": "success",
            "model": best_model["name"],
            "result": result
        }

# Example Usage
if __name__ == "__main__":
    service = ModelRouterService(api_key="your_api_key_here")
    sample_payload = {
        "input": "Summarize this financial report using neutral tone.",
        "language": "en"
    }
    result = service.route_task(task_payload=sample_payload, task_type="text_summarization")
    logger.info(f"Final routed output:\n{result}")
