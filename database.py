import sqlite3
from datetime import datetime, timedelta

class DatabaseConnector:
    def __init__(self, db_name='../messages_20250313_010002.db'):
        self.db_name = db_name

    def _get_connection(self):
        # Cria uma nova conexão para cada operação
        return sqlite3.connect(self.db_name)

    def get_messages_last_24_hours(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        query = """
        SELECT * FROM messages WHERE event_ts >= datetime('now', '-1 day')
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def get_contacts_last_24_hours(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        query = """
        SELECT DISTINCT number FROM messages WHERE event_ts >= datetime('now', '-1 day')
        """
        cursor.execute(query)
        result = [row[0] for row in cursor.fetchall()]
        conn.close()
        return result