from sqlobject import *

from turbogears import identity 
from turbogears.database import PackageHub

hub = PackageHub("aventura")
__connection__ = hub


# class YourDataClass(SQLObject):
#     pass


