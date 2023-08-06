__version__ = '0.1'

try:
    from .code import PearsonDictionary
except ImportError:
    from code import PearsonDictionary