import socket
import threading
import json
import customtkinter as ctk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 65432

class QCMClient:
    def __init__(self, master):
        self.master = master
        master.title(" QCM Client")
        master.geometry("450x350")
        master.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.question_label = ctk.CTkLabel(master, text="En attente de la question...", font=("Arial", 16), wraplength=400)
        self.question_label.pack(pady=(20,10))

        self.choice_var = ctk.StringVar(value="")

        self.radio_buttons = []
        for i in range(3):
            rb = ctk.CTkRadioButton(master, text=f"Choix {i+1}", variable=self.choice_var, value=chr(65+i))
            rb.pack(anchor="w", padx=40, pady=5)
            self.radio_buttons.append(rb)

        self.send_button = ctk.CTkButton(master, text="Envoyer", command=self.send_answer, state='disabled')
        self.send_button.pack(pady=20)

        self.status_label = ctk.CTkLabel(master, text="", font=("Arial", 12))
        self.status_label.pack()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            messagebox.showerror("Erreur de connexion", "⚠️ Serveur non disponible.")
            master.destroy()
            return

        threading.Thread(target=self.receive_questions, daemon=True).start()

    def receive_questions(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                try:
                    q = json.loads(data)
                    self.show_question(q)
                except json.JSONDecodeError:
                    self.status_label.configure(text=data)
                    self.send_button.configure(state='disabled')
                    self.disable_choices()
                    break
            except:
                break

    def show_question(self, q):
        self.question_label.configure(text=q['question'])
        self.choice_var.set("")  
        for i, choice_text in enumerate(q['choices']):
            self.radio_buttons[i].configure(text=choice_text)
        self.send_button.configure(state='normal')
        self.enable_choices()

    def send_answer(self):
        answer = self.choice_var.get()
        if not answer:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une réponse.")
            return
        self.client_socket.sendall(answer.encode())
        self.send_button.configure(state='disabled')
        self.disable_choices()
        self.status_label.configure(text="Réponse envoyée, en attente...")

    def disable_choices(self):
        for rb in self.radio_buttons:
            rb.configure(state='disabled')

    def enable_choices(self):
        for rb in self.radio_buttons:
            rb.configure(state='normal')


if __name__ == "__main__":
    app = ctk.CTk()
    QCMClient(app)
    app.mainloop()
