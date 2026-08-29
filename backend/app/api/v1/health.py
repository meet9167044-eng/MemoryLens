from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=dict)
def health_check():
    """
    Health check endpoint.
    Returns 200 OK when the service is running.
    """
    return {"status": "ok"}
