
from pathlib import Path

import docker


def main():
    client = docker.from_env()
    root_path = Path(__file__).parent.resolve()
    for docker_file in root_path.rglob("*.DockerFile"):
        client.images.build(
            path=str(docker_file.parent),
            dockerfile=str(docker_file),
            tag=f"{docker_file.stem}-container"
        )


if __name__ == "__main__":
    main()
