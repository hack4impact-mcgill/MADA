from functools import lru_cache

from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@lru_cache()
def get_settings():
    return schemas.Settings()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/")
def main():
    """
    Displays MADA
    :return: HTMLResponse - MADA
    """
    title = """
    <pre>                                                   
    _           _        _        _  _  _  _           _          
   (_) _     _ (_)     _(_)_     (_)(_)(_)(_)        _(_)_        
   (_)(_)   (_)(_)   _(_) (_)_    (_)      (_)_    _(_) (_)_      
   (_) (_)_(_) (_) _(_)     (_)_  (_)        (_) _(_)     (_)_    
   (_)   (_)   (_)(_) _  _  _ (_) (_)        (_)(_) _  _  _ (_)   
   (_)         (_)(_)(_)(_)(_)(_) (_)       _(_)(_)(_)(_)(_)(_)   
   (_)         (_)(_)         (_) (_)_  _  (_)  (_)         (_)   
   (_)         (_)(_)         (_)(_)(_)(_)(_)   (_)         (_)                                                     
    </pre>
    """
    return HTMLResponse(title)


@router.get("/health")
def health():
    """
    Displays a health check
    :return: HTMLResponse - MADA
    """
    health = "healthy"
    return HTMLResponse(health)
