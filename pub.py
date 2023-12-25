# Import libraries
import paho.mqtt.client as mqtt
import datetime
import os
import sys
import json
import time

# --------------------- MQTT Setup ---------------------
def on_connect(client, userdata, flags, rc):
    """
    Callback saat client menerima balasan CONNACK dari server (broker)

    rc: integer, result code dari percobaan koneksi ke server (broker)
    """
    if rc == 0:
        print("Tersambung dengan client")
    else:
        print(f"Koneksi error, dengan kode {rc}")


def on_message(client, userdata, message):
    """
    Callback saat pesan PUBLISH diterima dari server (broker)

    message: bytes, pesan yang diterima dari server (broker)
    """
    print(f"Pesan diterima: {message.topic} {message.payload.decode("utf-8")}")

# Membuat client Publisher
print("Membuat client baru (publisher)...")
client = mqtt.Client("Publisher")
client.on_connect = on_connect
client.on_message = on_message

# Menyambungkan client Publisher dengan broker hivemq pada port 1883
print("Menyambungkan ke broker...")
client.connect("broker.hivemq.com", 1883)
time.sleep(2)


# --------------------- Fungsi untuk Main Program ---------------------
clearScreen = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")

def validasiRute(idxAsal, idxTujuan):
    """
    Mengembalikan false jika asal sama dengan tujuan atau jika terdapat string kosong,
    true jika sebaliknya

    idxAsal: int, indeks bandara asal penerbangan
    idxTujuan: int, indeks bandara tujuan penerbangan
    """
    if ((idxAsal == idxTujuan) or ((idxAsal <= 0) and (idxAsal >= 10)) or ((idxTujuan <= 0) and (idxTujuan >= 10))):
        return False
    else:
        return True


