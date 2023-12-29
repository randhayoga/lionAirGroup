# Import libraries
import paho.mqtt.client as mqtt
import buatJadwal
import perbaruiJadwal
import os
import sys
import json
import time
import datetime

# --------------------- MQTT Setup ---------------------
def on_connect(client, userdata, flags, rc):
    """
    Callback saat client menerima balasan CONNACK dari server (broker)

    rc: integer, result code dari percobaan koneksi ke server (broker)
    """
    if rc == 0:
        print("Tersambung dengan client wkwkw dari")
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
client = mqtt.Client("Publisher", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message


# Menghidupkan TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("admin", "Adm1nAdm1n")


# Menyambungkan client Publisher dengan broker hivemq pada port 8883
print("Menyambungkan ke broker...")
client.connect("431e1591f5c743efa435fc1f6fcc032b.s1.eu.hivemq.cloud", 8883)
time.sleep(2)


# --------------------- Fungsi untuk Main Program ---------------------
clearScreen = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")


def resetConnection():
    client.disconnect()
    client.connect("431e1591f5c743efa435fc1f6fcc032b.s1.eu.hivemq.cloud", 8883)

def header():
    clearScreen()
    print("============= Program Jadwal Penerbangan =============\n")


def menuBuatJadwal():
    """
    Membuat jadwal penerbangan baru secara lengkap dan menyimpannya ke dalam 
    sebuah array
    """
    global arrOfKode, arrOfMsgObj

    kode = buatJadwal.inputKode()
    idxKotaAsal, idxKotaTujuan = buatJadwal.inputKota(arrOfKota)
    tanggal, waktu = buatJadwal.inputTanggalWaktu()

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
        time.sleep(2)
    else:
        arrOfKode.append(kode)
        payload = buatJadwal.formattingJadwalBaru(kode, idxKotaAsal, idxKotaTujuan, tanggal, waktu, arrOfKota)
        isSend = True

        for i in arrOfMsgObj:
            if i["tanggal"] == tanggal and i["waktu"] == waktu and i["kotaAsal"] == arrOfKota[idxKotaAsal] and i["kotaTujuan"] == arrOfKota[idxKotaTujuan]:
                isSend = False

        if isSend:
            arrOfMsgObj.append(payload)
            dataOut = json.dumps(payload)
            client.publish("lionAir/Notif", dataOut, 1)
            print("Notifikasi berhasil dikirimkan")

        else:
            print("Notifikasi tidak dikirimkan karena terdapat jadwal boarding dan lokasi transit yang sama")
        time.sleep(2)


def menuPerbaruiJadwal():
    """
    Memperbarui jadwal penerbangan berdasarkan masukan dari user 
    """
    global arrOfKode

    header()
    print("---------- Perbarui Jadwal ----------\n")

    kode = input("Masukkan (Y) jika Anda ingin melihat seluruh jadwal terlebih dahulu : ")
    if kode == "Y":
        printAllJadwal()

    header()
    print("---------- Perbarui Jadwal ----------\n")
    kode = input("Masukkan kode dari jadwal yang ingin diperbarui : ")
    while (kode not in arrOfKode):
        print("\nKode jadwal tidak ditemukan! Ulangi masukan dengan data yang benar")
        time.sleep(2)

        header()
        print("---------- Perbarui Jadwal ----------\n")
        kode = input("Masukkan (Y) jika Anda ingin melihat seluruh jadwal terlebih dahulu : ")
        if kode == "Y":
            printAllJadwal()
        
        header()
        print("---------- Perbarui Jadwal ----------\n")
        kode = "JT" + input("Masukkan kode dari jadwal yang ingin diperbarui : ")

    for i in arrOfMsgObj:
        if i["kode"] == kode:
            notifBaru = "Terdapat jadwal penerbangan yang diperbarui!"
            kodeBaru = kode
            tanggalBaru = i["tanggal"]
            waktuBaru = i["waktu"]
            kotaAsalBaru = i["kotaAsal"]
            kotaTujuanBaru = i["kotaTujuan"]

            header()
            print("---------- Menu Perbarui ----------\n")
            print(f"Kode sekarang : {i["kode"]}")
            inputMenu = input("Perbarui kode? (Y) untuk iya : ")
            if inputMenu == "Y" or inputMenu == "y":
                kodeBaru = perbaruiJadwal.perbaruiKode(i["kode"], arrOfKode)

            header()
            print("---------- Menu Perbarui ----------\n")
            print(f"Kota asal sekarang   : {i["kotaAsal"]}")
            print(f"Kota tujuan sekarang : {i["kotaTujuan"]}")
            inputMenu = input("Perbarui kota asal/tujuan? (Y) untuk iya : ")
            if inputMenu == "Y" or inputMenu == "y":
                idxKotaAsal, idxKotaTujuan = perbaruiJadwal.perbaruiKota(i["kotaAsal"], i["kotaTujuan"], arrOfKota)
                kotaAsalBaru = arrOfKota[idxKotaAsal]
                kotaTujuanBaru = arrOfKota[idxKotaTujuan]

            header()
            print("---------- Menu Perbarui ----------\n")
            print(f"Tanggal sekarang : {i["tanggal"]}")
            print(f"Waktu sekarang : {i["waktu"]}")
            inputMenu = input("Perbarui tanggal/waktu? (Y) untuk iya : ")
            if inputMenu == "Y" or inputMenu == "y":
                tanggalBaru, waktuBaru = perbaruiJadwal.perbaruiTanggalWaktu(i["tanggal"], i["waktu"])
           
            waktuSekarang = datetime.datetime.now()
            waktuSekarang = waktuSekarang.strftime("%Y-%m-%d %H:%M:%S")

            # Mengecek apakah sudah ada data boarding dan transit yang sama
            isSend = True
            for i in arrOfMsgObj:
                if i["tanggal"] == tanggalBaru and i["waktu"] == waktuBaru and i["kotaAsal"] == kotaAsalBaru and i["kotaTujuan"] == kotaTujuanBaru:
                    isSend = False

            if isSend:
                i["notif"] = notifBaru
                i["kode"] = kodeBaru
                i["kotaAsal"] = kotaAsalBaru
                i["kotaTujuan"] = kotaTujuanBaru
                i["tanggal"] = tanggalBaru
                i["waktu"] = waktuBaru
                i["diedit"] = waktuSekarang

                dataOut = json.dumps(i)
                client.publish("lionAir/Notif", dataOut, 1)
                print("Notifikasi berhasil dikirimkan")
            else:
                
                print("Perubahan tidak disimpan dan notifikasi tidak dikirimkan karena terdapat jadwal boarding dan lokasi transit yang sama")

            time.sleep(2)


def printAllJadwal():
    """
    Mencetak semua jadwal yang telah dibuat
    """
    global arrOfMsgObj

    header()
    print("---------- Daftar Jadwal ----------\n")

    print("Terdapat " + str(len(arrOfMsgObj)) + " jadwal yang telah dibuat, yakni sebagai berikut:\n")
    print("\n-------------------------------------------\n")
    for i in arrOfMsgObj:
        print("kode penerbangan      : ", i["kode"])
        print("asal                  : ", i["kotaAsal"])
        print("tujuan                : ", i["kotaTujuan"])
        print("tanggal keberangkatan : ", i["tanggal"])
        print("waktu keberangkatan   : ", i["waktu"])
        print("dibuat pada           : ", i["dibuat"])
        print("terakhir diedit       : ", i["diedit"])
        print("\n-------------------------------------------\n")

    input("Ok...")


def menu():
    """
    Menu sederhana untuk mengontrol flow aplikasi
    """
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
             "Yogyakarta (Bandara Internasional Yogyakarta)",
             "Batam      (Bandara Internasional Hang Nadim)",
             "Palembang  (Bandara Internasional Sultan Mahmud Badaruddin II)",
             "Semarang   (Bandara Internasional Jenderal Ahmad Yani)",
             "Bandung    (Bandara Internasional Kertajati)",
             "Pontianak  (Bandara Internasional Supadio)",
             "Mataram    (Bandara Zainuddin Abdul Madjid)",]

menu()
inputMenu = int(input("\nPilihan menu : "))
while inputMenu != 0:
    match inputMenu:
        case 1:
            menuBuatJadwal()
        case 2:
            menuPerbaruiJadwal()
        case 3:
            printAllJadwal()
        case default:
            print("Masukan tidak valid, ulangi lagi.")
            time.sleep(2)

    menu()
    inputMenu = int(input("\nPilihan menu : "))

print("Keluar dari program ...")
sys.exit()
