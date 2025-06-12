import time
import network
import urequests
from time import sleep
from machine import Pin, Timer
import machine
import utime
from micropyGPS import MicropyGPS
from machine import UART, Pin

time.sleep(3)
    
# Fungsi bantu: konversi GPS ke format desimal
def convert_to_decimal(coord):
    degrees, minutes, direction = coord
    decimal = degrees + (minutes / 60)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal
        
# Koneksi WiFi
SSID = "Loraswat"
PASSWORD = "12345678"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(SSID, PASSWORD)
    sleep(2)
    max_wait = 10
    while not wlan.isconnected():
        print("Menghubungkan ke WiFi...")
        time.sleep(2)

print("Terhubung dengan IP:", wlan.ifconfig()[0])
time.sleep(3)

# Inisialisasi micropyGPS
my_gps = MicropyGPS()
time.sleep(5)
# UART GPS
gps_serial = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
sleep(5)

# Inisialisasi relay
relay = Pin(18, Pin.OUT)
relay.value(1)  # default OFF

# URL server
base_url = "http://192.168.31.7/pico-web/command"
get_status_url = base_url + "/get_relay.php"
post_gps_url = base_url + "/send_gps.php"

# Waktu terakhir aksi
last_get_time = time.time()
last_post_time = time.time()

# Loop utama
led = machine.Pin("LED",machine.Pin.OUT) #led blink
while True:
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(0.4)
    now = time.time()

    # Ambil status relay tiap 10 detik
    # Ambil status relay tiap 10 detik
    if now - last_get_time >= 10:
        try:
            response = urequests.get(get_status_url)
            result = response.json()  # Parse JSON
            response.close()

            server_status = result.get('data', {}).get('status', 'OFF')  # Ambil status dari data
            
            print("[GET] Status : ", result)
            print("[GET] Status relay : ", server_status)
            
            if server_status == 'ON':
                relay.value(0)
            else:
                relay.value(1)

            last_get_time = now
        except Exception as e:
            print("Gagal GET : ", e)
            
    # Kirim gps ke server tiap 20 detik
    if now - last_post_time >= 20:
        try:
            # Update GPS dari serial
            while gps_serial.any():
                data = gps_serial.read()
                for byte in data:
                    stat = my_gps.update(chr(byte))
                    if stat is not None:
                        # Print parsed GPS data
                        print('UTC Timestamp:', my_gps.timestamp)
                        print('Date:', my_gps.date_string('long'))
                        print('Latitude:', my_gps.latitude_string())
                        print('Longitude:', my_gps.longitude_string())
                        print('Altitude:', my_gps.altitude)
                        print('Satellites in use:', my_gps.satellites_in_use)
                        print('Horizontal Dilution of Precision:', my_gps.hdop)
                        print()

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
                print("[POST] Status kirim data GPS : ", response.text.strip())
                response.close()
            else:
                print("[POST] GPS belum valid.")

            last_post_time = now
        except Exception as e:
            print("Gagal POST : ", e)
    time.sleep(0.1)
