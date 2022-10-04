# -*- coding: utf-8 -*-
"""
The initialization of the logging module is intentionaly done here in the
_logging.py module so that it will be initialized before any other of our
python-gitlab modules are loaded. So if they do logging upon being loaded it
will allow them to do it safely.
"""

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from typing import List

__all__: List[str] = []

# Using the `NullHandler` means that any log messages generated will not be
# output unless the client application configures logging. For example by
# calling `logging.basicConfig()`
_module_root_logger_name = __name__.split(".", maxsplit=1)[0]
logging.getLogger(_module_root_logger_name).addHandler(logging.NullHandler())
