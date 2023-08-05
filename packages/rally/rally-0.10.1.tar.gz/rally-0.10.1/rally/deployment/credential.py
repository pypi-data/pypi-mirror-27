# Copyright 2017: Mirantis Inc.
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

from rally.common.plugin import plugin


def configure(platform):
    def wrapper(cls):
        cls = plugin.configure(name="credential", platform=platform)(cls)
        return cls
    return wrapper


def get(platform):
    return Credential.get(name="credential", platform=platform)


@plugin.base()
@six.add_metaclass(abc.ABCMeta)
class Credential(plugin.Plugin):
    """Base class for credentials."""

    @abc.abstractmethod
    def to_dict(self):
        """Converts credential object to dict.

        :returns: dict that can be used to recreate credential using
            constructor: Credential(**credential.to_dict())
        """

    @abc.abstractmethod
    def verify_connection(self):
        """Verifies that credential can be used for connection."""

    def list_services(self):
        """Returns available services.

        :returns: dict
        """
        return {}

    @classmethod
    def get_validation_context(cls):
        return {}


def configure_builder(platform):
    def wrapper(cls):
        cls = plugin.configure(name="credential_builder",
                               platform=platform)(cls)
        return cls
    return wrapper


def get_builder(platform):
    return CredentialBuilder.get(name="credential_builder",
                                 platform=platform)


@plugin.base()
@six.add_metaclass(abc.ABCMeta)
class CredentialBuilder(plugin.Plugin):
    """Base class for extensions of ExistingCloud deployment."""

    CONFIG_SCHEMA = {"type": "null"}

    def __init__(self, config):
        self.config = config

    @classmethod
    def validate(cls, config):
        jsonschema.validate(config, cls.CONFIG_SCHEMA)

    @abc.abstractmethod
    def build_credentials(self):
        """Builds credentials from provided configuration"""
