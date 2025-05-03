from flask import Flask, jsonify
from math import cos, sin, tan, acos, asin, atan, radians, degrees
from datetime import date

app = Flask(__name__)

# Fungsi pembantu
def decimal_to_hm(x):
    jam = int(x)
    menit = int((x - jam) * 60)
    return f"{jam:02}:{menit:02}"

# Fungsi utama untuk menghitung jadwal salat
def hitung_jadwal_salat(tanggal=date.today(), lintang=-6.2, bujur=106.8166667, zona=7):
    # Perhitungan hari dalam tahun
    tgl = tanggal
    N = tgl.timetuple().tm_yday

    # Koreksi deklinasi matahari
    L = 280.46 + 0.9856474 * N
    g = radians(357.528 + 0.9856003 * N)
    lambd = radians(L + 1.915 * sin(g) + 0.02 * sin(2 * g))
    delta = degrees(asin(sin(radians(23.45)) * sin(lambd)))

    # Waktu tengah hari (Dzuhur)
    G = (12 + zona - (bujur / 15)) - ((0.170 * sin(4 * radians(N - 80))) - (0.129 * sin(2 * radians(N - 8))))
    Dzuhur = G

    # Waktu salat lainnya
    def waktu_salat(hSudut):
        sudut = acos(-tan(radians(lintang)) * tan(radians(delta)))
        waktu = degrees(sudut) / 15
        return waktu

    def waktu_matahari(sudut_matahari):
        sudut = acos(cos(radians(90 + sudut_matahari)) / (cos(radians(lintang)) * cos(radians(delta))) - tan(radians(lintang)) * tan(radians(delta)))
        return degrees(sudut) / 15

    Imsak = Dzuhur - waktu_matahari(108)
    Subuh = Dzuhur - waktu_matahari(110)
    Terbit = Dzuhur - waktu_matahari(90.833)
    Duha = Dzuhur - waktu_matahari(85)
    Ashar = Dzuhur + waktu_salat(1)
    Maghrib = Dzuhur + waktu_matahari(90.833)
    Isya = Dzuhur + waktu_matahari(108)

    return {
        "tanggal": tgl.strftime("%A, %d %B %Y"),
        "Imsak": decimal_to_hm(Imsak),
        "Subuh": decimal_to_hm(Subuh),
        "Terbit": decimal_to_hm(Terbit),
        "Duha": decimal_to_hm(Duha),
        "Dzuhur": decimal_to_hm(Dzuhur),
        "Ashar": decimal_to_hm(Ashar),
        "Maghrib": decimal_to_hm(Maghrib),
        "Isya": decimal_to_hm(Isya),
    }

@app.route('/api/jadwal-salat', methods=['GET'])
def jadwal_salat():
    hasil = hitung_jadwal_salat()
    return jsonify(hasil)

if __name__ == '__main__':
    app.run(debug=True)
