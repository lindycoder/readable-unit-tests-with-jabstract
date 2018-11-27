import unittest

import requests_mock

from jabstract_demo.base.specifications import MachineStatus, Machine
from jabstract_demo.demo01_3_back_to_big_test.openstack_machines import OpenstackMachines


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
    def test_machine_statuses(self, rmock):
        expectations = [
            ("ACTIVE", MachineStatus.UP),
            ("SHUFTOFF", MachineStatus.DOWN),
            ("WHATEVER", MachineStatus.DOWN),
        ]

        for actual, expected in expectations:
            rmock.get("https://invalid/servers/MY-MACHINE", headers={"X-Auth-Token": self.token},
                  json={
                      "server": {
                          "name": "MY-HOSTNAME",
                          "status": actual
                      }
                  })

            machine = self.openstack_machines.get_machine("MY-MACHINE")

            self.assertEqual(machine.status, expected, f"for {actual}")
