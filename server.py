import socket
import sys
import threading

# Fonction pour gérer chaque connexion client
def handle_client_message(client_socket, client_address, display_ports):
    while True:
        try:
            # Recevoir un message du client
            message = client_socket.recv(1024)
            if not message:
                break

            # Envoie le message reçu à tous les serveurs d'affichage
            for port in display_ports:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect(("localhost", port))
                        s.send(message)
                    except Exception as e:
                        print(f"Erreur lors de l'envoi au port {port}: {e}")
        except Exception as e:
            print(f"Une erreur s'est produite: {e}")
            break

    print(f"Connexion fermée avec {client_address}")
    client_socket.close()

# Fonction principale du serveur
def main():
    if len(sys.argv) < 3 :
        print("Usage: {} port_local port1 port2 port3".format(sys.argv[0]))
        sys.exit(1)

    port_local = int(sys.argv[1])
    ports_display = [int(port) for port in sys.argv[2:]]

    # Créer un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur_socket:
        # Autoriser la réutilisation de l'adresse
        serveur_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Lier le socket au port
        serveur_socket.bind(('', port_local))
        # Écouter les connexions entrantes
        serveur_socket.listen(5)
        print("Serveur en écoute sur le port {}...".format(port_local))

        try:
            # Accepter les connexions des clients
            while True:
                client_socket, client_address = serveur_socket.accept()
                print("Connexion de", client_address)

                # Démarrer un nouveau thread pour gérer la connexion client
                client_thread = threading.Thread(target=handle_client_message, args=(client_socket, client_address, ports_display))
                client_thread.start()

        except KeyboardInterrupt:
            print("Serveur arrêté")

main()
