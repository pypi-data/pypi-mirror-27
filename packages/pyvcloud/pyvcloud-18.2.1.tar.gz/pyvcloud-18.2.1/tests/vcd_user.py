import unittest
import string
import random

from pyvcloud.vcd.org import Org
from pyvcloud.vcd.test import TestCase

class TestUser(TestCase):
    def create_user(self, user_name):
        logged_in_org = self.client.get_org()
        org = Org(self.client, resource=logged_in_org, is_admin=False)
        role = org.get_role(self.config['vcd']['role_name'])
        role_href = role.get('href')
        return org.create_user(user_name, "password", role_href, "Full Name",
            "Description", "xyz@mail.com", "408-487-9087",
            "test_user_im", "xyz@mail.com", "Alert Vcd:",
            is_enabled=True)

    def delete_user(self, user_name):
        logged_in_org = self.client.get_org()
        org = Org(self.client, resource=logged_in_org, is_admin=False)
        result = org.delete_user(user_name)
        print(result)

    def test_create_and_delete_user(self):
        user_name = self.config['vcd']['user_name'].join(
            random.sample(string.ascii_lowercase, 8))
        user = self.create_user(user_name)
        assert user_name == user.get('name')
        self.delete_user(user_name)

if __name__ == '__main__':
    unittest.main()
