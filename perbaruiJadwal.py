import os
import time
import validator
import datetime

clearScreen = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")


def header():
    clearScreen()
    print("============= Program Jadwal Penerbangan =============\n")


def perbaruiKode(kodeLama, arrOfKode):
    """
    Memperbarui kode penerbangan Lion Air yang didapat dari masukan user
    """
    header()
    print("---------- Menu Perbarui Kode Penerbangan ----------\n")
    print(f"Kode sekarang   : {kodeLama}")
    print("Contoh kode baru : '523'")

    kodeBaru = "JT" + input("Masukkan kode penerbangan baru : ")
    while kodeBaru in arrOfKode:
        print("\nKode penerbangan telah digunakan!")
        time.sleep(1)
        header()
        print("---------- Menu Input Kode Penerbangan ----------\n")
        print(f"Kode sekarang   : {kodeLama}")
        print("Contoh kode: '523'")
        kodeBaru = "JT" + input("Masukkan kode penerbangan baru : ")

    return kodeBaru


def perbaruiKota(kotaAsalLama, kotaTujuanLama, arrOfKota):
    """
    Memperbarui kota asal dan kota tujuan penerbangan berdasarkan masukan user
    """
    header()
    print("---------- Menu Perbarui Kota Asal & Tujuan ----------\n")
    print(f"Kota asal sekarang   : {kotaAsalLama}")
    print(f"Kota tujuan sekarang : {kotaTujuanLama}")

    # List kota
    i = 1
    for kota in arrOfKota:
        print(f"({i}) {kota}")
        i += 1

    idxAsalBaru = int(input("\nMasukkan nomor kota asal baru   : ")) - 1
    idxTujuanBaru = int(input("Masukkan nomor kota tujuan baru : ")) - 1

    while validator.validasiRute(idxAsalBaru, idxTujuanBaru, arrOfKota) == False:
        print("Rute tidak valid, pastikan angka sudah sesuai!")
        time.sleep(1)

        header()
        print("---------- Menu Perbarui Kota Asal & Tujuan ----------\n")
        print(f"Kota asal sekarang   : {kotaAsalLama}")
        print(f"Kota tujuan sekarang : {kotaTujuanLama}")

        # List kota
        i = 1
        for kota in arrOfKota:
            print(f"({i}) {kota}")
            i += 1

        idxAsalBaru = int(input("\nMasukkan nomor kota asal baru   : ")) - 1
        idxTujuanBaru = int(input("Masukkan nomor kota tujuan baru : ")) - 1

    return idxAsalBaru, idxTujuanBaru


def perbaruiTanggalWaktu(tanggalLama, waktuLama):
    """
    Memperbarui tanggal dan waktu penerbangan
    """
    # Perbarui jadwal
    header()
    print("---------- Menu Perbarui Jadwal ----------\n")
    print(f"Tanggal sekarang : {tanggalLama}")
    print("Contoh tanggal: 25-12-2023")
    tanggalBaru = input(
        "Masukkan tanggal penerbangan baru (dengan format DD-MM-YYYY) : "
    )
    while validator.validasiTanggal(tanggalBaru) == False:
        print("Terdapat kesalahan input tanggal, pastikan format telah sesuai!")
        header()
        print("---------- Menu Perbarui Jadwal ----------\n")
        print(f"Tanggal sekarang : {tanggalLama}")
        print("Contoh tanggal: 25-12-2023")
        tanggalBaru = input(
            "Masukkan tanggal penerbangan baru (dengan format DD-MM-YYYY) : "
        )

    # Perbarui waktu
    header()
    print("---------- Menu Perbarui Jadwal ----------\n")
    print(f"Waktu sekarang : {waktuLama}")
    print("Contoh waktu: 18:00")
    waktuBaru = input("Masukkan waktu penerbangan (dengan format HH:MM) : ")
    while validator.validasiWaktu(waktuBaru) == False:
        print("Terdapat kesalahan input waktu, pastikan format telah sesuai!")
        header()
        print("---------- Menu Perbarui Jadwal ----------\n")
        print(f"Waktu sekarang : {waktuLama}")
        print("Contoh waktu: 18:00")
        waktuBaru = input("Masukkan waktu penerbangan (dengan format HH:MM) : ")

    return tanggalBaru, waktuBaru


def perbarui(kode, arrOfKode, arrOfKota, arrOfMsgObj):
    for i in arrOfMsgObj:
        if i["kode"] == kode:
            header()
            print("---------- Menu Perbarui ----------\n")
            print(f"Kode sekarang : {i["kode"]}")
            inputMenu = input("Perbarui kode? (Y) untuk iya : ")
            if inputMenu == "Y" or inputMenu == "y":
                i["kode"] = perbaruiKode(i["kode"], arrOfKode)

            header()
            print("---------- Menu Perbarui ----------\n")
            print(f"Kota asal sekarang   : {i["kotaAsal"]}")
            print(f"Kota tujuan sekarang : {i["kotaTujuan"]}")
            inputMenu = input("Perbarui kota asal/tujuan? (Y) untuk iya : ")
            if inputMenu == "Y" or inputMenu == "y":
                idxKotaAsal, idxKotaTujuan = perbaruiKota(i["kotaAsal"], i["kotaTujuan"], arrOfKota)
                i["kotaAsal"] = arrOfKota[idxKotaAsal]
                i["kotaTujuan"] = arrOfKota[idxKotaTujuan]

            header()
            print("---------- Menu Perbarui ----------\n")
            print(f"Tanggal sekarang : {i["tanggal"]}")
            print(f"Waktu sekarang : {i["waktu"]}")
            inputMenu = input("Perbarui tanggal/waktu? (Y) untuk iya : ")
            if inputMenu == "Y" or inputMenu == "y":
                i["tanggal"], i["waktu"] = perbaruiTanggalWaktu(i["tanggal"], i["waktu"])
           
            waktuSekarang = datetime.datetime.now()
            waktuSekarang = waktuSekarang.strftime("%Y-%m-%d %H:%M:%S")
            i["diedit"] = waktuSekarang
