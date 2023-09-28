import hmac
from starter_code.models.user import UserModel


def authenicate(username, password):
    """
    Function that gets called when a user calls the /auth endpoint
    with username and password
    :param username: username in string format
    :param password: user's un-encrypted password in string format
    :return: A userModel object if authentication was successful none otherwise
    """
    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT
    verified their authorization header is correct
    :param payload: A dictionary with 'identity' key which is user id.
    :return: A userModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
