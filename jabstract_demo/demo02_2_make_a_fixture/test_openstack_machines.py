import unittest

import requests_mock

from jabstract_demo.base.specifications import MachineStatus, Machine
from jabstract_demo.demo02_2_make_a_fixture.openstack_machines import OpenstackMachines


class TestOpenstackMachines(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://invalid"
        self.token = "random-token"

        self.openstack_machines = OpenstackMachines(self.base_url, self.token)

    @requests_mock.mock()
    def test_get_machine_returns_a_machine(self, rmock):
        rmock.get("https://invalid/servers/MY-MACHINE", headers={"X-Auth-Token": self.token},
                  json={
                      "server": fixture
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
            fixture["status"] = actual

            rmock.get("https://invalid/servers/MY-MACHINE", headers={"X-Auth-Token": self.token},
                      json={
                          "server": fixture
                      })

            machine = self.openstack_machines.get_machine("MY-MACHINE")

            self.assertEqual(machine.status, expected, f"for {actual}")


fixture = {
    "OS-DCF:diskConfig": "AUTO",
    "OS-EXT-AZ:availability_zone": "nova",
    "OS-EXT-SRV-ATTR:host": "compute",
    "OS-EXT-SRV-ATTR:hostname": "new-server-test",
    "OS-EXT-SRV-ATTR:hypervisor_hostname": "fake-mini",
    "OS-EXT-SRV-ATTR:instance_name": "instance-00000001",
    "OS-EXT-SRV-ATTR:kernel_id": "",
    "OS-EXT-SRV-ATTR:launch_index": 0,
    "OS-EXT-SRV-ATTR:ramdisk_id": "",
    "OS-EXT-SRV-ATTR:reservation_id": "r-ov3q80zj",
    "OS-EXT-SRV-ATTR:root_device_name": "/dev/sda",
    "OS-EXT-SRV-ATTR:user_data": "IyEvYmluL2Jhc2gKL2Jpbi9zdQplY2hvICJJIGFtIGluIHlvdSEiCg==",
    "OS-EXT-STS:power_state": 1,
    "OS-EXT-STS:task_state": None,
    "OS-EXT-STS:vm_state": "active",
    "OS-SRV-USG:launched_at": "2017-02-14T19:23:59.895661",
    "OS-SRV-USG:terminated_at": None,
    "accessIPv4": "1.2.3.4",
    "accessIPv6": "80fe::",
    "addresses": {
        "private": [
            {
                "OS-EXT-IPS-MAC:mac_addr": "aa:bb:cc:dd:ee:ff",
                "OS-EXT-IPS:type": "fixed",
                "addr": "192.168.0.3",
                "version": 4
            }
        ]
    },
    "config_drive": "",
    "created": "2017-02-14T19:23:58Z",
    "description": None,
    "flavor": {
        "disk": 1,
        "ephemeral": 0,
        "extra_specs": {
            "hw:cpu_policy": "dedicated",
            "hw:mem_page_size": "2048"
        },
        "original_name": "m1.tiny.specs",
        "ram": 512,
        "swap": 0,
        "vcpus": 1
    },
    "hostId": "2091634baaccdc4c5a1d57069c833e402921df696b7f970791b12ec6",
    "host_status": "UP",
    "id": "9168b536-cd40-4630-b43f-b259807c6e87",
    "image": {
        "id": "70a599e0-31e7-49b7-b260-868f441e862b",
        "links": [
            {
                "href": "http://openstack.example.com/6f70656e737461636b20342065766572/images/70a599e0-31e7-49b7-b260-868f441e862b",
                "rel": "bookmark"
            }
        ]
    },
    "key_name": None,
    "links": [
        {
            "href": "http://openstack.example.com/v2.1/6f70656e737461636b20342065766572/servers/9168b536-cd40-4630-b43f-b259807c6e87",
            "rel": "self"
        },
        {
            "href": "http://openstack.example.com/6f70656e737461636b20342065766572/servers/9168b536-cd40-4630-b43f-b259807c6e87",
            "rel": "bookmark"
        }
    ],
    "locked": False,
    "metadata": {
        "My Server Name": "Apache1"
    },
    "name": "MY-HOSTNAME",
    "os-extended-volumes:volumes_attached": [],
    "progress": 0,
    "security_groups": [
        {
            "name": "default"
        }
    ],
    "status": "ACTIVE",
    "tags": [],
    "tenant_id": "6f70656e737461636b20342065766572",
    "trusted_image_certificates": [
        "0b5d2c72-12cc-4ba6-a8d7-3ff5cc1d8cb8",
        "674736e3-f25c-405c-8362-bbf991e0ce0a"
    ],
    "updated": "2017-02-14T19:24:00Z",
    "user_id": "fake"
}
