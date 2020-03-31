class unable_to_open_session_exception(Exception):
    """Exception raised when it is impossible to open a session."""
    pass

class wrong_password(Exception):
    """Exception raised for errors in the input of the password."""
    pass

class user_doesnt_exist(Exception):
    """Exception raised when the user doesn't exist."""
    pass

class invalid_parameter(Exception):
    """Exception raised when entered an invalid parameter."""
    pass

class account_name_already_exist(Exception):
    """Exception raised when the account name already exist."""
    pass

class account_doesnt_exist(Exception):
    """Exception raised when the account doesn't exist."""
    pass