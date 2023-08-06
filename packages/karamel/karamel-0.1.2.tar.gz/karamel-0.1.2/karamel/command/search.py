import re
from termcolor import colored

from karamel.packages import read_packages_file

from .command import Command

__command__ = 'search'
__description__ = 'Search package'

class SearchCommand(Command):

    def __init__(self, packages_file_url):
        super().__init__(__command__, __description__)
        self.add_argument('pattern')
        self.packages_file_url = packages_file_url

    def callback(self, args):
        packages = read_packages_file(self.packages_file_url)
        packages_name = list(packages.keys())
        r = re.compile('.*{}.*'.format(args.pattern))
        packages_matching_pattern = filter(r.match, packages_name)
        for name in packages_matching_pattern:
            package = packages[name]
            print('{}'.format(colored(name, 'white')))
            print('  {}'.format(colored(package['description'], 'yellow')))
            print('  {}'.format(colored(package['url'], 'cyan')))
            print('')
