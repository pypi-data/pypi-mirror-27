#!/usr/bin/env python
"""Tests for grr.server.flows.general.endtoend."""

from grr.endtoend_tests import base
from grr.endtoend_tests import endtoend_mocks
from grr.lib import flags
from grr.lib import rdfvalue
from grr.lib import utils
from grr.lib.rdfvalues import client as rdf_client
from grr.server import aff4
from grr.server import flow
from grr.server.aff4_objects import aff4_grr
from grr.server.flows.general import endtoend
from grr.test_lib import action_mocks
from grr.test_lib import flow_test_lib
from grr.test_lib import test_lib


class TestEndToEndTestFlow(flow_test_lib.FlowTestsBaseclass):

  def setUp(self):
    super(TestEndToEndTestFlow, self).setUp()
    self.SetupClients(1, system="Linux", os_version="14.04", arch="x86_64")
    install_time = rdfvalue.RDFDatetime.Now()
    user = "testuser"
    userobj = rdf_client.User(username=user)
    interface = rdf_client.Interface(ifname="eth0")
    self.client = aff4.FACTORY.Create(
        self.client_id,
        aff4_grr.VFSGRRClient,
        mode="rw",
        token=self.token,
        age=aff4.ALL_TIMES)
    kb = self.client.Get(self.client.Schema.KNOWLEDGE_BASE)
    kb.users.Append(userobj)
    self.client.Set(self.client.Schema.HOSTNAME("hostname"))
    self.client.Set(self.client.Schema.OS_RELEASE("debian"))
    self.client.Set(self.client.Schema.KERNEL("3.15-rc2"))
    self.client.Set(self.client.Schema.FQDN("hostname.example.com"))
    self.client.Set(self.client.Schema.INSTALL_DATE(install_time))
    self.client.Set(self.client.Schema.KNOWLEDGE_BASE(kb))
    self.client.Set(self.client.Schema.USERNAMES([user]))
    self.client.Set(self.client.Schema.INTERFACES([interface]))
    self.client.Flush()

    self.client_mock = action_mocks.ListDirectoryClientMock()

  def testRunSuccess(self):
    args = endtoend.EndToEndTestFlowArgs(test_names=[
        "TestListDirectoryOSLinuxDarwin", "MockEndToEndTest",
        "TestListDirectoryOSLinuxDarwin"
    ])

    with test_lib.Instrument(flow.GRRFlow, "SendReply") as send_reply:
      for _ in flow_test_lib.TestFlowHelper(
          endtoend.EndToEndTestFlow.__name__,
          self.client_mock,
          client_id=self.client_id,
          token=self.token,
          args=args):
        pass

      results = []
      for _, reply in send_reply.args:
        if isinstance(reply, endtoend.EndToEndTestResult):
          results.append(reply)
          self.assertTrue(reply.success)
          self.assertTrue(reply.test_class_name in [
              "TestListDirectoryOSLinuxDarwin", "MockEndToEndTest"
          ])
          self.assertFalse(reply.log)

      # We only expect 2 results because we dedup test names
      self.assertEqual(len(results), 2)

  def testNoApplicableTests(self):
    """Try to run linux tests on windows."""
    self.SetupClients(
        1, system="Windows", os_version="6.1.7601SP1", arch="AMD64")
    install_time = rdfvalue.RDFDatetime.Now()
    user = "testuser"
    userobj = rdf_client.User(username=user)
    interface = rdf_client.Interface(ifname="eth0")
    self.client = aff4.FACTORY.Create(
        self.client_id,
        aff4_grr.VFSGRRClient,
        mode="rw",
        token=self.token,
        age=aff4.ALL_TIMES)

    kb = self.client.Get(self.client.Schema.KNOWLEDGE_BASE)
    kb.users.Append(userobj)
    self.client.Set(self.client.Schema.HOSTNAME("hostname"))
    self.client.Set(self.client.Schema.OS_RELEASE("7"))
    self.client.Set(self.client.Schema.KERNEL("6.1.7601"))
    self.client.Set(self.client.Schema.FQDN("hostname.example.com"))
    self.client.Set(self.client.Schema.INSTALL_DATE(install_time))
    self.client.Set(self.client.Schema.KNOWLEDGE_BASE(kb))
    self.client.Set(self.client.Schema.USERNAMES([user]))
    self.client.Set(self.client.Schema.INTERFACES([interface]))
    self.client.Flush()

    args = endtoend.EndToEndTestFlowArgs(test_names=[
        "TestListDirectoryOSLinuxDarwin", "MockEndToEndTest",
        "TestListDirectoryOSLinuxDarwin"
    ])

    self.assertRaises(flow.FlowError, list,
                      flow_test_lib.TestFlowHelper(
                          endtoend.EndToEndTestFlow.__name__,
                          self.client_mock,
                          client_id=self.client_id,
                          token=self.token,
                          args=args))

  def testRunSuccessAndFail(self):
    args = endtoend.EndToEndTestFlowArgs()

    with utils.Stubber(base.AutomatedTest, "classes", {
        "MockEndToEndTest": endtoend_mocks.MockEndToEndTest,
        "TestFailure": endtoend_mocks.TestFailure
    }):
      with test_lib.Instrument(flow.GRRFlow, "SendReply") as send_reply:
        for _ in flow_test_lib.TestFlowHelper(
            endtoend.EndToEndTestFlow.__name__,
            self.client_mock,
            client_id=self.client_id,
            token=self.token,
            args=args):
          pass

        results = []
        for _, reply in send_reply.args:
          if isinstance(reply, endtoend.EndToEndTestResult):
            results.append(reply)
            if reply.test_class_name == "MockEndToEndTest":
              self.assertTrue(reply.success)
              self.assertFalse(reply.log)
            elif reply.test_class_name == "TestFailure":
              self.assertFalse(reply.success)
              self.assertTrue("This should be logged" in reply.log)

        self.assertItemsEqual([x.test_class_name for x in results],
                              ["MockEndToEndTest", "TestFailure"])
        self.assertEqual(len(results), 2)

  def testRunBadSetUp(self):
    args = endtoend.EndToEndTestFlowArgs(test_names=["TestBadSetUp"])

    self.assertRaises(RuntimeError, list,
                      flow_test_lib.TestFlowHelper(
                          endtoend.EndToEndTestFlow.__name__,
                          self.client_mock,
                          client_id=self.client_id,
                          token=self.token,
                          args=args))

  def testRunBadTearDown(self):
    args = endtoend.EndToEndTestFlowArgs(test_names=["TestBadTearDown"])

    self.assertRaises(RuntimeError, list,
                      flow_test_lib.TestFlowHelper(
                          endtoend.EndToEndTestFlow.__name__,
                          self.client_mock,
                          client_id=self.client_id,
                          token=self.token,
                          args=args))

  def testRunBadFlow(self):
    """Test behaviour when test flow raises in Start.

    A flow that raises in its Start method will kill the EndToEndTest run.
    Protecting and reporting on this significantly complicates this code, and a
    flow raising in Start is really broken, so we allow this behaviour.
    """
    args = endtoend.EndToEndTestFlowArgs(
        test_names=["MockEndToEndTestBadFlow", "MockEndToEndTest"])

    self.assertRaises(RuntimeError, list,
                      flow_test_lib.TestFlowHelper(
                          endtoend.EndToEndTestFlow.__name__,
                          self.client_mock,
                          client_id=self.client_id,
                          token=self.token,
                          args=args))

  def testEndToEndTestFailure(self):
    args = endtoend.EndToEndTestFlowArgs(test_names=["TestFailure"])

    with test_lib.Instrument(flow.GRRFlow, "SendReply") as send_reply:

      for _ in flow_test_lib.TestFlowHelper(
          endtoend.EndToEndTestFlow.__name__,
          self.client_mock,
          client_id=self.client_id,
          token=self.token,
          args=args):
        pass

      results = []
      for _, reply in send_reply.args:
        if isinstance(reply, endtoend.EndToEndTestResult):
          results.append(reply)
          self.assertFalse(reply.success)
          self.assertEqual(reply.test_class_name, "TestFailure")
          self.assertTrue("This should be logged" in reply.log)

      self.assertEqual(len(results), 1)


def main(argv):
  test_lib.main(argv)


if __name__ == "__main__":
  flags.StartMain(main)
