#   Copyright 2021 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Module """
from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import module  # pylint: disable=E0611,E0401
from tools import theme, VaultClient, constants as c


class Module(module.ModuleModel):
    """ Pylon module """

    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor

    def init(self):
        """ Init module """
        log.info("Initializing module Secrets")
        self.descriptor.init_api()
        self.descriptor.init_rpcs()
        self.descriptor.init_blueprint()

        theme.register_subsection(
            "configuration", "secrets",
            "Secrets",
            title="Secrets",
            kind="slot",
            permissions={
                "permissions": ["configuration.secrets"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": False, "editor": False},
                    "default": {"admin": True, "viewer": False, "editor": False},
                    "developer": {"admin": True, "viewer": False, "editor": False},
                }},
            prefix="secrets_",
            weight=5,
        )

        theme.register_mode_subsection(
            "administration", "configuration",
            "secrets", "Secrets",
            title="Secrets",
            kind="slot",
            permissions={
                "permissions": ["configuration.secrets"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": False, "editor": False},
                    "default": {"admin": True, "viewer": False, "editor": False},
                    "developer": {"admin": True, "viewer": False, "editor": False},
                }},
            prefix="administration_secrets_",
            # icon_class="fas fa-server fa-fw",
            # weight=2,
        )

        self.descriptor.init_slots()

        vault_client = VaultClient()
        initial_secrets = {
            'influx_port': c.INFLUX_PORT,
            'loki_port': c.LOKI_PORT,
            'redis_password': c.REDIS_PASSWORD,
            'rabbit_user': c.RABBIT_USER,
            'rabbit_password': c.RABBIT_PASSWORD,
            'influx_user': c.INFLUX_USER,
            'influx_password': c.INFLUX_PASSWORD,
            'gf_api_key': c.GF_API_KEY,
            'backend_performance_results_retention': c.BACKEND_PERFORMANCE_RESULTS_RETENTION
        }
        persistent_secrets = {
            'galloper_url': c.APP_HOST,
            'redis_host': c.REDIS_HOST,
            'loki_host': c.LOKI_HOST,
            'influx_ip': c.APP_IP,
            'rabbit_host': c.APP_IP,
        }
        existing_secrets = vault_client.get_all_secrets()
        initial_secrets.update(existing_secrets)
        initial_secrets.update(persistent_secrets)
        vault_client.set_secrets(initial_secrets)
        log.info('secrets set %s', initial_secrets)

    def deinit(self):  # pylint: disable=R0201
        """ De-init module """
        log.info("De-initializing module Secrets")
