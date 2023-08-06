# coding: utf-8
import optparse
import os
import sys
import tempfile
import json

from xml.etree import ElementTree
from distutils.version import LooseVersion


import requests


from acmd import tool, error, log
from acmd import OK, USER_ERROR, SERVER_ERROR
from acmd.tools import get_action, get_argument


SERVICE_PATH = '/crx/packmgr/service.jsp'

parser = optparse.OptionParser("acmd packages [options] [list|build|install|upload|download|promote] \
    [<zip>|<package>|<server>]")
parser.add_option("-v", "--version",
                  dest="version", help="specify explicit version")
parser.add_option("-g", "--group",
                  dest="group", help="specify explicit group")
parser.add_option("-r", "--raw",
                  action="store_const", const=True, dest="raw",
                  help="output raw response data")
parser.add_option("-c", "--compact",
                  action="store_const", const=True, dest="compact",
                  help="output only package name")
parser.add_option("-i", "--install",
                  action="store_const", const=True, dest="install",
                  help="install package after upload")
parser.add_option("-t", "--target",
                  dest="target_server", help="specify target server")


@tool('package', ['list', 'build', 'install', 'uninstall', 'download', 'upload'])
class PackageTool(object):
    def __init__(self):
        self.config = None

    def execute(self, server, argv):
        options, args = parser.parse_args(argv)

        action = get_action(args, default='list')
        actionarg = get_argument(args)

        if action == 'list' or action == 'ls':
            return list_packages(server, options)
        elif actionarg is None:
            parser.print_help()
            return USER_ERROR
        elif action == 'build':
            return build_package(server, options, actionarg)
        elif action == 'install':
            return install_package(server, options, actionarg)
        elif action == 'uninstall':
            return uninstall_package(server, options, actionarg)
        elif action == 'download':
            return download_package(server, options, actionarg)
        elif action == 'upload':
            return upload_package(server, options, actionarg)
        elif action == 'promote':
            target_server_name = options.target_server
            if target_server_name is None:
                error("Missing target server, use -t flag.")
                return USER_ERROR
            target_server = self.config.get_server(target_server_name)
            return promote_package(server, target_server, options, actionarg)
        else:
            sys.stderr.write('error: Unknown package action {a}\n'.format(a=action))
            return USER_ERROR


def make_packages_request(server):
    url = server.url(SERVICE_PATH)
    form_data = {'cmd': (None, 'ls')}
    resp = requests.post(url, auth=(server.username, server.password), files=form_data)
    if resp.status_code != 200:
        raise Exception("Failed to get " + url)
    return resp.content


def get_packages_list(server):
    content = make_packages_request(server)
    tree = ElementTree.fromstring(content)
    return parse_packages(tree)


def list_packages(server, options):
    content = make_packages_request(server)

    if options.raw:
        sys.stdout.write(content)
    else:
        tree = ElementTree.fromstring(content)
        packages = parse_packages(tree)
        for pkg in packages:
            if options.compact:
                msg = "{pkg}".format(pkg=pkg['name'])
            else:
                msg = format_package(pkg)
            sys.stdout.write("{}\n".format(msg))
    return OK


def format_package(pkg):
    return "{g}\t{pkg}\t{v}\t{u}".format(g=pkg['group'], pkg=pkg['name'], v=pkg['version'], u=pkg['lastUnpacked'])


def parse_packages(tree):
    pkg_elems = tree.find('response').find('data').find('packages').findall('package')
    packages = [parse_package(elem) for elem in pkg_elems]
    return packages


def parse_package(elem):
    ret = dict()
    for sub in elem.getchildren():
        ret[sub.tag] = sub.text
    return ret


def get_latest_version(packages):
    ret = None
    highest_version = LooseVersion("0.0")
    for pkg in packages:
        version = LooseVersion(pkg['version'])
        if version > highest_version:
            ret = pkg
    return ret


def get_group(options, pkg):
    if options.group is not None:
        return options.group
    else:
        return pkg['group']


def _get_package(package_name, server, options):
    packages = get_packages_list(server)
    packages = list(filter(lambda x: x['name'] == package_name, packages))
    if len(packages) == 0:
        raise Exception('No package named {} found'.format(package_name))

    pkg = get_latest_version(packages)
    if options.version is None:
        version = pkg['version']
    else:
        version = options.version

    zipfile = pkg['name'] + _zip_suffix(version)
    group = get_group(options, pkg)
    return group, zipfile


def _zip_suffix(version):
    if version is None:
        return '.zip'
    else:
        return '-' + str(version) + '.zip'


