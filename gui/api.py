"""
   Copyright 2020 Yann Dumont

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__all__ = ("Static", )


from .logger import getLogger
from .configuration import ui_conf
import requests
import falcon


logger = getLogger(__name__.split(".", 1)[-1])


def reqDebugLog(req):
    logger.debug("method='{}' path='{}' content_type='{}' parameters={}".format(req.method, req.path, req.content_type, req.params))


def reqErrorLog(req, ex):
    logger.error("method='{}' path='{}' - {}".format(req.method, req.path, ex))


class Static:
    def __init__(self, location):
        self.__location = location

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        raise falcon.HTTPPermanentRedirect(self.__location)


class Router:
    __srv_map = {
        "module-management": ui_conf.Internal.mm,
        "deployment-management": ui_conf.Internal.dm,
        "configuration-storage": ui_conf.Internal.cs,
        "monitoring": ui_conf.Internal.m
    }

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, service, api, resource=None):
        reqDebugLog(req)
        try:
            if service not in self.__srv_map:
                raise RuntimeError(falcon.HTTP_404)
            url = self.__srv_map[service] + "/" + api
            if resource:
                url = url + "/" + resource
            response = requests.get(url=url, params=req.params)
            if not response.status_code == 200:
                raise RuntimeError("{} {}".format(response.status_code, response.reason))
            resp.body = response.content
            resp.content_type = response.headers.get("content-type")
        except RuntimeError as ex:
            resp.status = str(ex)
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response, service, api, resource=None):
        reqDebugLog(req)
        try:
            if service not in self.__srv_map:
                raise RuntimeError(falcon.HTTP_404)
            url = self.__srv_map[service] + "/" + api
            if resource:
                url = url + "/" + resource
            response = requests.post(url=url, data=req.bounded_stream, params=req.params, headers={"Content-Type": req.content_type})
            if not response.status_code == 200:
                raise RuntimeError("{} {}".format(response.status_code, response.reason))
            resp.status = falcon.HTTP_200
        except RuntimeError as ex:
            resp.status = str(ex)
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_patch(self, req: falcon.request.Request, resp: falcon.response.Response, service, api, resource=None):
        reqDebugLog(req)
        try:
            if service not in self.__srv_map:
                raise RuntimeError(falcon.HTTP_404)
            url = self.__srv_map[service] + "/" + api
            if resource:
                url = url + "/" + resource
            response = requests.patch(url=url, data=req.bounded_stream, params=req.params, headers={"Content-Type": req.content_type})
            if not response.status_code == 200:
                raise RuntimeError("{} {}".format(response.status_code, response.reason))
            resp.status = falcon.HTTP_200
        except RuntimeError as ex:
            resp.status = str(ex)
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_put(self, req: falcon.request.Request, resp: falcon.response.Response, service, api, resource=None):
        reqDebugLog(req)
        try:
            if service not in self.__srv_map:
                raise RuntimeError(falcon.HTTP_404)
            url = self.__srv_map[service] + "/" + api
            if resource:
                url = url + "/" + resource
            response = requests.put(url=url, data=req.bounded_stream, params=req.params, headers={"Content-Type": req.content_type})
            if not response.status_code == 200:
                raise RuntimeError("{} {}".format(response.status_code, response.reason))
            resp.status = falcon.HTTP_200
        except RuntimeError as ex:
            resp.status = str(ex)
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_delete(self, req: falcon.request.Request, resp: falcon.response.Response, service, api, resource=None):
        reqDebugLog(req)
        try:
            if service not in self.__srv_map:
                raise RuntimeError(falcon.HTTP_404)
            url = self.__srv_map[service] + "/" + api
            if resource:
                url = url + "/" + resource
            response = requests.delete(url=url, params=req.params)
            if not response.status_code == 200:
                raise RuntimeError("{} {}".format(response.status_code, response.reason))
            resp.status = falcon.HTTP_200
        except RuntimeError as ex:
            resp.status = str(ex)
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)
