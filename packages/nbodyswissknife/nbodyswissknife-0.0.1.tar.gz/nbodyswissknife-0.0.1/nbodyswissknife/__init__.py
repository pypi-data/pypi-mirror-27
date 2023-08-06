from . import potential
from . import potential_cpu

class Configuration(object):
    """
    The configuration of the module

    Enable selecting the backend that does the computations
    """
    def __init__(self):
        """
        Constructor
        """
        self.backends = {
            'native': None,
            'cpu': None,
            'numba_cpu': None,
            'numba_gpu': None,
            'gpu': None
        }
        """the dict of supported backends"""

        self._backend = 'native'
        """the current backend in use"""

config_params = Configuration()


def use(backend):

    pass
