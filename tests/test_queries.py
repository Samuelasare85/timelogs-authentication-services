import unittest
from src.resolvers import user_resolvers

class TestUserQueries(unittest.TestCase):
    # def test_resolve_me(self):
    #     pass
        
    def test_resolve_user(self):
        id = 2
        self.assertEqual(user_resolvers.resolve_user(id),{})