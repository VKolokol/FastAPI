from fastapi import HTTPException, status
from core.security import verify_password


class Authentication:

    error = HTTPException

    def active_user(self, user):
        if not user.is_active:
            raise self.error(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user!")
        return True

    def verification(self, password, user):
        if not verify_password(password, user.hash_password):
            raise self.error(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect email or password')

    def login_user(self, user, password):
        self.active_user(user=user)
        self.verification(password=password, user=user)
