import sqlite3

from database import get_connection, init_database


def _row_to_dict(row: sqlite3.Row) -> dict:
    return {
        'id': row['id'],
        'descripcion': row['descripcion'],
        'monto': row['monto'],
        'categoria': row['categoria'],
        'created_at': row['created_at'],
    }


class GastoRepository:
    """Persistencia SQLite para gastos del CRUD."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        init_database(db_path)

    def list_all(self) -> list[dict]:
        with get_connection(self._db_path) as conn:
            rows = conn.execute(
                'SELECT id, descripcion, monto, categoria, created_at '
                'FROM gastos ORDER BY id ASC'
            ).fetchall()
        return [_row_to_dict(r) for r in rows]

    def get_by_id(self, gasto_id: int) -> dict | None:
        with get_connection(self._db_path) as conn:
            row = conn.execute(
                'SELECT id, descripcion, monto, categoria, created_at '
                'FROM gastos WHERE id = ?',
                (gasto_id,),
            ).fetchone()
        return _row_to_dict(row) if row else None

    def exists(self, gasto_id: int) -> bool:
        with get_connection(self._db_path) as conn:
            row = conn.execute(
                'SELECT 1 FROM gastos WHERE id = ?', (gasto_id,)
            ).fetchone()
        return row is not None

    def create(
        self,
        *,
        descripcion: str,
        monto: float,
        categoria: str,
        gasto_id: int | None = None,
    ) -> dict:
        with get_connection(self._db_path) as conn:
            if gasto_id is not None:
                conn.execute(
                    'INSERT INTO gastos (id, descripcion, monto, categoria) '
                    'VALUES (?, ?, ?, ?)',
                    (gasto_id, descripcion, monto, categoria),
                )
                new_id = gasto_id
            else:
                cur = conn.execute(
                    'INSERT INTO gastos (descripcion, monto, categoria) '
                    'VALUES (?, ?, ?)',
                    (descripcion, monto, categoria),
                )
                new_id = int(cur.lastrowid)
            conn.commit()
            row = conn.execute(
                'SELECT id, descripcion, monto, categoria, created_at '
                'FROM gastos WHERE id = ?',
                (new_id,),
            ).fetchone()
        return _row_to_dict(row)

    def update(self, gasto_id: int, fields: dict) -> dict | None:
        if not fields:
            return self.get_by_id(gasto_id)

        columns = []
        values: list = []
        for key in ('descripcion', 'monto', 'categoria'):
            if key in fields:
                columns.append(f'{key} = ?')
                values.append(fields[key])
        if not columns:
            return self.get_by_id(gasto_id)

        values.append(gasto_id)
        sql = f"UPDATE gastos SET {', '.join(columns)} WHERE id = ?"

        with get_connection(self._db_path) as conn:
            cur = conn.execute(sql, values)
            conn.commit()
            if cur.rowcount == 0:
                return None
        return self.get_by_id(gasto_id)

    def delete(self, gasto_id: int) -> dict | None:
        gasto = self.get_by_id(gasto_id)
        if gasto is None:
            return None
        with get_connection(self._db_path) as conn:
            conn.execute('DELETE FROM gastos WHERE id = ?', (gasto_id,))
            conn.commit()
        return gasto
