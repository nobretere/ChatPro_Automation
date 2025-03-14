import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from database import DatabaseConnector
from openai_api import OpenAIResponder

class ChatProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatPro - Atendimento via WhatsApp")

        self.db_connector = DatabaseConnector()
        self.openai_responder = OpenAIResponder()

        self.create_widgets()

    def create_widgets(self):
        # Dropdown de contatos
        self.contacts = self.db_connector.get_contacts_last_24_hours()
        self.contact_var = tk.StringVar()
        self.contact_dropdown = ttk.Combobox(self.root, textvariable=self.contact_var, values=self.contacts)
        self.contact_dropdown.grid(row=0, column=0, padx=10, pady=10)

        # Campo de instruções
        self.instruction_label = tk.Label(self.root, text="Instruções para a resposta:")
        self.instruction_label.grid(row=1, column=0, padx=10, pady=5)
        self.instruction_entry = tk.Entry(self.root, width=50)
        self.instruction_entry.grid(row=1, column=1, padx=10, pady=5)

        # Frame para mensagens e respostas
        self.messages_frame = tk.Frame(self.root)
        self.messages_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        # Área de mensagens
        self.messages_text = tk.Text(self.messages_frame, width=80, height=20)
        self.messages_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para a área de mensagens
        scrollbar = tk.Scrollbar(self.messages_frame, command=self.messages_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.messages_text.config(yscrollcommand=scrollbar.set)

        # Botão Gerar Resposta
        self.generate_button = tk.Button(self.root, text="Gerar Resposta", command=self.generate_response)
        self.generate_button.grid(row=3, column=0, padx=10, pady=10)

    def generate_response(self):
        selected_contact = self.contact_var.get()
        if not selected_contact:
            messagebox.showwarning("Aviso", "Por favor, selecione um contato.")
            return
            
        instructions = self.instruction_entry.get()
        messages = self.db_connector.get_messages_last_24_hours()
        
        # Limpar área de mensagens
        self.messages_text.delete(1.0, tk.END)
        
        for message in messages:
            # Verificando se o número do contato corresponde ao selecionado
            if message[7] == selected_contact:  # índice 7 corresponde à coluna 'number'
                # índice 9 corresponde à coluna 'message'
                client_message = message[9]
                response = self.openai_responder.generate_response(client_message, instructions)
                
                # Adicionar mensagem e resposta à área de texto
                self.messages_text.insert(tk.END, f"Mensagem: {client_message}\n", "message")
                self.messages_text.insert(tk.END, f"Resposta: {response}\n", "response")
                
                # Adicionar botão de copiar
                copy_button = tk.Button(self.messages_text, text="Copiar", 
                                       command=lambda r=response: self.copy_to_clipboard(r))
                self.messages_text.window_create(tk.END, window=copy_button)
                self.messages_text.insert(tk.END, "\n\n")
                
        # Configurar tags para formatação
        self.messages_text.tag_configure("message", foreground="blue")
        self.messages_text.tag_configure("response", foreground="green")
    
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        messagebox.showinfo("Copiado", "Resposta copiada para a área de transferência!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatProApp(root)
    root.mainloop()