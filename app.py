from flask import Flask, render_template, request, jsonify
from database import DatabaseConnector
from openai_api import OpenAIResponder
import os

# Configurar a chave da API OpenAI para demonstração
# IMPORTANTE: Em produção, use variáveis de ambiente ou um arquivo .env seguro
os.environ["OPENAI_API_KEY"] = "sk-demo-api-key-substitua-pela-sua-chave-real"  # Substitua pela sua chave real

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatpro-secret-key'

db_connector = DatabaseConnector()
openai_responder = OpenAIResponder()

@app.route('/')
def index():
    contacts = db_connector.get_contacts_last_24_hours()
    return render_template('index.html', contacts=contacts)

@app.route('/get_messages', methods=['POST'])
def get_messages():
    contact = request.form.get('contact')
    messages = db_connector.get_messages_last_24_hours()
    contact_messages = []
    
    for message in messages:
        if message[7] == contact:  # índice 7 corresponde à coluna 'number'
            contact_messages.append({
                'id': message[0],
                'message': message[9],  # índice 9 corresponde à coluna 'message'
                'timestamp': message[2]  # índice 2 corresponde à coluna 'event_ts'
            })
    
    return jsonify(contact_messages)

@app.route('/generate_response', methods=['POST'])
def generate_response():
    message = request.form.get('message')
    instructions = request.form.get('instructions', '')
    
    try:
        response = openai_responder.generate_response(message, instructions)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Erro na geração de resposta: {str(e)}")
        return jsonify({
            'response': "Olá! Agradeço pelo seu contato. Estamos verificando sua solicitação e retornaremos em breve.",
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5001)