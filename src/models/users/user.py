import uuid

from src.common.database import Database
import src.models.users.errors as UserErrors
from src.common.utils import Utils
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email/password combo as sent
        by the site forms is valid.
        Checks that the email exists, and that password associated
        with that email is correct
        :param email: The user's email
        :param password: a sha512 hashed password
        :return: True if valid, false oteherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email}) #password in sha512 -> pbkdf2_sha512
        if user_data is None:
            #Tell user their email doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("You password was wrong")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using e-mail and password
        the password already comes hashed as sha-512
        :param email: user's email (might be invalid)
        :param password: sha512 hashed password
        :return: True if registered successfully, or false otherwise
        """
        user_data  = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The email you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("Your email has an invalid format!")


        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)