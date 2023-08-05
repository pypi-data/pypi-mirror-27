#!/usr/bin/env python
"""GRR data store tests.

This module loads and registers all the data store tests.
"""


# These need to register plugins so,
# pylint: disable=unused-import,g-import-not-at-top

from grr.server.data_stores import fake_data_store_test

try:
  from grr.server.data_stores import cloud_bigtable_data_store_test
except ImportError:
  pass

try:
  from grr.server.data_stores import mysql_advanced_data_store_test
except ImportError:
  pass

try:
  from grr.server.data_stores import sqlite_data_store_test
except ImportError:
  pass
