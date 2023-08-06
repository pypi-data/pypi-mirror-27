import json
import datetime
from datetime import timedelta
from werkzeug.wrappers import Request, BaseResponse
from obscure_api.crypto import AESCipher
from anytree import Node, PostOrderIter
import importlib
import types
import re
from jose import jwt
import jose.exceptions
from werkzeug import exceptions

class Server(object):
    jwt_secret = ""
    root_nodes = []
    services = {}
    controller_nodes = {}
    controller_nodes_by_class = {}
    leafs = {}

    def __init__(self, key="1234567891234567", jwt_secret="123456qwerty"):
        self.cipher = AESCipher(key)
        Server.jwt_secret = jwt_secret
        for key, value in self.controller_nodes.items():
            if "parent" in value.data:
                value.parent = self.controller_nodes[value.data["parent"]]
            else:
                self.root_nodes.append(value)

        for class_name, elements in self.leafs.items():
            for leaf in elements:
                Node(leaf["path"], parent=self.controller_nodes_by_class[class_name], data=leaf)

        for root in self.root_nodes:
            for i in PostOrderIter(root):
                if "callable" in i.data:
                    path = "/" + "/".join([str(node.data["path"]) for node in i.path])
                    print(path)
                    self.services[path] = i.data["callable"]

        self.parser = UrlMatcher(self.services)



    def run(self, host="0.0.0.0", port=4000):
        from werkzeug.serving import run_simple
        run_simple(host, port, self.application)

    @Request.application
    def application(self, request):

        # if there are headers into headers is because it is a hidden request
        cipher_output = False
        if "Headers" in request.headers:
            cipher_output = True
            # Hidden request
            hidden_headers = json.loads(self.cipher.decrypt(request.headers["Headers"]))
            # _c is creation date
            request_age = datetime.datetime.now() - datetime.datetime.strptime(hidden_headers["_c"], "%Y-%m-%dT%H:%M:%S")
            # _d is duration while the request is valid
            d = timedelta(seconds=hidden_headers["_d"])

            # _m is the method type
            if "_m" in hidden_headers:
                request.method = hidden_headers["_m"]

            if request_age <= d:
                request.path = self.cipher.decrypt(request.path[1:])
                request.headers = hidden_headers
                if len(request.data) > 0:
                    request.data = self.cipher.decrypt(request.data)
            else:
                return BaseResponse(self.cipher.encrypt("400Request expired"))

        method_data = self.parser.match(request.path)

        if method_data is not None:
            # Dynamically load the method by name
            o = self.services[method_data["url"]]
            namespace = o.__qualname__.replace("."+o.__name__, "")
            m = importlib.import_module(o.__module__)

            #TODO storage instances in a cache
            controller = getattr(m, namespace)()
            method = getattr(controller, o.__name__)

            try:
                data_res = method(request=request, **method_data["params"])

                if cipher_output:
                    data_res = self.cipher.encrypt("200" + str(data_res))
                return BaseResponse(data_res)
            except Exception as e:
                #raise e
                if cipher_output:
                    data_res = self.cipher.encrypt("400" + str(e))
                else:
                    data_res = str(e)
                return BaseResponse(data_res, status=400)
        else:
            if cipher_output:
                return BaseResponse(self.cipher.encrypt("404Not found"))
            else:
                return BaseResponse("Not found", status=404)


class url(object):
    def __init__(self, **kwargs):
        self.path = kwargs["path"]
        if "name" in kwargs:
            self.name = kwargs["name"]
        else:
            self.name = None
        if "parent" in kwargs:
            self.parent = kwargs["parent"]
        else:
            self.parent = None
        self.kwargs = kwargs
        # print(kwargs)

    def __call__(self, f, *args, **kwargs):

        if isinstance(f, types.FunctionType):
            if "parent" in self.kwargs:
                raise Exception("Parent cannot be set in a method")

            n = f.__qualname__.split(".")[0]
            if n not in Server.leafs:
                Server.leafs[n] = []
            self.kwargs["callable"] = f
            Server.leafs[n].append(self.kwargs)

        else:

            self.kwargs.update({"class": f.__name__})
            Server.controller_nodes[self.name] = Node(self.name, data=self.kwargs)
            Server.controller_nodes_by_class[f.__name__] = Server.controller_nodes[self.name]
        return f

class secure(object):
    def __init__(self, **kwargs):
        self.entities = kwargs

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            request = kwargs["request"]
            auth = request.headers.get('Authorization')
            if auth is None or not auth.startswith("Bearer"):
                raise exceptions.BadRequest('Permission denied')

            try:
                token = auth.split(" ")[1]
                jwt.decode(token, Server.jwt_secret, algorithms=['HS256'])
            except jose.exceptions.JWTError as e:
                print(e)
                raise exceptions.BadRequest('Permission denied')
            return f(*args, **kwargs)
            #return f(*args, **kwargs)

        return wrapped_f


class UrlMatcher(object):
    def __init__(self, urls):
        self.urls = urls
        self.reurls = {}
        for url in self.urls:
            m = re.findall('(<[a-zA-Z_0-9]+>)', url)
            final_reg = url
            for url_var in m:
                final_reg = re.sub(url_var, "(?P" + url_var + "[a-zA-Z_0-9]+)", final_reg)
            self.reurls[url] = "^" + final_reg + "$"

    def match(self, url):
        for orig_url, regexp in self.reurls.items():
            matched = re.match(regexp, url)
            if matched is not None:
                return {"url": orig_url, "params": matched.groupdict()}

        return None

# Guadrar esto para tests
# def usuarios_simple(user_id):
#     print("SOY EL USER ID " + user_id)
#
# def usuarios_mindundi(user_id, mindundi):
#     print("SOY EL USER ID " + user_id + " y un mindundi " + mindundi)
#
#
# def admin(admin_id):
#     print("SOY EL ADMIN ID " + admin_id)
#
# def index():
#     print("SOY EL USER INDEX")
'''
urls = {
    '/usuarios/<user_id>': usuarios_simple,
    '/usuarios/<user_id>/cosa/<mindundi>': usuarios_mindundi,
    '/admin/<user_id>/post': admin,
    '/index': index
}

reurls = {}

for url in urls:
    m = re.findall('(<[a-zA-Z_0-9]+>)', url)
    final_reg = url
    for url_var in m:
        final_reg = re.sub(url_var, "(?P" + url_var + "[a-zA-Z_0-9]+)", final_reg)
    reurls[url] = "^"+final_reg+"$"


found = False
for orig_url, regexp in reurls.items():
    matched = re.match(regexp, ex_url)
    if matched is not None:
        print("a")
        urls[orig_url](**matched.groupdict())
        found = True
        break

if not found:
    print("Not found")

#print(m)
'''
