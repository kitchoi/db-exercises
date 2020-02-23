import os
import shutil
import subprocess
import time

import click


HERE = os.path.dirname(__file__)
DEVENV_DIR = os.path.join(HERE, ".env")
DEVENV_BIN = os.path.join(DEVENV_DIR, "bin")
PYTHON = os.path.join(DEVENV_BIN, "python")


DEPENDENCIES = [
    "sqlalchemy",
    "psycopg2-binary",
]


@click.group()
def main():
    pass


@main.command("build")
def build():
    if os.path.exists(DEVENV_DIR):
        shutil.rmtree(DEVENV_DIR)
    subprocess.run(
        ["python3.8", "-m", "venv", DEVENV_DIR],
    )
    for package in DEPENDENCIES:
        subprocess.run(
            [
                get_command("pip"),
                "install",
                package,
            ]
        )
    subprocess.run([PYTHON, "setup.py", "develop"])


@main.command("test")
@click.option("-v/--verbose", "verbose", is_flag=True)
def test(verbose):

    dbname = "test"
    postgres_process = subprocess.Popen(
        os.path.join(HERE, "postgres_start.sh"),
        env={"NAME": dbname},
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    with postgres_process:
        # Reset
        postgres_process.stdin.write(b"y\n")

        time.sleep(8)

        command = [
            PYTHON,
            "-m", "unittest",
            "discover",
            "-t", HERE,
        ]
        if verbose:
            command.append("-v")

        command.append(HERE)
        completed_proc = subprocess.run(
            command,
            env={
                "POSRGRES_URL": (
                    "postgresql://postgres:postgres@0.0.0.0/" + dbname
                ),
            })
        # Clean up
        postgres_process.stdin.write(b"y\n")

    if completed_proc.returncode > 0:
        raise click.ClickException("Failed.")


def get_command(name):
    return os.path.join(DEVENV_BIN, name)


if __name__ == "__main__":
    main()
