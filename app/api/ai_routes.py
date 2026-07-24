from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.dependencies import get_bedrock_service
from app.schemas.ticket_schema import (
    SummarizeRequest,
    SummarizeResponse,
)
from app.services.aws.bedrock_service import (
    BedrockService,
    BedrockServiceError,
    FakeBedrockService,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/summarize",
    response_model=SummarizeResponse,
)
def summarize_ticket(
    payload: SummarizeRequest,
    service: BedrockService | FakeBedrockService = Depends(
        get_bedrock_service
    ),
) -> dict[str, str]:
    try:
        return service.summarize_ticket(
            payload.ticket_description
        )
    except BedrockServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service is temporarily unavailable",
        ) from exc