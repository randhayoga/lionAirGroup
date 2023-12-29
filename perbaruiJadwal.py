import os
import time
import validator

clearScreen = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")


def header():
    clearScreen()
    print("============= Program Jadwal Penerbangan =============\n")


def perbaruiKode(kodeLama, arrOfKode):
    """
    Memperbarui kode penerbangan Lion Air yang didapat dari masukan user

    kodeLama: string, kode penerbangan yang lama
    arrOfKode: list, yang berisi seluruh kode penerbangan yang telah dibuat
    """
    header()
    print("---------- Menu Perbarui Kode Penerbangan ----------\n")
    print(f"Kode sekarang   : {kodeLama}")
    print("Contoh kode baru : '523'")

    kodeBaru = "JT" + input("Masukkan kode penerbangan baru : ")

    # Ganti kodeLama dengan kodeBaru pada list kode
    arrOfKode[arrOfKode.index(kodeLama)] = kodeBaru
    return kodeBaru


def perbaruiKota(kotaAsalLama, kotaTujuanLama, arrOfKota):
    """
    Memperbarui kota asal dan kota tujuan penerbangan berdasarkan masukan user
    """
    header()
    print("---------- Menu Perbarui Kota Asal & Tujuan ----------\n")
    print(f"Kota asal sekarang   : {kotaAsalLama}")
    print(f"Kota tujuan sekarang : {kotaTujuanLama}")

    # Mencetak semua kota
    i = 1
    for kota in arrOfKota:
        print(f"({i}) {kota}")
        i += 1

    idxAsalBaru = int(input("\nMasukkan nomor kota asal baru   : ")) - 1
    idxTujuanBaru = int(input("Masukkan nomor kota tujuan baru : ")) - 1

    while validator.validasiRute(idxAsalBaru, idxTujuanBaru, arrOfKota) == False:
        print("Rute tidak valid, pastikan angka sudah sesuai!")
        time.sleep(2)

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

    tangalLama: string, tanggal keberangkatan yang lama
    waktuLama: string, waktu keberangkatan yang lama
    """
    # Perbarui tanggal
    header()
    print("---------- Menu Perbarui Jadwal ----------\n")
    print(f"Tanggal sekarang : {tanggalLama}")
    print("Contoh tanggal: 25-12-2023")
    tanggalBaru = input(
        "Masukkan tanggal penerbangan baru (dengan format DD-MM-YYYY) : "
    )
    while validator.validasiTanggal(tanggalBaru) == False:
        print("Terdapat kesalahan input tanggal, pastikan format telah sesuai!")
        time.sleep(2)
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
        time.sleep(2)
        header()
        print("---------- Menu Perbarui Jadwal ----------\n")
        print(f"Waktu sekarang : {waktuLama}")
        print("Contoh waktu: 18:00")
        waktuBaru = input("Masukkan waktu penerbangan (dengan format HH:MM) : ")

    return tanggalBaru, waktuBaru
