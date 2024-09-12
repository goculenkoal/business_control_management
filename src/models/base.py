from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

dt_now_utc_sql = text("TIMEZONE('utc', now())")


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=dt_now_utc_sql)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=dt_now_utc_sql,
        onupdate=dt_now_utc_sql,
    )


class BaseModelCompany(DeclarativeBase):
    pass
