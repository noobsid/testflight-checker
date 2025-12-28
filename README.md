# 🚨 TestFlight Availability Checker + ESP32 Alarm

Sistem ini digunakan untuk **memonitor TestFlight beta Apple** dan memberikan **alarm suara real-time** menggunakan **ESP32 + buzzer** ketika beta menjadi AVAILABLE (tidak full).

Begitu status berubah:
- 🔔 **AVAILABLE** → buzzer langsung berbunyi (bangunin orang 😄)
- ⛔ **FULL kembali** → buzzer otomatis berhenti
- 🧑‍💻 **Manual backup** → kontrol via Telegram (`ALARM` / `STOP`)

---
---

## 🔧 Komponen

### Hardware
- ESP32
- Buzzer aktif (HIGH = bunyi)
- WiFi lokal

### Software
- Python 3
- `requests`, `pytz`
- ESP32 Arduino Core
- Library:
  - `UniversalTelegramBot`
  - `WiFiClientSecure`
  - `WebServer`

---

## 📡 ESP32 Configuration

| Item | Value |
|-----|------|
| IP ESP32 | `192.168.11.12` |
| Port HTTP | `880` |
| Buzzer Pin | `GPIO 15` |

### Endpoint

---

## 🐍 Install Python Dependencies (PEP-668 Safe)

```bash
python3 -m venv testflight
source testflight/bin/activate
pip install requests pytz
