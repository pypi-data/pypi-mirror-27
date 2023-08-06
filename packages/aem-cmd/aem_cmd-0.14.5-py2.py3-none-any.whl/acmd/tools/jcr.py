# coding: utf-8
import json
import optparse
import os
import sys

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from acmd import OK, SERVER_ERROR, USER_ERROR
from acmd import tool, log, error
from acmd.util.props import parse_properties, format_multipart

parser = optparse.OptionParser("acmd <ls|cat|find|mv|setprop|rmprop> [options] <jcr path>")
parser.add_option("-r", "--raw",
                  action="store_const", const=True, dest="raw",
                  help="output raw response data")
parser.add_option("-f", "--fullpath",
                  action="store_const", const=True, dest="full_path",
                  help="output full paths instead of local")


@tool('ls')
class ListTool(object):
    """ Since jcr operations are considered so common we extract what would otherwise be
        a jcr tool into separate smaller tools for ease of use.
    """

    @staticmethod
    def execute(server, argv):
        options, args = parser.parse_args(argv)
        log("Done {}".format(len(args)))
        if len(args) >= 2:
            path = args[1]
            log("Listing {}".format(path))
            return list_node(server, options, path)
        else:
            ret = OK

            for path in sys.stdin:
                log("Listing subpath {}".format(path))
                ret = ret | list_node(server, options, path.strip())
            return ret


def list_node(server, options, path):
    data = _get_subnodes(server, path)
    if options.raw:
        sys.stdout.write("{}\n".format(json.dumps(data, indent=4)))
    else:
        _list_nodes(path, data, full_path=options.full_path)
    return OK


def _list_nodes(path, nodes, full_path=False):
    for path_segment, data in nodes.items():
        if not is_property(path_segment, data):
            _list_node(path, path_segment, full_path)


def _list_node(path, path_segment, full_path=False):
    if full_path:
        full_path = os.path.join(path, path_segment)
        _list_path(full_path)
    else:
        _list_path(path_segment)


def _list_path(path):
    sys.stdout.write("{path}\n".format(path=path))


@tool('cat')
class InspectTool(object):

    @staticmethod
    def execute(server, argv):
        options, args = parser.parse_args(argv)
        if len(args) >= 2:
            path = args[1]
            return cat_node(server, options, path)
        else:
            ret = OK
            for line in sys.stdin:
                ret = ret | cat_node(server, options, line.strip())
            return ret


def cat_node(server, options, path):
    url = server.url("{path}.1.json".format(path=path))
    resp = requests.get(url, auth=server.auth)
    if resp.status_code != 200:
        sys.stderr.write("error: Failed to get path {}, request returned {}\n".format(path, resp.status_code))
        return SERVER_ERROR
    data = json.loads(resp.content)
    if options.raw:
        sys.stdout.write("{}\n".format(json.dumps(data, indent=4)))
    else:
        for prop, data in data.items():
            if is_property(prop, data):
                sys.stdout.write("{key}:\t{value}\n".format(key=prop, value=data))
    return OK


@tool('find')
class FindTool(object):

    @staticmethod
    def execute(server, argv):
        options, args = parser.parse_args(argv)

        try:
            if len(args) >= 2:
                path = args[1]
                return list_tree(server, options, path)
            else:
                ret = OK
                for line in sys.stdin:
                    ret = ret | list_tree(server, options, line.strip())
                return ret
        except KeyboardInterrupt:
            return USER_ERROR


def list_tree(server, options, path):
    _list_path(path)
    nodes = _get_subnodes(server, path)
    for path_segment, data in nodes.items():
        if not is_property(path_segment, data):
            list_tree(server, options, os.path.join(path, path_segment))
    return OK


def _get_subnodes(server, path):
    url = server.url("{path}.1.json".format(path=path))

    log("GETting service {}".format(url))
    resp = requests.get(url, auth=server.auth)

    if resp.status_code != 200:
        sys.stderr.write("error: Failed to get path {}, request returned {}\n".format(path, resp.status_code))
        sys.exit(-1)

    return json.loads(resp.content)


def is_property(_, data):
    return not isinstance(data, dict)


@tool('rm')
class RmTool(object):
    """ curl -X DELETE http://localhost:4505/path/to/node/jcr:content/nodeName -u admin:admin
    """

    @staticmethod
    def execute(server, argv):
        options, args = parser.parse_args(argv)
        if len(args) >= 2:
            path = args[1]
            return rm_node(server, options, path)
        else:
            for line in sys.stdin:
                path = line.strip()
                rm_node(server, options, path)
        return OK


