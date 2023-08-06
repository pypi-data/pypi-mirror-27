import urllib.request
import os, yaml, git, re

from karamel.exception import PackagesFileNotFound


empty = lambda *args, **kwargs: None


def read_packages_file(packages_file_url):
    try:
        response = urllib.request.urlopen(packages_file_url)
        content = response.read()
    except ValueError:
        try:
            stream = open(packages_file_url, 'r')
            content = stream.read()
            stream.close()
        except:
            raise PackagesFileNotFound(packages_file_url)

    return yaml.safe_load(content)


def get_package_install_dir(package_install_dir):
    package_install_dir = os.path.expanduser(package_install_dir)
    if package_install_dir != '' and not os.path.isdir(package_install_dir):
        os.makedirs(package_install_dir)
    return package_install_dir


def get_installed_packages(package_install_dir):
    return os.listdir(package_install_dir)


def search_packages(packages_file_url, pattern):
    packages = read_packages_file(packages_file_url)
    packages_name = list(packages.keys())
    r = re.compile('.*{}.*'.format(pattern))
    packages_matching_pattern = filter(r.match, packages_name)

    packages_found = {}
    for package_name in packages_matching_pattern:
        if package_name in packages:
            packages_found[package_name] = packages[package_name]

    return packages_found


def install_packages(packages_file_url,
                     package_install_dir,
                     packages_to_install,
                     on_package_downloading=empty,
                     on_package_installing=empty,
                     on_package_install_success=empty,
                     on_package_already_installed=empty,
                     on_package_not_found=empty,
                     on_package_bad_version_provided=empty):

    packages = read_packages_file(packages_file_url)
    installed_packages = get_installed_packages(package_install_dir)

    for package_name in packages_to_install:

        # TODO verify package_name with regex

        version_requested = None
        if '==' in package_name:
            package_name, version_requested = package_name.split('==')

        if package_name in packages:
            package = packages[package_name]
            package_path = os.path.join(package_install_dir, package_name)

            if not package_name in installed_packages:
                on_package_downloading(package_name)
                download_package(package_install_dir, package['url'])
                on_package_installing(package_name)
                on_package_install_success(package_name)
            else:
                on_package_already_installed(package_name, package_path)

            package_version = get_package_version(package_path)
            if version_requested and version_requested != package_version:
                try:
                    change_package_version(package_path, version_requested)
                except BadVersionProvided:
                    on_package_bad_version_provided(package_name, version_requested)

        else:
            on_package_not_found(package_name)


def freeze_packages(package_install_dir, packages_to_freeze=[]):
    packages_installed = get_installed_packages(package_install_dir)
    freeze = {}

    if packages_to_freeze == []:
        packages_to_freeze = packages_installed

    for package in packages_to_freeze:
        if package in packages_installed:
            package_path = os.path.join(package_install_dir, package)
            git_reference = get_package_version(package_path)
            freeze[package] = str(git_reference)
        else:
            freeze[package] = None

    return freeze


def download_package(package_install_dir, url):
    git.Git(package_install_dir).clone(url)


class BadVersionProvided(Exception):
    pass


def change_package_version(package_path, package_version):
    try:
        repo_git = git.Repo(package_path).git
        repo_git.checkout(package_version)
    except git.exc.GitCommandError as e:
        raise BadVersionProvided()


def get_package_version(package_path):
    repo = git.Repo(package_path)
    version = repo.head.commit

    current_tag = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)
    if current_tag: version = current_tag

    try: version = repo.head.ref
    except: pass

    return version
