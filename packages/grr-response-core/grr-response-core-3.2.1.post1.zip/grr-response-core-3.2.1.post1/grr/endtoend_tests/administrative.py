#!/usr/bin/env python
"""End to end tests for lib.flows.general.administrative."""

import logging
import os


from grr import config
from grr.endtoend_tests import base
from grr.server import aff4
from grr.server import maintenance_utils
from grr.server.aff4_objects import collects as aff4_collects
from grr.server.aff4_objects import stats as aff4_stats
from grr.server.flows.general import administrative


class TestGetClientStats(base.AutomatedTest):
  """GetClientStats test."""
  platforms = ["Linux", "Windows", "Darwin"]
  test_output_path = "stats"
  flow = administrative.GetClientStats.__name__

  def CheckFlow(self):
    aff4.FACTORY.Flush()
    client_stats = aff4.FACTORY.Open(
        self.client_id.Add(self.test_output_path), token=self.token)
    self.assertIsInstance(client_stats, aff4_stats.ClientStats)

    stats_list = list(client_stats.Get(client_stats.Schema.STATS))
    self.assertGreater(len(stats_list), 0)
    entry = stats_list[0]
    self.assertGreater(entry.RSS_size, 0)
    self.assertGreater(entry.VMS_size, 0)
    self.assertGreater(entry.boot_time, 0)
    self.assertGreater(entry.bytes_received, 0)
    self.assertGreater(entry.bytes_sent, 0)
    self.assertGreater(entry.memory_percent, 0)

    self.assertGreater(len(list(entry.cpu_samples)), 0)
    if not list(entry.io_samples):
      logging.warning("No IO samples received. This is ok if the tested"
                      " client is a mac.")


class TestLaunchBinaries(base.ClientTestBase):
  """Test that we can launch a binary.

  The following program is used and will be signed and uploaded before
  executing the test if it hasn't been uploaded already.

  #include <stdio.h>
  int main(int argc, char** argv) {
    printf("Hello world!!!");
    return 0;
  };

  This class deliberately doesn't inherit from base.AutomatedTest because the
  code signing requires a password.
  """
  platforms = ["Windows", "Linux"]
  flow = administrative.LaunchBinary.__name__
  filenames = {"Windows": "hello.exe", "Linux": "hello"}
  ds_names = {"Windows": "hello.exe", "Linux": "hello"}

  limit = None

  def __init__(self, **kwargs):
    super(TestLaunchBinaries, self).__init__(**kwargs)
    self.context = ["Platform:%s" % self.platform.title()]
    self.binary = config.CONFIG.Get(
        "Executables.aff4_path", context=self.context).Add(
            "test/%s" % self.ds_names[self.platform])

    self.args = dict(binary=self.binary)

    try:
      aff4.FACTORY.Open(
          self.binary, aff4_type=aff4_collects.GRRSignedBlob, token=self.token)
    except IOError:
      print "Uploading the test binary to the Executables area."
      source = os.path.join(config.CONFIG["Test.data_dir"],
                            self.filenames[self.platform])

      if not os.path.exists(source):
        self.fail("Path %s should exist." % source)

      maintenance_utils.UploadSignedConfigBlob(
          open(source, "rb").read(),
          aff4_path=self.binary,
          client_context=self.context,
          token=self.token,
          limit=self.limit)

  def CheckFlow(self):
    # Check that the test binary returned the correct stdout:
    fd = aff4.FACTORY.Open(
        self.session_id, age=aff4.ALL_TIMES, token=self.token)
    logs = "\n".join([x.log_message for x in fd.GetLog()])

    self.assertTrue("Hello world" in logs)


class TestLaunchChunkedBinaries(TestLaunchBinaries):
  # Set a small limit for the maximum blob size such that the binary gets
  # split into multiple parts when uploading.
  limit = 5000

  # Since we want to store the binary using chunks, we need to assign it a
  # different aff4 path than the one used in the previous test.
  ds_names = {"Windows": "hello_chunked.exe", "Linux": "hello_chunked"}
