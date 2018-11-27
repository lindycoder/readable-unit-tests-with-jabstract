import unittest

import requests_mock

from jabstract_demo.base.specifications import MachineStatus, Machine
from jabstract_demo.demo01_0_starting_off.openstack_machines import OpenstackMachines


class TestOpenstackMachines(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://invalid"
        self.token = "random-token"

        self.openstack_machines = OpenstackMachines(self.base_url, self.token)

    @requests_mock.mock()
    def test_get_machine_returns_a_machine(self, rmock):
        rmock.get("https://invalid/servers/MY-MACHINE", headers={"X-Auth-Token": self.token},
                  json={
                      "server": {
                          "name": "MY-HOSTNAME",
                          "status": "ACTIVE"
                      }
                  })

        machine = self.openstack_machines.get_machine("MY-MACHINE")

        self.assertEqual(machine, Machine(
            hostname="MY-HOSTNAME",
            status=MachineStatus.UP
        ))

    @requests_mock.mock()
    def test_get_machine_with_status_down(self, rmock):
        rmock.get("https://invalid/servers/MY-MACHINE", headers={"X-Auth-Token": self.token},
                  json={
                      "server": {
                          "name": "MY-HOSTNAME",
                          "status": "SHUTOFF"
                      }
                  })

        machine = self.openstack_machines.get_machine("MY-MACHINE")

        self.assertEqual(machine.status, MachineStatus.DOWN)

    @requests_mock.mock()
    def test_get_machine_with_status_unknown_assume_down(self, rmock):
        rmock.get("https://invalid/servers/MY-MACHINE", headers={"X-Auth-Token": self.token},
                  json={
                      "server": {
                          "name": "MY-HOSTNAME",
                          "status": "WHATEVER"
                      }
                  })

        machine = self.openstack_machines.get_machine("MY-MACHINE")

        self.assertEqual(machine.status, MachineStatus.DOWN)
