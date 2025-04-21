import network
import urequests
import time
from machine import UART, Pin
from micropyGPS import MicropyGPS

# Fungsi bantu: konversi GPS ke format desimal
def convert_to_decimal(coord):
    degrees, minutes, direction = coord
    decimal = degrees + (minutes / 60)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

# Koneksi WiFi
SSID = "Dalban Hotspot"
PASSWORD = "Dalban12345678"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Menghubungkan ke WiFi...")
        time.sleep(1)

print("Terhubung dengan IP:", wlan.ifconfig()[0])

# Inisialisasi micropyGPS
my_gps = MicropyGPS()

# UART GPS
gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Inisialisasi relay
relay = Pin(18, Pin.OUT)
relay.value(1)  # default OFF

# URL server
base_url = "http://192.168.1.216/pico-web/command"
get_status_url = base_url + "/get_relay.php"
post_gps_url = base_url + "/send_gps.php"

# Waktu terakhir aksi
last_get_time = time.time()
last_post_time = time.time()

# Loop utama
while True:
    now = time.time()

    # Ambil status relay tiap 5 detik
    if now - last_get_time >= 5:
        try:
            response = urequests.get(get_status_url)
            server_status = response.text.strip()
            print("[GET] Status relay : ", server_status)
            response.close()

            if 'ON' in server_status:
                relay.value(0)
            else:
                relay.value(1)

            last_get_time = now
        except Exception as e:
            print("Gagal GET : ", e)

    # Kirim gps ke server tiap 10 detik
    if now - last_post_time >= 10:
        try:
            # Update GPS dari serial
            while gps_serial.any():
                data = gps_serial.read()
                for byte in data:
                    my_gps.update(chr(byte))

            # Ambil data GPS
            lat = my_gps.latitude
            lon = my_gps.longitude

            # Pastikan data sudah valid
            if lat[0] != 0 and lon[0] != 0:
                lat_decimal = convert_to_decimal(lat)
                lon_decimal = convert_to_decimal(lon)

                data_json = {
                    "latitude": lat_decimal,
                    "longitude": lon_decimal
                }

                response = urequests.post(post_gps_url, json=data_json)
                print("[POST] Kirim GPS ke server : ", data_json)
                response.close()
            else:
                print("[POST] GPS belum valid.")

            last_post_time = now
        except Exception as e:
            print("Gagal POST : ", e)

    time.sleep(0.1)

