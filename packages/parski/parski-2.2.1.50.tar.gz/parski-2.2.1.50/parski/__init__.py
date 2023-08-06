"""package for getting and filtering api/file data"""

from parski.get_data import get_data
from parski.filter_data import filter_data

#remove variables from global namespace
del utils

#try __all__ for declaring submodules