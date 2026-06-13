"""
Data modules for inflect: re-export all data for convenience.
"""

from .numbers import *  # noqa: F401 F403
from .articles import *  # noqa: F401 F403
from .pronouns import *  # noqa: F401 F403
from .plurals import *  # noqa: F401 F403
from .singulars import _init as _init_singulars

# Initialize derived singular data
_init_singulars()

from .singulars import *  # noqa: F401 F403
