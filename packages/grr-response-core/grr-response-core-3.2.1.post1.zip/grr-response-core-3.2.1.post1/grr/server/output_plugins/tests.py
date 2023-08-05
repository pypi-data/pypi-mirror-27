#!/usr/bin/env python
"""Loads up all output plugins tests."""

# pylint: disable=unused-import,g-import-not-at-top,g-statement-before-imports
try:
  from grr.server.output_plugins import bigquery_plugin_test
except ImportError:
  pass

from grr.server.output_plugins import csv_plugin_test
from grr.server.output_plugins import email_plugin_test
from grr.server.output_plugins import sqlite_plugin_test
from grr.server.output_plugins import yaml_plugin_test
