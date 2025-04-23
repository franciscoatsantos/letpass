from vault.models import PasswordEntry

class PasswordEntryDAO:

    """
    Data Access Object (DAO) for PasswordEntry model.
    This class handles all database operations related to the PasswordEntry model.
    """

    @staticmethod
    def get_list(user_id: str) -> list[PasswordEntry]:
        """
        Retrieve a list of password entries for a given user.
        :param user_id: The ID of the user whose password entries to retrieve.
        :return: List of PasswordEntry objects.
        """
        return PasswordEntry.objects.filter(user_id=user_id).order_by('-created_at')
    
    @staticmethod
    def get_by_id(entry_id: str) -> PasswordEntry:
        """
        Retrieve a password entry by ID.
        :param entry_id: The ID of the password entry to retrieve.
        :return: PasswordEntry object if found, None otherwise.
        """
        try:
            return PasswordEntry.objects.get(id=entry_id)
        except PasswordEntry.DoesNotExist:
            return None
        
    @staticmethod
    def create_entry(user_id: str, title: str, encrypted_data: str) -> PasswordEntry:
        """
        Create a new password entry.
        :param user_id: The ID of the user creating the entry.
        :param title: The title of the password entry.
        :param encrypted_data: The encrypted password data.
        :return: The created PasswordEntry object.
        """
        entry = PasswordEntry(user_id=user_id, title=title, encrypted_data=encrypted_data)
        entry.save()
        return entry