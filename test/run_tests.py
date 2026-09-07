import unittest.loader
from pathlib import Path

from Autumn import new  # type: ignore[import-not-found]


def write(out: str, dest: str):
    path = Path(f"test_results/{dest}")
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as file:
        file.write(out if not out.startswith("<!DOCTYPE") else out)

if __name__ == "__main__":
    new() # To load

    suite = unittest.loader.defaultTestLoader.discover("./test")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)