"""Backward-compatible entry point.

The production workflow lives in ``src``. This wrapper keeps older commands such
as ``python healthcare.py`` working while avoiding duplicate graph code.
"""

from src.main import main


if __name__ == "__main__":
    main()
