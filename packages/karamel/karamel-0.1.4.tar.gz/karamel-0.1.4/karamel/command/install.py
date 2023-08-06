import os, re, git

from karamel.packages import read_packages_file
from karamel.exception import KaramelException
from karamel.logger import logger

from .command import Command

__command__ = 'install'
__description__ = 'Install a package'

class InstallCommand(Command):

    def __init__(self, packages_file_url, package_install_dir):
        super().__init__(__command__, __description__)
        self.add_argument('package')
        self.packages_file_url = packages_file_url
        self.package_install_dir = os.path.expanduser(package_install_dir)

    def callback(self, args):
        packages = read_packages_file(self.packages_file_url)

        if self.package_install_dir != '' and not os.path.isdir(self.package_install_dir):
            os.makedirs(self.package_install_dir)

        if args.package in packages:
            package = packages[args.package]
            package_path = os.path.join(self.package_install_dir, args.package)

            if not os.path.isdir(package_path):
                logger.info('Downloading {}'.format(args.package))
                git.Git(self.package_install_dir).clone(package['url'])
                logger.info('Installing {}'.format(args.package))
                logger.info('Successfully installed {}'.format(args.package))
            else:
                raise KaramelException('Package already installed: {} in {}'.format(args.package, package_path))

        else:
            raise KaramelException('Package not found')
