import os
import sys

sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/../")

from dotenv import load_dotenv
load_dotenv('.env.local')

import unittest

from utils.notifications.enums import Agent
import Environment as env

class Test(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
    

if __name__ == '__main__':
    unittest.main()