def validasiTanggal(tanggal):
    """
    Mengembalikan true jika format tanggal sesuai (DD-MM-YYYY), false jika sebaliknya

    tanggal: string
    """
    try:
        datetime.datetime.strptime(tanggal, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def validasiWaktu(waktu):
    """
    Mengembalikan true jika format waktu sesuai (HH:MM), false jika sebaliknya

    waktu: string
    """
    try:
        datetime.datetime.strptime(waktu, "%H:%M")
        return True
    except ValueError:
        return False


def header():
    clearScreen()
    print("============= Program Jadwal Penerbangan =============\n")


def inputKode():
    """
    Mengembalikan kode penerbangan Lion Air yang didapat dari masukan user
    """
    header()
    print("---------- Menu Input Kode Penerbangan ----------\n")
    print("Contoh kode: '523'")

    kode = input("Masukkan kode penerbangan : ")
    while (kode in arrOfKode):
        print("Kode penerbangan telah digunakan")
        kode = input("Masukkan kode penerbangan : ")

    return "JT" + kode


def inputKota():
    """
    Mengembalikan kota asal dan kota tujuan penerbangan berdasarkan masukan user
    """
    header()
    print("---------- Menu Pemilihan Kota Asal & Tujuan ----------\n")

    # List kota
    i = 1
    for kota in arrOfKota:
        print(f"({i}) {kota}")
        i += 1

    idxKotaAsal = int(input("\nMasukkan nomor kota asal   : "))
    idxKotaTujuan = int(input("Masukkan nomor kota tujuan : "))

    while (validasiRute(idxKotaAsal, idxKotaTujuan) == False):
        print("Rute tidak valid, pastikan angka sudah sesuai!")
        time.sleep(5)

        header()
        print("---------- Menu Pemilihan Kota Asal & Tujuan ----------\n")    

        # List kota
        i = 1
        for kota in arrOfKota:
            print(f"({i}) {kota}")
            i += 1

        idxKotaAsal = int(input("\nMasukkan nomor kota asal   : "))
        idxKotaTujuan = int(input("Masukkan nomor kota tujuan : "))

    return idxKotaAsal-1, idxKotaTujuan-1

def inputJadwal():
    """
    
    """
    header()
    print("---------- Menu Input Jadwal ----------\n")

    # Input tanggal
    print("Contoh tanggal: 25-12-2023")
    tanggal = input("Masukkan tanggal penerbangan (dengan format DD-MM-YYYY) : ")
    while (validasiTanggal(tanggal) == False):
        print("Terdapat kesalahan input tanggal, pastikan format telah sesuai!")
        header()
        print("---------- Menu Input Jadwal ----------\n")
        print("Contoh tanggal: 25-12-2023")
        tanggal = input("Masukkan tanggal penerbangan (dengan format DD-MM-YYYY) : ")

    # Input waktu
    header()
    print("---------- Menu Input Jadwal ----------\n")
    print("Contoh waktu: 18:00")
    waktu = input("Masukkan waktu penerbangan (dengan format HH:MM) : ")
    while(validasiWaktu(waktu) == False):
        print("Terdapat kesalahan input waktu, pastikan format telah sesuai!")
        header()
        print("---------- Menu Input Jadwal ----------\n")
        print("Contoh waktu: 18:00")
        waktu = input("Masukkan waktu penerbangan (dengan format HH:MM) : ")

    return tanggal, waktu

def buatJadwal():
    global arrOfKode

    kode = inputKode()
    idxKotaAsal, idxKotaTujuan = inputKota()
    tanggal, waktu = inputJadwal()

    # Pengecekan konfirmasi
    header()
    print("---------- Menu Pembuatan Jadwal ----------\n")
    print("Berikut data jadwal penerbangan yang akan dibuat:\n")
    print(f"Kode    : {kode}")
    print(f"Asal    : {arrOfKota[idxKotaAsal]}")
    print(f"Tujuan  : {arrOfKota[idxKotaTujuan]}")
    print(f"Tanggal : {tanggal}")
    print(f"Waktu   : {waktu}")

    print("\nApakah data di atas sudah benar?")
    konfirm = input("n untuk Cancel, enter jika sudah benar : ")
    if (konfirm == "n"):
        print("\nPembuatan jadwal dibatalkan...")
        time.sleep(1)
    else:
        arrOfKode.append(kode)
        payload = formattingJadwalBaru(kode, idxKotaAsal, idxKotaTujuan, tanggal, waktu)
        arrOfMsgObj.append(payload)
        dataOut = json.dumps(payload)
        client.publish("my/LionAIR/Notifikasi", dataOut, 1)
        print("Notifikasi berhasil dikirimkan")
        time.sleep(2)

def formattingJadwalBaru(kode, idxKotaAsal, idxKotaTujuan, tanggal, waktu):
    waktuSekarang = datetime.datetime.now()
    waktuSekarang = waktuSekarang.strftime("%Y-%m-%d %H:%M:%S")

    jsonData = {"kode": kode,
                "kotaAsal": arrOfKota[idxKotaAsal],
                "kotaTujuan": arrOfKota[idxKotaTujuan],
                "tanggal": tanggal,
                "waktu": waktu,
                "dibuat": waktuSekarang,
                "diedit": "-"}

    return jsonData

def getNotifikasi():
    global arrOfMsgObj
    print("Terdapat " + str(len(arrOfMsgObj)) + " jadwal yang telah dibuat, yakni sebagai berikut:")
    for i in arrOfMsgObj:
        print("Kode penerbangan      : ", i["kode"])
        print("Asal                  : ", i["kotaAsal"])
        print("Tujuan                : ", i["kotaTujuan"])
        print("Tanggal Keberangkatan : ", i["tanggal"])
        print("Waktu Keberangkatan   : ", i["waktu"])
        print("Dibuat pada           : ", i["dibuat"])
        print("Terakhir diedit       : ", i["diedit"])
        print("-------------------------------------------")

    input("\nOk...")

def menu():
    header()
    print("(1) Buat jadwal penerbangan baru")
    print("(2) Perbarui jadwal penerbangan")
    print("(3) Lihat jadwal penerbangan")
    print("(0) Keluar dari program")

# --------------------- Main Program ---------------------
arrOfKode = []
arrOfMsgObj = []

arrOfKota = ["Jakarta    (Bandara Internasional Soekarno–Hatta)", 
             "Denpasar   (Bandara Internasional Ngurah Rai)", 
             "Surabaya   (Bandara Internasional Juanda)",
             "Makassar   (Bandara Internasional Sultan Hasanuddin)",
             "Medan      (Bandara Internasional Kualanamu)",
             "Yogyakarta (Bandara Internasional Adisutjipto)",
             "Batam      (Bandara Internasional Hang Nadim)",
             "Palembang  (Bandara Internasional Sultan Mahmud Badaruddin II)",
             "Bandung    (Bandara Internasional Kertajati)",
             "Bandung    (Bandara Internasional Kertajati)",]

menu()
inputMenu = int(input("\nPilihan menu : "))
while inputMenu != 0:
    match inputMenu:
        case 1:
            buatJadwal()
        case 2:
            pass
        case 3:
            pass
        case default:
            print("Masukan tidak valid, ulangi lagi.")
            time.sleep(1)

    menu()
    inputMenu = int(input("\nPilihan menu : "))

print("Keluar dari program ...")
sys.exit()
