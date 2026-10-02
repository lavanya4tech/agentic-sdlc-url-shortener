from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.responses import RedirectResponse

from pydantic import BaseModel, HttpUrl

from sqlalchemy.orm import Session

from ..infrastructure.database import get_db

from ..infrastructure.models import UrlModel

router = APIRouter()

class CreateUrlRequest(BaseModel):

    original_url: HttpUrl

class CreateUrlResponse(BaseModel):

    id: int

    original_url: str

    short_code: str

def generate_short_code(length: int = 6) -> str:

    import secrets

    import string

    characters = string.ascii_letters + string.digits

    return "".join(

        secrets.choice(characters)

        for _ in range(length)

    )

@router.post(

    "/urls",

    response_model=CreateUrlResponse,

    status_code=status.HTTP_201_CREATED,

)

def create_url(

    request: CreateUrlRequest,

    db: Session = Depends(get_db),

):

    short_code = generate_short_code()

    while (

        db.query(UrlModel)

        .filter(UrlModel.short_code == short_code)

        .first()

    ):

        short_code = generate_short_code()

    url = UrlModel(

        original_url=str(request.original_url),

        short_code=short_code,

    )

    db.add(url)

    db.commit()

    db.refresh(url)

    return CreateUrlResponse(

        id=url.id,

        original_url=url.original_url,

        short_code=url.short_code,

    )

@router.get("/{short_code}")

def redirect_url(

    short_code: str,

    db: Session = Depends(get_db),

):

    url = (

        db.query(UrlModel)

        .filter(

            UrlModel.short_code == short_code,

            UrlModel.is_active.is_(True),

        )

        .first()

    )

    if not url:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Short URL not found",

        )

    url.click_count += 1

    db.commit()

    return RedirectResponse(

        url=url.original_url,

        status_code=status.HTTP_307_TEMPORARY_REDIRECT,

    )

@router.get("/urls/{url_id}/analytics")

def get_analytics(

    url_id: int,

    db: Session = Depends(get_db),

):

    url = (

        db.query(UrlModel)

        .filter(UrlModel.id == url_id)

        .first()

    )

    if not url:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="URL not found",

        )

    return {

        "id": url.id,

        "short_code": url.short_code,

        "original_url": url.original_url,

        "click_count": url.click_count,

        "created_at": url.created_at,

        "is_active": url.is_active,

    }
