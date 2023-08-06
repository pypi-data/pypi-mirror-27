import urllib.request
import yaml

from karamel.exception import PackagesFileNotFound

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
