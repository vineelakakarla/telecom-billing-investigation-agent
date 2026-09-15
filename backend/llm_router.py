from litellm import Router
from .llm_config import MODEL_LIST

router = Router(
    model_list=MODEL_LIST
)