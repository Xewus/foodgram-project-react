from time import sleep

import docker
from docker.models.containers import Container


class Docker:
    """Running and managing Docker containers for testing."""

    def __init__(
        self,
        postgres_name: str = "postgres_test",
        postgres_port: int = 5432,
        postgres_user: str = "postgres",
        postgres_password: str = "postgres",
    ) -> None:
        self.postgres_name = postgres_name
        self.postgres_port = postgres_port
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.containers: list[Container] = []
        self.client = docker.from_env()

        for _ in range(5):
            if self.client.ping():
                break
            sleep(1)
        else:
            raise ConnectionError("no connection to docker")

        for container in self.client.containers.list():
            container: Container
            if container.name == postgres_name:
                container.stop()
                container.wait()

    def __enter__(self) -> None:
        self.run_all()

    def __exit__(self, *_) -> None:
        self.stop_all()

    def _check_running_container(self, container: Container) -> None:
        """Make sure the container status is running.
        Time limit for checking is near `1.5 sec`.

        #### Args:
        - container (Container):
            Container for checking.

        #### Raises:
        - ConnectionError:
            Time limit for checking is out.
        """
        for _ in range(5):
            if container.status == "running":
                break
            sleep(0.3)
            container.reload()
        else:
            raise ConnectionError(f"{container.name} is not running")
        return None

    def _check_running_containers(self) -> None:
        """Check the status of all containers."""
        for container in self.containers:
            self._check_running_container(container)
        return None

    def _run_postgres(self) -> None:
        """Run container with `Postgres` database.."""
        postgres: Container = self.client.containers.run(
            image="postgres:15-alpine",
            name=self.postgres_name,
            environment={"POSTGRES_PASSWORD": self.postgres_password},
            ports={5432: self.postgres_port},
            auto_remove=True,
            detach=True,
        )
        self.containers.append(postgres)
        return None

    def stop_all(self) -> None:
        """Stop all containers associated with the `Doker` instance."""
        for container in self.containers:
            container.stop()
            container.wait()
        return None

    def run_all(self) -> None:
        """Run all containers associated with the `Doker` instance."""
        self.stop_all()
        self._run_postgres()
        self._run_redis()
        self._check_running_containers()
        return None
