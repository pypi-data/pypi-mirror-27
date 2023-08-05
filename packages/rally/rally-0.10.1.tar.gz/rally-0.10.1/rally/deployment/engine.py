# Copyright 2013: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import jsonschema
import six

from rally.common import logging
from rally.common.plugin import plugin
from rally import consts
from rally import exceptions


LOG = logging.getLogger(__name__)
configure = plugin.configure


@plugin.base()
@six.add_metaclass(abc.ABCMeta)
class Engine(plugin.Plugin):
    """Base class of all deployment engines.

    It's a base class with self-discovery of subclasses. Each subclass
    has to implement deploy() and cleanup() methods. By default, each engine
    located as a submodule of the package rally.deployment.engines is
    auto-discovered.

    Example of usage with a simple engine:

    # Add new engine with __name__ == "A"
    class A(Engine):
        def __init__(self, deployment):
            # do something

        def deploy(self):
            # Make a deployment and return OpenStack credentials.
            # The credentials may have either admin or ordinary users
            # permissions (depending on how the deploy engine has been
            # initialized).
            return [credential_1, credential_2, ...]

        def cleanup(self):
            # Destroy OpenStack deployment and free resource

    An instance of this class used as a context manager on any unsafe
    operations to a deployment. Any unhandled exceptions bring a status
    of the deployment to the inconsistent state.

    with Engine.get_engine("A", deployment) as deploy:
        # deploy is an instance of the A engine
        # perform all usage operations on your cloud
    """
    def __init__(self, deployment):
        self.deployment = deployment

    @property
    def config(self):
        return self.deployment["config"]

    def validate(self, config=None):
        # TODO(sskripnick): remove this checking when config schema
        # is done for all available engines
        if hasattr(self, "CONFIG_SCHEMA"):
            jsonschema.validate(config or self.config, self.CONFIG_SCHEMA)

    # FIXME(boris-42): Get rid of this method
    @staticmethod
    def get_engine(name, deployment):
        """Returns instance of a deploy engine with corresponding name."""
        try:
            engine_cls = Engine.get(name)
            return engine_cls(deployment)
        except exceptions.PluginNotFound:
            LOG.error(
                "Deployment %(uuid)s: Plugin %(name)s doesn't exist."
                % {"uuid": deployment["uuid"], "name": name})
            deployment.update_status(consts.DeployStatus.DEPLOY_FAILED)
            raise

    @abc.abstractmethod
    def deploy(self):
        """Deploy OpenStack cloud and return credentials."""

    @abc.abstractmethod
    def cleanup(self):
        """Cleanup OpenStack deployment."""

    @logging.log_deploy_wrapper(LOG.info, "OpenStack cloud deployment.")
    def make_deploy(self):
        self.deployment.set_started()
        credentials = self.deploy()
        self.deployment.set_completed()
        return credentials

    @logging.log_deploy_wrapper(LOG.info,
                                "Destroy cloud and free allocated resources.")
    def make_cleanup(self):
        self.deployment.update_status(consts.DeployStatus.CLEANUP_STARTED)
        self.cleanup()
        self.deployment.update_status(consts.DeployStatus.CLEANUP_FINISHED)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            exc_info = None
            if not issubclass(exc_type, exceptions.InvalidArgumentsException):
                exc_info = (exc_type, exc_value, exc_traceback)
            LOG.error("Deployment %s: Error has occurred in context "
                      "of the deployment" % self.deployment["uuid"],
                      exc_info=exc_info)
            status = self.deployment["status"]
            if status in (consts.DeployStatus.DEPLOY_INIT,
                          consts.DeployStatus.DEPLOY_STARTED):
                self.deployment.update_status(
                    consts.DeployStatus.DEPLOY_FAILED)
            elif status == consts.DeployStatus.DEPLOY_FINISHED:
                self.deployment.update_status(
                    consts.DeployStatus.DEPLOY_INCONSISTENT)
            elif status == consts.DeployStatus.CLEANUP_STARTED:
                self.deployment.update_status(
                    consts.DeployStatus.CLEANUP_FAILED)
