from .models import User

class UserDAO:
    """
    Data Access Object (DAO) for User model.
    This class handles all database operations related to the User model.
    """

    @staticmethod
    def get_by_email(email: str) -> User:
        """
        Retrieve a user by email.
        :param email: The email of the user to retrieve.
        :return: User object if found, None otherwise.
        """
        return User.objects.filter(email=email).first()

        
    @staticmethod
    def get_by_id(user_id: str) -> User:
        """
        Retrieve a user by ID.
        :param user_id: The ID of the user to retrieve.
        :return: User object if found, None otherwise.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
    @staticmethod
    def create_user(email: str, password_hash: str) -> User:
        """
        Create a new user.
        :param email: The email of the new user.
        :param password: The password of the new user.
        :return: The created User object.
        """
        user = User(email=email, password=password_hash)
        user.save()
        return user