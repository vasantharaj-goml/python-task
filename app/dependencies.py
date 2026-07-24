import os
from functools import lru_cache

from dotenv import load_dotenv

from app.services.aws.bedrock_service import (
    BedrockService,
    FakeBedrockService,
)


load_dotenv()


@lru_cache
def get_bedrock_service() -> (
    BedrockService | FakeBedrockService
):
    demo_mode = (
        os.getenv("AWS_DEMO_MODE", "false").lower()
        == "true"
    )

    if demo_mode:
        return FakeBedrockService()

    return BedrockService()