import subprocess
from pathlib import Path

import docker


def main():
    current_path = Path().resolve()
    subprocess.run(
        [
            "docker", "run", "-it", "--rm", "-v", f"{current_path}:/foo:ro",
            "example"
        ]
    )


if __name__ == "__main__":
    main()
