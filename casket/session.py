import casket

class session:

    def __init__(
        self,
        method,
        username,
        email = "user@example.com",
        password_master = "casket",
        algorithm = "sha256"
        ):

        self.username = username
        self.email = email
        self.password_master = password_master
        self.algorithm = algorithm

        if not casket.home.home_folder_exist():
            casket.home.make_folders()

        if method == "new":
            casket.home.make_user_folder(self)
        elif method == "load":
            if casket.home.check_user_exist(username):
                pass # query
            else:
                raise exception()
