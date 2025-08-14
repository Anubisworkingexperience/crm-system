from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.auth.hashing import hash_password, verify_password

class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, password: str) -> User:
        u = User(email=email, password_hash=hash_password(password))
        self.session.add(u)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("email_already_registered")
        await self.session.refresh(u)
        return u

    async def get_by_email(self, email: str) -> User | None:
        res = await self.session.execute(select(User).where(User.email == email))
        return res.scalars().first()

    async def verify_credentials(self, email: str, password: str) -> User | None:
        u = await self.get_by_email(email)
        if not u:
            return None
        return u if verify_password(password, u.password_hash) else None