def download_package(server, options, package_name, filename=None):
    group, zipfile = _get_package(package_name, server, options)

    path = '/etc/packages/{group}/{zip}'.format(group=group, zip=zipfile)
    url = server.url(path)
    response = requests.get(url, auth=(server.username, server.password))

    if filename is None:
        filename = zipfile
    with open(filename, 'wb') as f:
        if response.status_code == 200:
            f.write(response.content.encode('utf-8'))
            sys.stdout.write("{}\n".format(zipfile))
            return OK
        else:
            error("Failed to download " + url + " because " + str(response.status_code) + "\n")
            if options.raw:
                sys.stderr.write(response.content)
                sys.stderr.write("\n")
            return SERVER_ERROR


def json_bool(val):
    """ Returns the string 'true' if val is boolean is True """
    if val is True:
        return 'true'
    else:
        return 'false'


def upload_package(server, options, filename):
    """ curl -u admin:admin -F file=@"name of zip file" -F name="name of package"
            -F strict=true -F install=false http://localhost:4505/crx/packmgr/service.jsp """
    form_data = dict(
        file=(filename, open(filename, 'rb'), 'application/zip', dict()),
        name=filename.rstrip('.zip'),
        strict="true",
        install=json_bool(options.install)
    )
    log(form_data)
    url = server.url(SERVICE_PATH)
    log("POSTing to {}".format(url))
    resp = requests.post(url, auth=server.auth, files=form_data)
    log("Got status %s" % str(resp.content))

    if resp.status_code != 200:
        error('Failed to upload paackage: {}: {}'.format(resp.status_code, resp.content))
        if options.raw:
            sys.stdout.write("{}\n".format(resp.content))
        return SERVER_ERROR
    else:
        try:
            tree = ElementTree.fromstring(resp.content)
            pkg_elem = tree.find('response').find('data').find('package')
            pkg = parse_package(pkg_elem)
            sys.stdout.write("{}\n".format(format_package(pkg)))
        except Exception as e:
            sys.stderr.write('error: Failed to parse response: {}\n'.format(e))
            return SERVER_ERROR
    return OK


def get_package_url(package_name, server, options):
    group, zipfile = _get_package(package_name, server, options)
    path = '/crx/packmgr/service/.json/etc/packages/{group}/{zip}'.format(group=group, zip=zipfile)
    return server.url(path)


def install_package(server, options, package_name):
    """ curl -u admin:admin -X POST \
        http://localhost:4505/crx/packmgr/service/.json/etc/packages/export/name of package?cmd=install """
    url = get_package_url(package_name, server, options)
    form_data = dict(cmd='install')

    log("Installing package with POST to {}".format(url))
    resp = requests.post(url, auth=server.auth, data=form_data)
    if resp.status_code != 200:
        error("Failed to install package: {}".format(resp.content))
        return SERVER_ERROR
    data = json.loads(resp.content)
    assert data['success'] is True
    if options.raw:
        sys.stdout.write("{}\n".format(resp.content))
    else:
        sys.stdout.write("{}\n".format(data['msg']))
    return OK


def uninstall_package(server, options, package_name):
    url = get_package_url(package_name, server, options)
    form_data = dict(cmd='uninstall')

    log("Uninstalling package with POST to {}".format(url))
    resp = requests.post(url, auth=server.auth, data=form_data)
    if resp.status_code != 200:
        error("Failed to uninstall package: {}".format(resp.content))
        return SERVER_ERROR
    if options.raw:
        sys.stdout.write("{}\n".format(resp.content))
    return OK


def build_package(server, options, package_name):
    """ curl -u admin:admin -X POST
            http://localhost:4505:/crx/packmgr/service/.json/etc/packages/name_of_package.zip?cmd=build """
    url = get_package_url(package_name, server, options)
    form_data = dict(cmd='build')

    resp = requests.post(url, auth=server.auth, data=form_data)
    if resp.status_code != 200:
        error("Failed to rebuild package: {}".format(resp.content))
        return SERVER_ERROR
    if options.raw:
        sys.stdout.write("{}\n".format(resp.content))
    return OK


def promote_package(server, target_server, options, package_name):
    """ Download package from server, upload to target_server and install. """
    if not package_name:
        error("Missing package name argument")
        return USER_ERROR

    _, tmp_filepath = tempfile.mkstemp(".zip")
    log("Download package from source server {} to {}".format(server, tmp_filepath))
    status = download_package(server, options, package_name, filename=tmp_filepath)
    if status != OK:
        return status

    log("Upload downloaded package file to target server {}".format(target_server))
    status = upload_package(target_server, options, tmp_filepath)
    os.remove(tmp_filepath)
    if status != OK:
        return status

    log("Install uploaded package on target server")
    install_package(target_server, options, package_name)
    return status
