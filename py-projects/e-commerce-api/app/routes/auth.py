from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/health")
def auth_health():
    return {"message": "Auth router is working"}

@router.post("/register")
def register_user():
    pass