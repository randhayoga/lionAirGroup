# Import libraries
import paho.mqtt.client as mqtt
import os
import sys
import json
import time
import requests
import datetime
from threading import Thread


# --------------------- MQTT Setup ---------------------
def on_connect(client, userdata, flags, rc):
    """
    Callback saat client menerima balasan CONNACK dari server (broker)

    rc: integer, result code dari percobaan koneksi ke server (broker)
    """
    if rc == 0:
        print("Tersambung dengan client\n")
    else:
        print(f"Koneksi error, dengan kode {rc}")


def on_message(client, userdata, message):
    """
    Callback saat pesan PUBLISH diterima dari server (broker)

    message: bytes, pesan yang diterima dari server (broker)
    """
    print(f"Notifikasi baru masuk dari LionAir pada topic : {message.topic}")
    jsonData = message.payload.decode("utf-8")
    messageObj = json.loads(jsonData)

    if cekKode(messageObj["kode"]):
        print(f"Notifkasi masuk dengan kode penerbangan : {messageObj["kode"]}")
        print("Kode penerbangan telah tersedia")
        time.sleep(2)
        client.disconnect()
    else:
        print(messageObj["notif"])
        print("kode penerbangan      : ", messageObj["kode"])
        print("asal                  : ", messageObj["kotaAsal"])
        print("tujuan                : ", messageObj["kotaTujuan"])
        print("tanggal keberangkatan : ", messageObj["tanggal"])
        print("waktu keberangkatan   : ", messageObj["waktu"])
        print("dibuat pada           : ", messageObj["dibuat"])
        print("terakhir diedit       : ", messageObj["diedit"])

        waktuTerima = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with open("boarding.txt", "a") as f:
            f.write("Kode Penerbangan : "+messageObj["kode"]+"\n"
                    "Tanggal Keberangkatan : "+messageObj["tanggal"]+"\n"
                    "Diterima pada : "+ waktuTerima +"\n\n")

        with open('lokasi.txt', 'a') as f:
            f.write("Kode Penerbangan : "+messageObj["kode"]+"\n"
                    "Asal : "+messageObj["kotaAsal"]+"\n"
                    "Tujuan : "+messageObj["kotaTujuan"]+"\n"
                    "Diterima pada : "+ waktuTerima +"\n\n")

        print("File boarding.txt dan lokasi.txt telah diperbarui\n")

        global arrOfMsgObj
        arrOfMsgObj.append(messageObj)


# Membuat client Publisher
print("Membuat client baru (subscriber)...")
client = mqtt.Client("Subscriber", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

# Menghidupkan TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("admin", "Adm1nAdm1n")

# Menyambungkan client Publisher dengan broker hivemq pada port 1883
print("Menyambungkan ke broker...")
client.connect("431e1591f5c743efa435fc1f6fcc032b.s1.eu.hivemq.cloud", 8883)
client.subscribe("lionAir/Notif", 1)

# --------------------- Fungsi untuk Main Program ---------------------
clearScreen = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")


def header():
    clearScreen()
    print("============= Program Penerima Jadwal Penerbangan =============\n")


def cekKode(kode):
    """
    Mengecek apakah kode penerbangan tertentu sudah pernah diterima 
    notifikasinya

    kode: string, kode penerbangan dari message yang diterima dari pub
    """
    global arrOfMsgObj
    for messageObj in arrOfMsgObj:
        if kode in messageObj["kode"]:
            return True
        else:
            return False


def menu():
    """
    Menu sederhana untuk mengontrol flow aplikasi
    """
    header()
    print("(1) Dapatkan notifikasi")
    print("(0) Keluar dari program")


def inputStop():
    """
    Menghentikan input dan memutuskan koneksi klien
    """
    input()
    client.disconnect()

def loopForever():
    """
    Menghubungkan klien sub ke broker dan menjalankan klien secara terus-menerus.
    """
    client.connect("431e1591f5c743efa435fc1f6fcc032b.s1.eu.hivemq.cloud", 8883)
    clearScreen()
    client.loop_forever()


def fetchNotifikasi():
    """
    Memulai dua thread untuk mendapatkan notifikasi secara real-time, yaitu 
    loopForever() dan inputStop().
    """
    print("Hint: tekan enter, jika ingin keluar dari program")
    Thread(target = loopForever).start()
    Thread(target = inputStop).start()


def switchMenu(inputan):
    """
    Logika pemilihan untuk menu sederhana
    """
    if inputan=='1':
        fetchNotifikasi()
    else:
        inputan=='0'

# --------------------- Main -------------------------
arrOfMsgObj = []

menu()
menuInput = input("\nPilihan menu : ")
while (menuInput != '0'):
    switchMenu(menuInput)
    menu()
    menuInput = input("\nPilihan menu : ")

print("Keluar dari program ...")
sys.exit()
