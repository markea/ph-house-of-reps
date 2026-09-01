from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def get_current_user(
    db: Session = Depends(get_db),
    x_goog_authenticated_user_email: str = Header(None)
) -> User:
    """
    Extracts the authenticated user.
    In Local mode (AUTH_MODE='mock'): Defaults to the seeded staff requester.
    In Prod mode (AUTH_MODE='iap'): Extracts verified identity from Google Cloud IAP header.
    """
    if settings.AUTH_MODE == "iap" and x_goog_authenticated_user_email:
        # Format in IAP: accounts.google.com:username@hrep.gov.ph
        email = x_goog_authenticated_user_email.split(":")[-1]
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user
            
    # Default / Local fallback
    user = db.query(User).filter(User.email == "staff.maria@hrep.gov.ph").first()
    if not user:
        user = db.query(User).first()
    return user

@router.get("/me")
def get_user_profile(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "position": user.position,
        "auth_mode": settings.AUTH_MODE,
        "app_env": settings.APP_ENV
    }