def rm_node(server, options, path):
    url = server.url(path)
    resp = requests.delete(url, auth=server.auth)
    if resp.status_code != 204:
        sys.stderr.write("error: Failed to delete path {}, request returned {}\n".format(path, resp.status_code))
        return SERVER_ERROR
    if options.raw:
        sys.stdout.write("{}\n".format(resp.content))
    else:
        sys.stdout.write("{}\n".format(path))
    return OK


@tool('setprop')
class SetPropertyTool(object):
    """ curl -u admin:admin -X POST --data test=sample
            http://localhost:4502/content/geometrixx/en/toolbar/jcr:content
    """

    @staticmethod
    def execute(server, argv):
        options, args = parser.parse_args(argv)
        props = parse_properties(args[1])
        if len(args) >= 3:
            path = args[2]
            return set_node_properties(server, options, path, props)
        else:
            for line in sys.stdin:
                path = line.strip()
                set_node_properties(server, options, path, props)
            return OK


def set_node_properties(server, options, path, props):
    """ curl -u admin:admin -X POST --data test=sample
            http://localhost:4502/content/geometrixx/en/toolbar/jcr:content
    """
    url = server.url(path)

    multipart_data = MultipartEncoder(
        fields=format_multipart(props)
    )
    resp = requests.post(url, auth=server.auth, data=multipart_data,
                         headers={'Content-Type': multipart_data.content_type})

    if resp.status_code != 200:
        sys.stderr.write(
            "error: Failed to set property on path {}, request returned {}\n".format(path, resp.status_code))
        return SERVER_ERROR
    if options.raw:
        sys.stdout.write("{}\n".format(resp.content))
    else:
        sys.stdout.write("{}\n".format(path))
    return OK


@tool('rmprop')
class DeletePropertyTool(object):
    """ curl -u admin:admin -X POST --data test@Delete=
            http://localhost:4502/content/geometrixx/en/toolbar/jcr:content
    """

    @staticmethod
    def execute(server, argv):
        options, args = parser.parse_args(argv)
        if len(args) <= 1:
            parser.print_help()
            return USER_ERROR
        prop_names = args[1].split(',')
        if len(args) >= 3:
            path = args[2]
            return rm_node_properties(server, options, prop_names, path)
        else:
            ret = OK
            for line in sys.stdin:
                path = line.strip()
                ret = ret | rm_node_properties(server, options, prop_names, path)
            return ret


def rm_node_properties(server, options, prop_names, path):
    props = {k + '@Delete': '' for k in prop_names}

    url = server.url(path)
    resp = requests.post(url, auth=server.auth, data=props)
    if resp.status_code != 200:
        sys.stderr.write(
            "error: Failed to set property on path {}, request returned {}\n".format(path, resp.status_code))
        return SERVER_ERROR
    if options.raw:
        sys.stdout.write("{}\n".format(resp.content))
    else:
        sys.stdout.write("{}\n".format(path))
    return OK


@tool('cp')
class CopyTool(object):
    @staticmethod
    def execute(server, argv):
        parser.set_usage("%prog cp <src-path> <dst-path>")
        options, args = parser.parse_args(argv)
        if len(args) < 3:
            parser.print_help()
            return USER_ERROR
        src_path = args[1]
        dst_path = args[2]
        data = {":operation": "copy", ":dest": dst_path}

        url = server.url(src_path)
        resp = requests.post(url, auth=server.auth, data=data)
        if resp.status_code != 200 and resp.status_code != 201:
            error("Failed to copy, request returned {}".format(resp.status_code))
            if options.raw:
                error(resp.content)
            return SERVER_ERROR

        msg = _result_folder(src_path, dst_path) if not options.raw else resp.content
        sys.stdout.write("{}\n".format(msg))
        return OK


@tool('mv')
class MoveTool(object):
    @staticmethod
    def execute(server, argv):
        options, args = parser.parse_args(argv)
        if len(args) < 3:
            parser.print_help()
            return USER_ERROR

        src_path = args[1]
        dst_path = args[2]

        data = {":operation": "move", ":dest": dst_path}

        url = server.url(src_path)
        resp = requests.post(url, auth=server.auth, data=data)
        if resp.status_code != 200 and resp.status_code != 201:
            error("Failed to copy, request returned {}".format(resp.status_code))
            if options.raw:
                error(resp.content)
            return SERVER_ERROR

        msg = _result_folder(src_path, dst_path) if not options.raw else resp.content
        sys.stdout.write("{}\n".format(msg))
        return OK


def _result_folder(src_path, dst_path):
    if dst_path.endswith('/'):
        last = src_path.split('/')[-1]
        return dst_path + last
    else:
        return dst_path
