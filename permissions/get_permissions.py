from fastapi import HTTPException, status


class Permissions:
    error = HTTPException

    def get_object(self, obj):
        if obj is None:
            raise self.error(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
        return True

    def get_superuser(self, user, user_id):
        if not user.is_stuff:
            self.get_user_permission(user, user_id)
        return True

    def get_user_permission(self, user, user_id):
        if user.id != user_id:
            raise self.error(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied!")
        return True

    def get_permission(self, obj, user, user_id):
        assert self.get_object(obj)
        assert self.get_superuser(user, user_id)
