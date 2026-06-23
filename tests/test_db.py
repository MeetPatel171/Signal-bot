"""init_db creates all expected tables; foreign keys + WAL are on."""
from signal_bot import db


def test_init_db_creates_all_tables(tmp_path):
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    with db.get_connection(db_path) as conn:
        tables = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    assert {"positions", "orders", "position_updates", "reader_state"} <= tables


def test_pragmas_on(tmp_path):
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    with db.get_connection(db_path) as conn:
        assert conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1


def test_init_db_is_idempotent(tmp_path):
    db_path = tmp_path / "test.db"
    db.init_db(db_path)
    db.init_db(db_path)  # should not raise
