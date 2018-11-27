import requests

from jabstract_demo.base.specifications import Machine, MachineStatus, Machines


class OpenstackMachines(Machines):
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_machine(self, identifier: str) -> Machine:
        response = requests.get(f"{self.base_url}/servers/{identifier}", headers={"X-Auth-Token": self.auth_token})

        server = response.json()["server"]

        return Machine(
            hostname=server["name"],
            status=_machine_status(server["status"]),
        )


def _machine_status(status):
    try:
        return {
            "ACTIVE": MachineStatus.UP,
            "SHUTOFF": MachineStatus.DOWN
        }[status]
    except KeyError:
        return MachineStatus.DOWN
