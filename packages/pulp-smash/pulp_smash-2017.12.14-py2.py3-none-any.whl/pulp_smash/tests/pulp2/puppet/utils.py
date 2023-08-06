# coding=utf-8
"""Utilities for Puppet tests."""
from pulp_smash import utils


def set_up_module():
    """Skip tests if the Puppet plugin is not installed.

    See :mod:`pulp_smash.tests` for more information.
    """
    utils.set_up_module()
    utils.skip_if_type_is_unsupported('puppet_module')
