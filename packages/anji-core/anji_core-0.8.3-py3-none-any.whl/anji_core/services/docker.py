import itertools

from anji_orm import StringField, IntField
import psutil
import consul

from .core import AbstractService

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.8.3"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"


class DockerService(AbstractService):

    model_subtype = 'docker'

    container_name = StringField(description='Docker container name', reconfigurable=True)
    signal_timeout = IntField(description='Timeout before force operation', reconfigurable=True, default=10)

    def service_registration(self) -> None:
        container = self.get_container_object()
        container_top = container.top()
        pid_index = container_top['Titles'].index('PID')
        connections_iterator = itertools.chain.from_iterable(psutil.Process(int(x[pid_index])).connections() for x in container_top['Processes'])
        useful_connections = [con for con in connections_iterator if con.status == psutil.CONN_LISTEN]
        if useful_connections:
            first_addr = useful_connections[0]
            self.shared.consul.agent.service.register(self.technical_name, address=first_addr.laddr.ip, port=first_addr.laddr.port)
            if len(useful_connections) < 2:
                self.shared.consul.agent.check.register(
                    self.technical_name, service_id=self.technical_name,
                    check=consul.Check.tcp(first_addr.laddr.ip, first_addr.laddr.port, '30s')
                )
            else:
                for useful_connection in useful_connections:
                    check_name = f"{self.technical_name}-{useful_connection.laddr.ip}-{useful_connection.laddr.port}"
                    self.shared.consul(
                        check_name, service_id=self.technical_name,
                        check=consul.Check.tcp(useful_connection.laddr.ip, useful_connection.laddr.port, '30s')
                    )
        else:
            self.shared.consul.agent.service.register(self.technical_name)

    def get_container_object(self):
        import docker
        client = docker.from_env()
        return client.containers.get(self.container_name)

    def start(self):
        container = self.get_container_object()
        container.start()

    def stop(self):
        container = self.get_container_object()
        container.stop(timeout=self.signal_timeout)

    def restart(self):
        container = self.get_container_object()
        container.restart(timeout=self.signal_timeout)
