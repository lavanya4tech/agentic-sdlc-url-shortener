from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from .database import Base

class UrlModel(Base):

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)

    original_url = Column(

        String(2048),

        nullable=False,

    )

    short_code = Column(

        String(20),

        unique=True,

        nullable=False,

        index=True,

    )

    click_count = Column(

        Integer,

        default=0,

        nullable=False,

    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow,

        nullable=False,

    )

    is_active = Column(

        Boolean,

        default=True,

        nullable=False,

    )

