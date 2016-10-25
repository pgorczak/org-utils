import os
import unittest

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    unittest.TextTestRunner().run(unittest.TestLoader().discover(path))
