import tkinter as tk
from tkinter import messagebox
import speedtest
import threading
import time
import math
import socket
import requests
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec
import psutil
import numpy as np
from PIL import Image, ImageTk
import subprocess

class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("950x650")

        # ==== BACKGROUND ====
        self.bg_original = Image.open("images/background.png")
        self.bg_image = ImageTk.PhotoImage(self.bg_original)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.resize_background)

        # ==== COLORS ====
        self.CYAN = "#00F3FF"
        self.PURPLE = "#C400FF"
        BOX_BG = "#0b0013"
        BOX_BORDER = "#6f00ff"
        FONT_MAIN = ("Segoe UI", 10, "bold")

        # ==== TITLE ====
        title = tk.Label(
            root, text="INTERNET SPEED TEST",
            font=("Segoe UI", 16, "bold"),
            fg=self.CYAN, bg="#000000"
        )
        title.pack(pady=10)

        # ==== INFO BOX ====
        info_box = tk.Frame(
            root, bg=BOX_BG,
            highlightbackground=BOX_BORDER,
            highlightthickness=3,
            width=520, height=340
        )
        info_box.pack(pady=10)
        info_box.pack_propagate(True)

        # ==== 2-label system (Option B) ====
        def neon_label(title):
            frame = tk.Frame(info_box, bg=BOX_BG)

            lbl_title = tk.Label(
                frame, text=title,
                font=FONT_MAIN, fg=self.PURPLE, bg=BOX_BG
            )
            lbl_title.pack(side="left")

            lbl_value = tk.Label(
                frame, text="--",
                font=("Segoe UI", 10, "normal"),  # normal font
                fg=self.CYAN, bg=BOX_BG
            )

            
            lbl_value.pack(side="left", padx=5)

            frame.pack(anchor="center")
            return lbl_title, lbl_value

        # ==== LABELS ====
        self.client_title, self.client_value = neon_label("Client:")
        self.server_title, self.server_value = neon_label("Server(s):")
        self.connection_title, self.connection_value = neon_label("Connection Type:")
        self.local_ip_title, self.local_ip_value = neon_label("IPv4 Address:")
        self.ipv6_title, self.ipv6_value = neon_label("IPv6 Address:")
        self.mac_title, self.mac_value = neon_label("MAC Address:")
        self.test_time_title, self.test_time_value = neon_label("Test Time:")
        self.ping_title, self.ping_value = neon_label("Ping:")
        self.jitter_title, self.jitter_value = neon_label("Jitter:")
        self.download_title, self.download_value = neon_label("Download:")
        self.upload_title, self.upload_value = neon_label("Upload:")
        self.signal_title, self.signal_value = neon_label("Signal Strength:")

        # ==== BUTTONS ====
        btn_frame = tk.Frame(root, bg="#000000")
        btn_frame.pack(pady=10)

        def neon_button(text, cmd, color):
            btn = tk.Button(
                btn_frame, text=text, command=cmd,
                bg=color, fg="black",
                font=("Segoe UI", 10, "bold"),
                relief="flat", padx=15, pady=5
            )
            btn.bind("<Enter>", lambda e: btn.config(bg="white"))
            btn.bind("<Leave>", lambda e: btn.config(bg=color))
            return btn

        self.start_btn = neon_button("START TEST", self.start_test, self.CYAN)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.reset_btn = neon_button("RESET", self.reset_values, self.PURPLE)
        self.reset_btn.pack(side=tk.LEFT, padx=10)

        self.save_btn = neon_button("SAVE INFO", self.save_info, "#00FF90")
        self.save_btn.pack(side=tk.LEFT, padx=10)

        # ==== GRAPH AREA ====
         # Figure
        self.fig = plt.Figure(figsize=(7,5), dpi=80)
        gs = GridSpec(2, 2, figure=self.fig, height_ratios=[0.8,0.7], hspace=0.4, wspace=0.2)

        self.ax_download = self.fig.add_subplot(gs[0,0])
        self.ax_upload = self.fig.add_subplot(gs[0,1])
        self.ax_history = self.fig.add_subplot(gs[1,:])

        for ax in [self.ax_download, self.ax_upload]:
            ax.set_xlim(-1,1)
            ax.set_ylim(0,1)
            ax.axis('off')
            ax.margins(0)

        self.ax_download.set_title("Download", color='cyan', fontsize=11)
        self.ax_upload.set_title("Upload", color='magenta', fontsize=11)

        img_download = mpimg.imread("images/speedometer_bg.png")
        img_upload = mpimg.imread("images/speedometer_bg.png")
        self.ax_download.imshow(img_download, extent=[-1,1,0,1], zorder=0)
        self.ax_upload.imshow(img_upload, extent=[-1,1,0,1], zorder=0)

        x0, y0 = self.draw_needle(0)
        self.download_line, = self.ax_download.plot(x0, y0, lw=2.5, color='cyan', zorder=1)
        self.upload_line, = self.ax_upload.plot(x0, y0, lw=2.5, color='magenta', zorder=1)

        self.ax_history.set_facecolor('white')
        self.ax_history.set_title("Speed Fluctuations", color='black', fontsize=11)
        self.ax_history.set_xlabel("Time Steps", color='black', fontsize=9)
        self.ax_history.set_ylabel("Mbps", color='black', fontsize=9)
        self.ax_history.set_xlim(0,100)
        self.ax_history.set_ylim(0,100)

        self.download_history = [0]
        self.upload_history = [0]
        self.line_download_hist, = self.ax_history.plot(self.download_history, color='cyan', label='Download')
        self.line_upload_hist, = self.ax_history.plot(self.upload_history, color='magenta', label='Upload')
        legend = self.ax_history.legend(fontsize=8)
        for text in legend.get_texts():
            text.set_color("black")

        self.fig.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.12)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=8)
        self.canvas.draw()
        self.running = False

    # ------------------------------
    def resize_background(self, event):
        if event.width < 200 or event.height < 200:
            return
        resized = self.bg_original.resize((event.width, event.height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_image)

    # ------------------------------
    def draw_needle(self, value, max_value=100, radius=0.9):
        angle = math.pi * (1 - min(value, max_value) / max_value)
        x = [0, radius * math.cos(angle)]
        y = [0, radius * math.sin(angle)]
        return x, y

    # ------------------------------
    

    def detect_connection_type(self):
        try:
            # get the local IP used to reach the internet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()

            # check which interface has this IP
            addrs = psutil.net_if_addrs()
            for iface_name, iface_addrs in addrs.items():
                for addr in iface_addrs:
                    if addr.family == socket.AF_INET and addr.address == local_ip:
                        name_lower = iface_name.lower()
                        if "wi-fi" in name_lower or "wireless" in name_lower or "wlan" in name_lower:
                            return "Wi-Fi"
                        else:
                            return "Ethernet"
            return "Unknown"
        except:
            return "Unknown"




    def get_ipv6_address(self):
        try:
            addrs = psutil.net_if_addrs()
            for iface in addrs:
                for addr in addrs[iface]:
                    if addr.family == socket.AF_INET6:
                        ipv6 = addr.address.split('%')[0]
                        if ipv6 != "::1":
                            return ipv6
        except:
            pass

        try:
            ipv6 = requests.get("https://api64.ipify.org", timeout=3).text
            if ipv6:
                return ipv6
        except:
            pass
        return "Not Available"

    def get_mac_address(self):
        try:
            addrs = psutil.net_if_addrs()
        except:
            return "Not Available"

        for iface, addr_list in addrs.items():
            for addr in addr_list:
                if addr.family == psutil.AF_LINK:
                    mac = addr.address
                    if mac and mac != "00:00:00:00:00:00":
                        return mac.upper()
        return "Not Available"

    # ------------------------------
    def start_test(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.run_speedtest, daemon=True).start()

    # ------------------------------
    def run_speedtest(self):
        # Client info
        try:
            response = requests.get("https://ipinfo.io/json", timeout=5).json()
            public_ip = response.get('ip', 'Unknown')
            isp = response.get('org', 'Unknown')
            city = response.get('city', 'Unknown')
            country = response.get('country', 'Unknown')
        except:
            public_ip = isp = city = country = "Unknown"

        self.root.after(0, lambda: self.client_value.config(
            text=f"{city}, {country} | {public_ip}  {isp}"
        ))

        # Connection type
        conn = self.detect_connection_type()
        self.root.after(0, lambda: self.connection_value.config(text=conn))

        # IPv4
        try:
            ipv4 = socket.gethostbyname(socket.gethostname())
        except:
            ipv4 = "Unknown"
        self.root.after(0, lambda: self.local_ip_value.config(text=ipv4))

        # IPv6
        ipv6 = self.get_ipv6_address()
        self.root.after(0, lambda: self.ipv6_value.config(text=ipv6))

        # MAC
        mac = self.get_mac_address()
        self.root.after(0, lambda: self.mac_value.config(text=mac))

        # Time
        test_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.root.after(0, lambda: self.test_time_value.config(text=test_time))

        # Speedtest
        st = speedtest.Speedtest()
        server = st.get_best_server()

        server_text = f"{server['name']}, {server['country']} | {server['sponsor']}"
        self.root.after(0, lambda: self.server_value.config(text=server_text))

        # ping
        self.root.after(0, lambda: self.ping_value.config(text=f"{server['latency']} ms"))

        # jitter
        pings = []
        for _ in range(5):
            st.get_best_server()
            pings.append(st.results.ping)
            time.sleep(0.1)

        jitter = sum(abs(pings[i] - pings[i+1]) for i in range(len(pings)-1)) / (len(pings)-1)
        self.root.after(0, lambda: self.jitter_value.config(text=f"{jitter:.2f} ms"))

        # download
        download = st.download() / 1_000_000
        self.animate_needle(download, self.download_line, self.download_value, "Download")

        # upload
        upload = st.upload() / 1_000_000
        self.animate_needle(upload, self.upload_line, self.upload_value, "Upload")

        # signal
        if download < 1:
            sig = "Poor"
        elif download < 5:
            sig = "Average"
        elif download < 20:
            sig = "Good"
        elif download < 30:
            sig = "Very Good"
        else:
            sig = "Excellent"

        self.root.after(0, lambda: self.signal_value.config(text=sig))
        self.running = False

    # ------------------------------
    def animate_needle(self, target_speed, line, label, text):
        steps = 50
        for i in range(steps):
            spd = target_speed * (i + 1) / steps
            x, y = self.draw_needle(spd)
            line.set_data(x, y)

            self.root.after(0, lambda s=spd: label.config(text=f"{s:.2f} Mbps"))

            # --- ADD HISTORY UPDATE ---
            if text == "Download":
                self.download_history.append(spd)
                self.upload_history.append(self.upload_history[-1])
            else:
                self.upload_history.append(spd)
                self.download_history.append(self.download_history[-1])

            # Keep only last 100 points
            self.download_history = self.download_history[-100:]
            self.upload_history = self.upload_history[-100:]

            # Update history plots
            self.line_download_hist.set_data(range(len(self.download_history)), self.download_history)
            self.line_upload_hist.set_data(range(len(self.upload_history)), self.upload_history)

            # Adjust y-limit dynamically
            self.ax_history.set_xlim(0, 100)
            self.ax_history.set_ylim(0, max(max(self.download_history), max(self.upload_history), 50))

            self.canvas.draw()
            time.sleep(0.05)


    # ------------------------------
    def reset_values(self):
        fields = [
            self.client_value, self.server_value, self.connection_value,
            self.local_ip_value, self.ipv6_value, self.mac_value,
            self.test_time_value, self.ping_value, self.jitter_value,
            self.download_value, self.upload_value, self.signal_value
        ]
        for f in fields:
            f.config(text="--")

        x0, y0 = self.draw_needle(0)
        self.download_line.set_data(x0, y0)
        self.upload_line.set_data(x0, y0)
        self.canvas.draw()

    # ------------------------------
    def save_info(self):
        try:
            test_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"InternetSpeedTest_{test_time}.txt"

            with open(filename, "w") as f:
                f.write(f"Client: {self.client_value.cget('text')}\n")
                f.write(f"Server(s): {self.server_value.cget('text')}\n")
                f.write(f"Connection Type: {self.connection_value.cget('text')}\n")
                f.write(f"IPv4 Address: {self.local_ip_value.cget('text')}\n")
                f.write(f"IPv6 Address: {self.ipv6_value.cget('text')}\n")
                f.write(f"MAC Address: {self.mac_value.cget('text')}\n")
                f.write(f"Test Time: {self.test_time_value.cget('text')}\n")
                f.write(f"Ping: {self.ping_value.cget('text')}\n")
                f.write(f"Jitter: {self.jitter_value.cget('text')}\n")
                f.write(f"Download: {self.download_value.cget('text')}\n")
                f.write(f"Upload: {self.upload_value.cget('text')}\n")
                f.write(f"Signal Strength: {self.signal_value.cget('text')}\n")

            messagebox.showinfo("Saved", f"Test info saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Run App
root = tk.Tk()
app = SpeedTestApp(root)
root.mainloop()
