# On commence par importer les modules dont on a besoin
import machine
import time
import network
import requests
import json

# Adresse de la girouette (0 : grande girouette avant 200×24, 1 : petite girouette côté, 2 : très petite girouette arrière)
display_address = 0

# Initialiser la communication avec le module RS485
uart = machine.UART(1, baudrate=4800, bits=8, parity=None, stop=1)

# On spécifie les informations du réseau wifi
# (remplacez "mon_reseau" et "mon_mot_de_passe" 
# par les informations de votre réseau)
ssid = "mon_reseau"
password = "mon_mot_de_passe"

def byte_to_ascii(value):
    return f"{value:02X}"

def print_message(message):
    buff = bytearray(512)

    buff[0] = 0x02                   # Caractère de début
    buff[1] = 0x30                   # Adresse b1
    buff[2] = 0x30 + display_address # Adresse b2

    for i in range(len(message)):
        buff[3 + i] = ord(message[i])

    sum_value = buff[0] + buff[1] + buff[2]
    for i in range(len(message)):
        sum_value += buff[3 + i]
    buff[3 + len(message) + 0] = 0x03  # Caractère de fin
    sum_value += 1

    sum_value &= 0xFF
    crc = (sum_value ^ 255) + 1  # xor+1
    ascii_crc = byte_to_ascii(crc)
    buff[3 + len(message) + 1] = int(ascii_crc[0], 16)
    buff[3 + len(message) + 2] = int(ascii_crc[1], 16)

    uart.write(buff)

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connexion au réseau...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Configuration du réseau:', wlan.ifconfig())

def fetch_json(url):
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Échec de la récupération des données : Code de statut {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
    return None

def main():
    display_setup()
    connect_wifi(SSID, PASSWORD)

    url = "http://<votre_serveur>/messages.json"
    while True:
        json_data = fetch_json(url)
        if json_data:
            for message in json_data.get('messages', []):
                text = message.get('text', '')
                print_message(text)
                time.sleep(10)  # Afficher chaque message pendant 10 secondes
        else:
            print("Aucune donnée reçue, nouvelle tentative dans 10 secondes...")
            time.sleep(10)

if __name__ == "__main__":
    main()
    
    
# On vient créer une instance de l'interface wifi en mode station
sta_if = network.WLAN(network.STA_IF)

# On active l'interface wifi
sta_if.active(True)

# Et on se connecte au réseau wifi
print(f"Connexion au réseau {ssid}...", end="")
if not sta_if.isconnected():
  sta_if.connect(ssid, password)
  while not sta_if.isconnected():
    print(".", end="")
    time.sleep(1)
    
# On affiche que la connexion a bien été établie
print(f"\nConnecté au réseau {ssid} !")
print(f"Adresse IP : {sta_if.ifconfig()[0]}")

while True:
    # On vérifie si la connexion est toujours active
    if not sta_if.isconnected():
        print('Reconnexion au réseau...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(1)
        print(f"\nReconnecté au réseau {ssid} !")
        print(f"Adresse IP : {sta_if.ifconfig()[0]}")

    r = requests.get("https://girouettes.labfab.fr/messages.json")

    # On affiche la réponse du serveur si le code HTTP est 200 (OK)
    if r.status_code == 200:
        # On affiche la réponse du serveur au format JSON
        print(f"Réponse du serveur : {r.json()}")
        
        # On affiche chaque message pendant le temps spécifié 
        for message in messages:
            text = message.get('text', '')
            duration = message.get('duration', 10)
            print(f"{text} pendant {duration}s")
            display_carousel(text)
            time.sleep(duration)