import os, re, git

from karamel.packages import read_packages_file
from karamel.exception import KaramelException
from karamel.logger import logger

from .command import Command

__command__ = 'list'
__description__ = 'List packages'

class ListCommand(Command):

    def __init__(self, packages_file_url, package_install_dir):
        super().__init__(__command__, __description__)
        self.add_argument('--installed', action='store_true')
        self.packages_file_url = packages_file_url
        self.package_install_dir = os.path.expanduser(package_install_dir)

    def callback(self, args):
        packages = read_packages_file(self.packages_file_url)

        if self.package_install_dir != '' and not os.path.isdir(self.package_install_dir):
            os.makedirs(self.package_install_dir)

        if args.installed:
            packages_installed = os.listdir(self.package_install_dir)

            for package_name in packages_installed:
                logger.info('{}'.format(package_name))

        else:
            for package_name, package_info in packages.items():
                logger.info('{}'.format(package_name))
