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

__all__ = ("ui_conf", "EnvVars", "static_dir")


import simple_env_var
import os

static_dir = "{}/static".format(os.path.dirname(os.path.realpath(__file__)))


@simple_env_var.configuration
class UIConf:

    @simple_env_var.section
    class MR:
        url = "http://module-registry"
        api = "modules"

    @simple_env_var.section
    class Internal:
        mm = "http://module-management"
        dm = "http://deployment-management"
        m = "http://monitoring"
        cs = "http://configuration-storage"

    @simple_env_var.section
    class Logger:
        level = "info"


ui_conf = UIConf()


class EnvVars:

    class GatewayLocalIP:
        name = "GATEWAY_LOCAL_IP"
        value = os.getenv("GATEWAY_LOCAL_IP")

    class ModuleID:
        name = "MODULE_ID"
        value = os.getenv("MODULE_ID")
