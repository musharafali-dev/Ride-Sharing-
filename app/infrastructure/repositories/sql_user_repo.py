import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.repositories.user_repo import UserRepository
from app.infrastructure.database.models.user_model import UserModel

class SQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def save(self, user: User) -> None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()

        if not model:
            model = UserModel(
                id=user.id,
                email=user.email.value,
                hashed_password=user.hashed_password,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self.session.add(model)
        else:
            model.email = user.email.value
            model.hashed_password = user.hashed_password
            model.full_name = user.full_name
            model.role = user.role
            model.is_active = user.is_active
            model.is_verified = user.is_verified
            model.updated_at = user.updated_at

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=Email(model.email),
            full_name=model.full_name,
            role=model.role,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
