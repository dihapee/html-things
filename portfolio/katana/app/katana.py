import os
import subprocess
import sys
import ctypes
from flask import Flask, render_template, request
from scapy.all import ARP, Ether, srp

# ASCII logo
logo = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣙⣿⡉⢷⣄⠀⠀⠀⠀⣸⣽⣇⠀⠀⠀⠀⣠⣾⢍⣽⣋⣃⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⠿⢮⣳⢝⡻⡌⢿⣇⠀⢀⡼⢿⣼⣿⢧⣀⠀⣰⡿⢁⣿⣫⣗⡦⠿⠷⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⡾⠾⣿⣾⣉⠀⣄⣸⣿⣿⣮⣷⣿⠳⢶⣿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢙⣿⣯⡿⠟⢾⣯⢿⣽⢿⠛⢿⣽⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣷⠶⣦⣄⡞⠁⣸⠋⢳⣿⣿⣿⣿⣽⡾⣿⣿⣿⣳⣤⣴⣶⣶⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡧⣿⣿⣿⣿⣿⣁⣤⣿⣶⣿⣾⡟⠛⠻⣷⣿⣿⡿⣜⣟⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⢷⣿⣿⣿⣾⣿⢫⣵⠏⠀⠀⠀⠙⣦⡙⢿⣿⣿⣿⣿⡿⠟⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣛⡿⠯⣤⣤⣤⣤⣤⣼⣷⣿⣿⣿⣿⣿⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣾⣿⣿⣼⡇⠙⣛⣿⣿⣹⣡⣍⢻⡿⠟⠋⢹⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡀⠤⠒⣿⠯⠹⠿⢿⠒⠤⢀⣾⣿⣿⣿⣟⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⣿⣿⣿⣿⣿⣧⡝⠀⡀⠛⠲⠤⠶⠟⣀⡀⢸⣿⣿⣿⣿⣿⣿⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣀⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⣿⣿⣿⣿⣿⣿⣿⡀⢿⣿⣿⣿⣿⣿⡿⢰⣿⣿⣿⣿⣿⣿⣿⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀
⢰⣿⣿⣿⢿⣶⣦⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠓⠚⠻⠿⠿⢿⣿⡖⠯⢿⣿⣿⠿⢣⣿⡿⠿⠿⠿⠛⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣴⣶⣿⣿⣿⣿⣶⣤
⠈⠛⠛⠛⠾⠧⣽⣋⡟⢻⠿⣶⣶⣤⣄⣀⣴⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠶⢤⣤⡤⠶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣶⣄⣠⣴⣶⣾⠿⡟⣻⣛⣿⠼⠷⠛⠛⠛⠁⠈
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠒⠧⢼⣃⣛⣿⡿⠛⢻⠦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⠴⡞⠻⢿⣿⢛⣩⡧⠼⠒⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡷⠦⠾⢍⣑⡺⠯⢝⣷⡶⢤⣄⣀⠀⠀⠀⠀⠀⣀⣠⣤⣶⣾⡯⠿⢗⣛⡩⠿⠴⢾⣿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠒⠲⢬⣍⣓⡛⠯⢿⣶⡾⠿⣿⣒⣩⡥⠔⠒⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡤⠶⠒⠛⠉⠉⢉⣳⡶⠦⢭⣀⣀⠉⠉⠓⠒⠶⠤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⡴⠶⠛⠋⠉⠁⢀⣀⣠⠴⠖⠚⠉⠁⠀⠀⠀⠀⠀⠈⠉⠛⠲⠦⢤⣀⡀⠈⠉⠙⠓⠶⠦⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⠞⠛⠋⠉⠁⢀⣠⡤⠴⠒⠚⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠒⠢⢤⣤⣀⠀⠉⠙⠛⠳⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣼⡧⠤⠔⠒⠊⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠒⠲⠤⢼⣧⡀⠀⠀⠀⠀⠀⠀⠀
"""

# Ověření administrátorských práv
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Síťové informace
def gather_network_info():
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    return result.stdout

# ARP scan pro zadanou IP
def scan_network(target_ip):
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=2, verbose=0)[0]
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

# Ping test
def ping_host(host):
    try:
        output = subprocess.check_output(["ping", "-n", "4", host], text=True)
        return output
    except subprocess.CalledProcessError:
        return "Ping failed."

# Flask web app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', logo=logo)

@app.route('/info')
def info():
    info = gather_network_info()
    return f"<pre>{info}</pre><a href='/'>← Zpět</a>"

@app.route('/scan', methods=["POST"])
def scan():
    ip_range = request.form.get("ip_range")
    results = scan_network(ip_range)
    return render_template("index.html", scan_results=results, logo=logo)

@app.route('/ping', methods=["POST"])
def ping():
    target = request.form.get("ping_target")
    result = ping_host(target)
    return render_template("index.html", ping_result=result, logo=logo)

if __name__ == "__main__":
    if not is_admin():
        print("⚠️ Tento program spusť jako správce.")
        sys.exit()

    print(logo)
    print("Spouštím webové rozhraní na http://127.0.0.1:5000 ...")
    app.run(debug=False)
