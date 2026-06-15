# 🚀 Internet Speed Test – Python GUI Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Matplotlib](https://img.shields.io/badge/Charts-Matplotlib-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

A modern desktop application built with Python that allows users to test their internet speed and view detailed network information through an interactive graphical interface.

</div>

---

## 📑 Table of Contents

* [📌 Overview](#-overview)
* [✨ Features](#-features)

  * [🌐 Network Information](#-network-information)
  * [⚡ Internet Speed Testing](#-internet-speed-testing)
  * [📊 Interactive Visualizations](#-interactive-visualizations)
  * [📶 Network Quality Metrics](#-network-quality-metrics)
  * [💾 Save Results](#-save-results)
* [🖼️ User Interface](#️-user-interface)
* [📂 Project Structure](#-project-structure)
* [🛠️ Technologies Used](#️-technologies-used)
* [📦 Requirements](#-requirements)
* [▶️ Running the Application](#️-running-the-application)
* [🔄 How It Works](#-how-it-works)
* [⚠️ Notes](#️-notes)
* [🚀 Future Improvements](#-future-improvements)
* [👨‍💻 Author](#-author)
* [📜 License](#-license)
  
---

## 📌 Overview

**Internet Speed Test** is a feature-rich desktop application developed using **Python and Tkinter**. It provides users with real-time internet speed testing along with detailed connection information, animated speedometers, and speed history graphs.

Unlike a traditional speed test tool that only displays download and upload speeds, this application also presents useful networking details such as:

* Public IP information
* ISP details
* Server information
* IPv4 and IPv6 addresses
* MAC address
* Connection type detection
* Ping and jitter analysis
* Signal quality assessment
* Historical speed fluctuations

The application combines functionality with an attractive user interface to create a professional speed testing experience.

---

## ✨ Features

### 🌐 Network Information

* Displays Public IP Address
* Detects Internet Service Provider (ISP)
* Shows client location information
* Retrieves IPv4 Address
* Retrieves IPv6 Address
* Displays MAC Address
* Detects whether the connection is:

  * Wi-Fi
  * Ethernet

---

### ⚡ Internet Speed Testing

* Real-time Download Speed Testing
* Real-time Upload Speed Testing
* Automatic Best Server Selection
* Displays:

  * Server Name
  * Server Sponsor
  * Server Country

---

### 📊 Interactive Visualizations

* Animated Download Speedometer
* Animated Upload Speedometer
* Speed fluctuation history graph
* Dynamic graph updates during testing
* Automatic graph scaling

---

### 📶 Network Quality Metrics

* Ping Measurement
* Jitter Calculation
* Signal Strength Classification:

| Download Speed | Signal Strength |
| -------------- | --------------- |
| < 1 Mbps       | Poor            |
| 1 – 5 Mbps     | Average         |
| 5 – 20 Mbps    | Good            |
| 20 – 30 Mbps   | Very Good       |
| > 30 Mbps      | Excellent       |

---

### 💾 Save Results

Save complete test information into a timestamped text report containing:

* Client Information
* Server Details
* Connection Type
* IP Addresses
* MAC Address
* Ping
* Jitter
* Download Speed
* Upload Speed
* Signal Strength

---

## 🖼️ User Interface

The application includes:

* Neon-inspired modern design
* Responsive background image
* Animated speedometer needles
* Historical speed charts
* Interactive buttons
* Clean information panel

---

## 📂 Project Structure

```text
Internet-Speed-Test/
│
├── speed_test.py
├── requirements.txt
├── README.md
│
└── images/
    ├── background.png
    └── speedometer_bg.png
```

---

## 🛠️ Technologies Used

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| Python        | Core Programming Language      |
| Tkinter       | Graphical User Interface       |
| speedtest-cli | Internet Speed Testing         |
| Matplotlib    | Graphs and Speedometers        |
| Pillow        | Image Processing               |
| Requests      | API Requests                   |
| Psutil        | System and Network Information |
| NumPy         | Numerical Operations           |

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

### requirements.txt

```text
matplotlib==3.10.7
numpy==2.3.4
pillow==12.0.0
psutil==7.1.3
requests==2.32.5
speedtest-cli==2.1.3
```

---

## ▶️ Running the Application

Clone the repository:

```bash
git clone https://github.com/Daksh-Sahu/internet-speed-test-python.git
```

Move into the project directory:

```bash
cd YOUR_REPOSITORY
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python speed_test.py
```

---

## 🔄 How It Works

1. The application gathers network information.
2. It identifies the active network connection.
3. The best Speedtest server is selected automatically.
4. Ping and jitter are measured.
5. Download speed is tested and visualized.
6. Upload speed is tested and visualized.
7. Speed history graphs update in real time.
8. Results can be saved locally.

---

## ⚠️ Notes

* An active internet connection is required.
* Speed testing duration depends on connection quality.
* IPv6 information may not be available on all networks.
* Tkinter is bundled with most Windows Python installations.

---

## 🚀 Future Improvements

Potential enhancements include:

* Export results to PDF
* Dark/Light themes
* Multi-language support
* Speed test scheduling
* CSV export functionality
* Detailed analytics dashboard
* Server selection options
* Internet outage logging

---

## 👨‍💻 Author

Developed with Python to provide a visually engaging and informative internet speed testing experience. <br>
If you found this project useful, consider giving it a ⭐ on GitHub!

**Daksh S** <br>
📧 **Email:** [daksh.s.blr@gmail.com](mailto:daksh.s.blr@gmail.com) <br>
💼 **LinkedIn:** https://www.linkedin.com/in/Daksh-Sahu-blr2023 




---

## 📜 License
Feel free to use, modify, and distribute it for educational and personal purposes.
