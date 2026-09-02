from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.config import settings, logger

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def verify_iap_jwt(iap_jwt: str, expected_audience: str) -> dict:
    """
    Verifies the cryptographically signed JWT assertion from Google Cloud IAP.
    Doc: https://cloud.google.com/iap/docs/signed-headers-howto
    """
    try:
        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token

        # Verify against Google's public keys
        payload = id_token.verify_token(
            iap_jwt,
            google_requests.Request(),
            audience=expected_audience,
            certs_url='https://www.gstatic.com/iap/verify/public_key'
        )
        return payload
    except Exception as e:
        logger.error(f"IAP JWT Verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or untrusted IAP authentication token.")

def get_current_user(
    db: Session = Depends(get_db),
    x_goog_authenticated_user_email: str = Header(None),
    x_goog_iap_jwt_assertion: str = Header(None)
) -> User:
    """
    Extracts and authenticates the user.
    - Production Mode (AUTH_MODE='iap'): Verifies cryptographic IAP token.
    - Localhost Mode (AUTH_MODE='mock'): Injects default staff persona.
    """
    if settings.AUTH_MODE == "iap" and settings.APP_ENV == "production":
        user_email = None
        
        # 1. Cryptographically verify IAP JWT Assertion if audience is configured
        if settings.IAP_AUDIENCE and x_goog_iap_jwt_assertion:
            claims = verify_iap_jwt(x_goog_iap_jwt_assertion, settings.IAP_AUDIENCE)
            user_email = claims.get("email")
        elif x_goog_authenticated_user_email:
            # Fallback format: accounts.google.com:username@hrep.gov.ph
            user_email = x_goog_authenticated_user_email.split(":")[-1]

        if not user_email:
            raise HTTPException(status_code=401, detail="Missing required IAP authentication credentials.")

        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            # Auto-provision user in directory if first time login via HRep Google Workspace
            user = User(
                email=user_email,
                full_name=user_email.split("@")[0].replace(".", " ").title(),
                role="Requester",
                position="House Personnel"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
            
    # Default Localhost Mock Fallback
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
