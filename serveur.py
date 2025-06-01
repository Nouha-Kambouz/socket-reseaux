import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 65432

questions = [
    {"question": "Quelle est la fonction principale du protocole TCP ? ?", "choices": [" Transmission fiable", "Attribution IP", "Cryptage données"], "answer": "A"},
    {"question": "Quel port est utilisé par défaut pour HTTP ?", "choices": ["40", "80", "90"], "answer": "B"},
    {"question": "Que fait la commande traceroute avec TTL ?", "choices": ["Incrémente TTL", "Ignore TTL", "Chiffre données"], "answer": "A"},
]

clients = []

def handle_client(conn, addr):
    score = 0
    try:
        for q in questions:
            
            conn.sendall(json.dumps(q).encode())

            
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            if data.upper() == q["answer"]:
                score += 1
        
        conn.sendall(f"Votre score est : {score} / {len(questions)}".encode())
    except:
        pass
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Serveur en écoute...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connexion de {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
