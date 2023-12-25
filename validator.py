import datetime


def validasiRute(idxAsal, idxTujuan, arrOfKota):
    """
    Mengembalikan false jika asal sama dengan tujuan atau jika terdapat string kosong,
    true jika sebaliknya

    idxAsal: int, indeks bandara asal penerbangan
    idxTujuan: int, indeks bandara tujuan penerbangan
    """
    if (
        (idxAsal == idxTujuan)
        or ((idxAsal < 0) or (idxAsal >= len(arrOfKota)))
        or ((idxTujuan < 0) or (idxTujuan >= len(arrOfKota)))
    ):
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
