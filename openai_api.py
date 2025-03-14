import openai
import os

class OpenAIResponder:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not os.getenv("OPENAI_API_KEY"):
            print("AVISO: A chave da API OpenAI não está definida. Defina a variável de ambiente OPENAI_API_KEY.")

    def generate_response(self, message, instructions=""):
        try:
            prompt = f"Responda à seguinte mensagem de um cliente de forma curta e cordial, adequada para WhatsApp: '{message}'. {instructions}"
            
            # Usando a versão 0.27.0 da API OpenAI
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=60
            )
            
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            # Resposta de fallback caso a API falhe
            return "Olá! Agradeço pelo seu contato. Estamos verificando sua solicitação e retornaremos em breve."