"""
main.py — MedLogic Entry Point
================================
Usage:
    python main.py

Architecture:
    main.py
      │
      ├── data.symptoms_db.load_facts()   ← loads all Kanren relations
      │
      └── interface.cli.run_cli()         ← starts the interactive loop
              │
              └── logic.reasoner.analyze()
                      │
                      └── logic.engine.*  ← Kanren queries
                              │
                              └── data.symptoms_db.*  ← Relations + facts
"""

import sys
from data.symptoms_db import load_facts
from interface.cli import run_cli


def main() -> None:
    # Step 1: Assert all facts into Kanren Relations (in-memory logic DB)
    load_facts()

    # Step 2: Hand control to the interactive CLI
    run_cli()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted. Goodbye!\n")
        sys.exit(0)
