import unittest

import requests_mock

from jabstract_demo.base.specifications import MachineStatus, Machine
from jabstract_demo.demo01_1_add_private_method.openstack_machines import OpenstackMachines
from jabstract_demo.demo01_1_add_private_method.openstack_machines import _machine_status


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

    def test_machine_statuses(self):
        self.assertEqual(_machine_status("ACTIVE"), MachineStatus.UP)
        self.assertEqual(_machine_status("SHUFTOFF"), MachineStatus.DOWN)
        self.assertEqual(_machine_status("WHATEVER"), MachineStatus.DOWN)
