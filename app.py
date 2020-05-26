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

from gui.logger import initLogger
from gui.configuration import ui_conf, static_dir
from gui import api
import falcon


initLogger(ui_conf.Logger.level)


app = falcon.API()

app.req_options.strip_url_path_trailing_slash = True

routes = (
    ("/", api.Static("/static/index.html")),
    ("/api/{service}/{api}", api.Router()),
    ("/api/{service}/{api}/{resource}", api.Router())
)

app.add_static_route("/static", static_dir)

for route in routes:
    app.add_route(*route)

# gunicorn -b 0.0.0.0:8000 --workers 1 --threads 4 --worker-class gthread --log-level error app:app