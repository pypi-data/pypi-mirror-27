#!/usr/bin/env python
"""End to end tests for lib.flows.general.registry."""

import os

from grr.endtoend_tests import base
from grr.lib import utils
from grr.lib.rdfvalues import client as rdf_client
from grr.lib.rdfvalues import paths as rdf_paths
from grr.server import aff4
from grr.server import data_store
from grr.server import flow_utils
from grr.server.flows.console import debugging
from grr.server.flows.general import filesystem
from grr.server.flows.general import find


class TestFindWindowsRegistry(base.ClientTestBase):
  """Test that user listing from the registry works.

  We basically list the registry and then run Find on the same place, we expect
  a single ProfileImagePath value for each user.

  TODO(user): this is excluded from automated tests for now because it needs
  to run two flows and defines its own runTest to do so.  We should support
  this but it requires more work.
  """
  flow = "DisabledTestFindWindowsRegistry"
  platforms = ["Windows"]
  reg_path = ("/HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Windows NT/"
              "CurrentVersion/ProfileList/")

  def runTest(self):
    """Launch our flows."""
    for flow, args in [(filesystem.ListDirectory.__name__, {
        "pathspec":
            rdf_paths.PathSpec(
                pathtype=rdf_paths.PathSpec.PathType.REGISTRY,
                path=self.reg_path)
    }), (find.FindFiles.__name__, {
        "findspec":
            rdf_client.FindSpec(
                pathspec=rdf_paths.PathSpec(
                    path=self.reg_path,
                    pathtype=rdf_paths.PathSpec.PathType.REGISTRY),
                path_regex="ProfileImagePath"),
    })]:

      if self.local_worker:
        self.session_id = debugging.StartFlowAndWorker(self.client_id, flow,
                                                       **args)
      else:
        self.session_id = flow_utils.StartFlowAndWait(
            self.client_id, flow_name=flow, token=self.token, **args)

    results = self.CheckResultCollectionNotEmptyWithRetry(self.session_id)
    for stat_entry in results:
      self.assertTrue(isinstance(stat_entry, rdf_client.StatEntry))
      self.assertTrue("ProfileImagePath" in stat_entry.pathspec.path)


class TestClientRegistry(base.AutomatedTest):
  """Tests if listing registry keys works on Windows."""
  platforms = ["Windows"]
  flow = filesystem.ListDirectory.__name__

  args = {
      "pathspec":
          rdf_paths.PathSpec(
              path="HKEY_LOCAL_MACHINE",
              pathtype=rdf_paths.PathSpec.PathType.REGISTRY)
  }
  output_path = "/registry/HKEY_LOCAL_MACHINE"

  def CheckFlow(self):
    urn = self.client_id.Add(self.output_path)
    fd = aff4.FACTORY.Open(urn, mode="r", token=self.token)
    children = list(fd.OpenChildren())
    self.assertTrue(
        "SYSTEM" in
        [os.path.basename(utils.SmartUnicode(child.urn)) for child in children])

  def tearDown(self):
    urn = self.client_id.Add(self.output_path)
    data_store.DB.DeleteSubject(str(urn.Add("SYSTEM")))
    data_store.DB.DeleteSubject(str(urn))
