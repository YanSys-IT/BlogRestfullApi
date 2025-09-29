"""Small utility to inspect SQLite foreign keys and report violations.

Usage:
  python scripts/check_fk.py            # use db.sqlite3 in project root
  python scripts/check_fk.py --db path  # use custom sqlite file
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple


def iter_tables(conn: sqlite3.Connection) -> Iterable[str]:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    for (name,) in cur.fetchall():
        yield name


def fk_list_for_table(conn: sqlite3.Connection, table: str) -> List[Tuple[int, int, str, str, str, str, str]]:
    """Returns rows of PRAGMA foreign_key_list(table).

    Columns returned are: id, seq, table, from, to, on_update, on_delete, match
    """
    cur = conn.execute(f"PRAGMA foreign_key_list('{table}')")
    return cur.fetchall()


def foreign_key_check(conn: sqlite3.Connection) -> List[Tuple[str, int, str]]:
    """Returns rows from PRAGMA foreign_key_check -> (table, rowid, parent)."""
    cur = conn.execute("PRAGMA foreign_key_check")
    return cur.fetchall()


def print_report(db_path: Path) -> int:
    if not db_path.exists():
        print(f"ERROR: database file not found: {db_path}")
        return 2

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    print(f"Inspecting SQLite DB: {db_path}\n")

    any_fk = False
    for table in iter_tables(conn):
        fks = fk_list_for_table(conn, table)
        if not fks:
            continue
        any_fk = True
        print(f"Table: {table}")
        print("  id | seq | table -> from->to | on_update | on_delete | match")
        for row in fks:
            # pragma foreign_key_list returns columns: id, seq, table, from, to, on_update, on_delete, match
            print("  " + " | ".join(str(x) for x in row))
        print("")

    if not any_fk:
        print("No tables with declared foreign keys found.")

    violations = foreign_key_check(conn)
    if not violations:
        print("No foreign-key constraint violations detected (PRAGMA foreign_key_check).")
        return 0

    print("\nForeign key violations (PRAGMA foreign_key_check):")
    print("  table | rowid | parent")
    for v in violations:
        print("  " + " | ".join(str(x) for x in v))

    return 1


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Check SQLite foreign keys and report violations.")
    p.add_argument(
        "--db",
        "-d",
        help="Path to sqlite database file. Defaults to db.sqlite3 in repo root.",
    )
    args = p.parse_args(argv)

    # Determine default db path relative to project root (one level up from scripts/)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    db_path = Path(args.db) if args.db else project_root / "db.sqlite3"

    try:
        return print_report(db_path)
    except sqlite3.DatabaseError as exc:
        print(f"SQLite error: {exc}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())



