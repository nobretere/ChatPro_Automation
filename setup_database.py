import sqlite3
import datetime

# Conectar ao banco de dados
conn = sqlite3.connect('../messages_20250313_010002.db')
cursor = conn.cursor()

# Criar tabela messages
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT,
    event_ts TEXT,
    message_id TEXT UNIQUE,
    instance_id TEXT,
    session_id TEXT,
    lead_id TEXT,
    number TEXT,
    from_me INTEGER,
    message TEXT,
    message_type TEXT,
    file_path TEXT,
    original_url TEXT,
    user_name TEXT
)
''')

# Data atual para as mensagens
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
one_hour_ago = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
two_hours_ago = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

# Inserir dados de exemplo
messages_data = [
    ('message_received', current_time, 'msg1', 'inst1', 'sess1', 'lead1', '+5511999999999', 0, 'Olá, gostaria de saber o status do meu pedido #12345', 'text', None, None, 'João'),
    ('message_received', one_hour_ago, 'msg2', 'inst1', 'sess1', 'lead1', '+5511999999999', 0, 'Já faz uma semana que fiz o pedido e ainda não recebi', 'text', None, None, 'João'),
    ('message_received', two_hours_ago, 'msg3', 'inst2', 'sess2', 'lead2', '+5511888888888', 0, 'Preciso de ajuda com o produto que comprei, ele não está funcionando corretamente', 'text', None, None, 'Maria'),
    ('message_received', current_time, 'msg4', 'inst2', 'sess2', 'lead2', '+5511888888888', 0, 'Tentei seguir o manual mas não consegui resolver o problema', 'text', None, None, 'Maria'),
]

# Inserir os dados na tabela
for message in messages_data:
    try:
        cursor.execute('''
        INSERT INTO messages (event, event_ts, message_id, instance_id, session_id, lead_id, number, from_me, message, message_type, file_path, original_url, user_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', message)
    except sqlite3.IntegrityError:
        # Ignorar erros de duplicação de message_id
        pass

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados configurado com sucesso!")