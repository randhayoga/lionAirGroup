import os
import time
import datetime
import validator

clearScreen = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")


def header():
    clearScreen()
    print("============= Program Jadwal Penerbangan =============\n")


def inputKode(arrOfKode):
    """
    Mengembalikan kode penerbangan Lion Air yang didapat dari masukan user
    """
    header()
    print("---------- Menu Input Kode Penerbangan ----------\n")
    print("Contoh kode: '523'")

    kode = "JT" + input("Masukkan kode penerbangan : ")

    return kode


def inputKota(arrOfKota):
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

    idxKotaAsal = int(input("\nMasukkan nomor kota asal   : ")) - 1
    idxKotaTujuan = int(input("Masukkan nomor kota tujuan : ")) - 1

    while validator.validasiRute(idxKotaAsal, idxKotaTujuan, arrOfKota) == False:
        print("Rute tidak valid, pastikan angka sudah sesuai!")
        time.sleep(1)

        header()
        print("---------- Menu Pemilihan Kota Asal & Tujuan ----------\n")

        # List kota
        i = 1
        for kota in arrOfKota:
            print(f"({i}) {kota}")
            i += 1

        idxKotaAsal = int(input("\nMasukkan nomor kota asal   : ")) - 1
        idxKotaTujuan = int(input("Masukkan nomor kota tujuan : ")) - 1

    return idxKotaAsal, idxKotaTujuan


def inputTanggalWaktu():
    """
    Mengembalikan tanggal dan waktu penerbangan
    """
    header()
    print("---------- Menu Input Jadwal ----------\n")

    # Input tanggal
    print("Contoh tanggal: 25-12-2023")
    tanggal = input("Masukkan tanggal penerbangan (dengan format DD-MM-YYYY) : ")
    while validator.validasiTanggal(tanggal) == False:
        print("Terdapat kesalahan input tanggal, pastikan format telah sesuai!")
        time.sleep(1)
        header()
        print("---------- Menu Input Jadwal ----------\n")
        print("Contoh tanggal: 25-12-2023")
        tanggal = input("Masukkan tanggal penerbangan (dengan format DD-MM-YYYY) : ")

    # Input waktu
    header()
    print("---------- Menu Input Jadwal ----------\n")
    print("Contoh waktu: 18:00")
    waktu = input("Masukkan waktu penerbangan (dengan format HH:MM) : ")
    while validator.validasiWaktu(waktu) == False:
        print("Terdapat kesalahan input waktu, pastikan format telah sesuai!")
        time.sleep(1)
        header()
        print("---------- Menu Input Jadwal ----------\n")
        print("Contoh waktu: 18:00")
        waktu = input("Masukkan waktu penerbangan (dengan format HH:MM) : ")

    return tanggal, waktu


def formattingJadwalBaru(kode, idxKotaAsal, idxKotaTujuan, tanggal, waktu, arrOfKota):
    """
    Mengembalikan data jadwal yang baru dibuat dalam format JSON

    kode: string
    idxKotaAsal: integer, indeks bandara asal penerbangan
    idxKotaTujuan: integer, indeks bandara tujuan penerbangan
    tanggal: string, tanggal penerbangan dalam format (DD-MM-YYYY)
    waktu: string, waktu penerbangan dalam format (HH:MM)
    arrOfKota: array of string, daftar bandara
    """
    waktuSekarang = datetime.datetime.now()
    waktuSekarang = waktuSekarang.strftime("%Y-%m-%d %H:%M:%S")

    jsonData = {
        "notif": "Terdapat jadwal penerbangan baru!",
        "kode": kode,
        "kotaAsal": arrOfKota[idxKotaAsal],
        "kotaTujuan": arrOfKota[idxKotaTujuan],
        "tanggal": tanggal,
        "waktu": waktu,
        "dibuat": waktuSekarang,
        "diedit": "-",
    }

    return jsonData
