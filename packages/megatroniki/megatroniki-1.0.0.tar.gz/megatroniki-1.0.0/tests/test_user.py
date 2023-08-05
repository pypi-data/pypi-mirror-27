from unittest import TestCase
from wiki.web.user import UserManager
import os


class UserTestCase(TestCase):
    """
        Tests User Class and UserManager class
    """

    def test_new_json_file(self):
        """
            Tests creating a new json file, and tries to create a new file when one is already made
        """
        um = UserManager("")

        um = UserManager("")

    def test_user_read_write_json(self):
        """
            Tests reading and writing back a json users file
        """
        um = UserManager("")
        json = um.read()

        assert json is not None

        um.write(json)

        assert um.read() is not None

    def test_user_creation_cleartext(self):
        """
            Tests creation of a user using UserManager
        """
        username = "clear name"
        password = "clear pass"
        um = UserManager("")

        cleartext_user = um.add_user(username, password, True, ["admin"], "cleartext")

        assert cleartext_user is not None

    def test_same_name(self):
        """
            Tests whether you can create two users with the same name
        """
        username = "clear name"
        password = "clear pass"
        um = UserManager("")

        cleartext_user = um.add_user(username, password, True, ["admin"], "cleartext")


        assert cleartext_user is not None

    def test_not_implemented_auth(self):
        """
            Tests the encryption scheme not implemented exception
        """
        username = "none name"
        password = "none pass"
        um = UserManager("")

        is_caught = False

        try:
            um.add_user(username, password, True, ["admin"], "asdf")
        except NotImplementedError:
            is_caught = True

        assert is_caught is True

    def test_user_creation_hash(self):
        """
            Tests creating a user with hashed password
        """
        # print(os.getcwd())

        username = "hash name"
        password = "hash pass"
        um = UserManager("")

        hash_user = um.add_user(username, password, True, ["admin"], "hash")

        assert hash_user is not None

    def test_user_get(self):
        """
            Tests creating a user with cleartext password
        """
        username = "get name"
        password = "get pass"
        um = UserManager("")

        cleartext_user = um.add_user(username, password, True, ["admin"], "cleartext")

        assert um.get_user(username) is not None

    def test_user_delete(self):
        """
            Tests deleting a user
        """
        username = "delete name"
        password = "delete pass"
        um = UserManager("")

        cleartext_user = um.add_user(username, password, True, ["admin"], "cleartext")

        assert um.get_user(username) is not None

        um.delete_user(username)

        assert um.get_user(username) is None

        assert um.delete_user("user never has been created") is False

    def test_user_update(self):
        """
        Tests updating a user
        """
        username = "update name"
        password = "update pass"
        um = UserManager("")

        cleartext_user = um.add_user(username, password, True, ["admin"], "cleartext")

        data = cleartext_user.data

        um.update(username, data)

    def test_simple_user(self):
        """
            Assert a simple User is created correctly.
        """
        name = 'Hash'
        password = 'password'
        active = True
        roles = ['Admin']
        authentication_method = 'hash'
        user_manager = UserManager('')
        hash_user = user_manager.add_user(name, password, active, roles, authentication_method)

        assert hash_user.is_active()

        assert hash_user.is_authenticated() is False

        hash_user.set('authenticated', True)
        assert hash_user.get('authenticated')

        assert hash_user.get_id() == name

        assert hash_user.is_anonymous() is True

        assert hash_user.check_password(password)

        name2 = 'Test2'
        authentication_method2 = 'cleartext'
        clear_user = user_manager.add_user(name2, password, active, roles, authentication_method2)
        assert clear_user.check_password(password)

        assert hash_user.check_password('hi') is False

        hash_user.set('authentication_method', 'hi')
        is_caught = False
        try:
            hash_user.check_password('hi')
        except NotImplementedError:
            is_caught = True
        assert is_caught

    def tearDown(self):
        try:
            os.remove("users.json")
        except:
            None




