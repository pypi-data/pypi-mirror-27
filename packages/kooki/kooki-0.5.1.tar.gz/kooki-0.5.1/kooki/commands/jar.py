from kooki.tools import Output
from kooki.jars import get_jars
from .command import Command

__command__ = 'jar'
__description__ = 'List jars'

class JarCommand(Command):

    def __init__(self):
        super(JarCommand, self).__init__(__command__, __description__)

    def callback(self, args):
        pass
