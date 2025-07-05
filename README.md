# LoginVR Quest Caster · v 2.0 (2025-07)

One-click mirroring of your **Meta Quest 2 / 3 / Pro** to any Windows 10 / 11 PC.  
Built with **Python + Tkinter** on top of ADB and [scrcpy].

[scrcpy]: https://github.com/Genymobile/scrcpy

---

## ✨ What’s new in 2.0
| Category | Upgrade |
|----------|---------|
| **True wireless casting** | Toggle ADB‐over-Wi-Fi with a single button. The app now detects a `…:5555` entry and will cast over TCP/IP even if the USB cable is left plugged in. |
| **Batch-file hand-off** | `cast.bat` now accepts an *optional* serial parameter (`%1`). If supplied it runs `scrcpy -s %1 …`, otherwise it falls back to the first device. |
| **Greener status dot** | The traffic-light indicator now shows **green + “מחובר אלחוטית”** when Wi-Fi is active. |
| **Pylint-clean codebase** | All `subprocess.run()` calls go through a `run()` helper (`check=False` by default). |

---

## 🖼️ Quick tour

| State | Circle | Label |
|-------|--------|-------|
| **No device / offline** | 🔴 | “וודא שהקווסט דלוק…” |
| **USB unauthorised** | 🟡 | “אשר גישה במכשיר…” |
| **USB ready** | 🟢 | “מכשיר מחובר” |
| **Wi-Fi ready** | 🟢 | “מכשיר מחובר אלחוטית” |

---

## 🖥️ Prerequisites

| Component | Why you need it |
|-----------|-----------------|
| **Python ≥ 3.8** | Run from source or package with PyInstaller |
| **scrcpy + adb** | Actual mirroring & ADB comms |
| **Oculus ADB driver** | Windows only — makes the Quest appear correctly in `adb devices` |

---

## 📂 Repo layout

```text
quest-caster/
├─ main.py           ← Tkinter GUI (all logic lives here)
├─ src/
│  ├─ adb.exe
│  ├─ scrcpy.exe
│  ├─ cast.bat      ← launches scrcpy with your flags
│  └─ icon.ico
└─ README.md
```

The application always looks for resources inside **`src/`**, both from source and when frozen.

---

## 🚀 Run from source

```bash
git clone https://github.com/Avi-Kohen/casting.git
cd casting
python main.py
```

---

## 🏗️ Build a portable EXE

```cmd
python -m PyInstaller --noconsole --onefile --add-data "src;src" --icon src/temp.ico main.py
```

`dist\main.exe` is the **single** file you distribute.

---

## 📖 How to use (USB ➜ Wi-Fi)

1. **Enable developer mode** in the Quest mobile app.  
2. Plug the headset into the PC → put it on → **Allow USB debugging (Always)**.  
3. Launch **Quest Caster** — circle turns **green**.  
4. Click **📡 חיבור אלחוטי**. The status flips to **“מחובר אלחוטית”**.  
5. (Optional) Unplug the cable.  
6. Click **📺 הצג מסך** — scrcpy mirrors over Wi-Fi with the crop/bitrate you set in `cast.bat`.

Close the window when done; Wi-Fi ADB is automatically disconnected(not yet implemented).

---

## 🛠️ Troubleshooting

| Symptom | Fix |
|---------|-----|
| **Red** circle | Check cable / port · Ensure Oculus ADB driver installed |
| **Yellow** circle | Put the headset on → tap **Allow** |
| scrcpy exits instantly while both links are up | Make sure *cast.bat* matches the template below |
| Black / stuttery video | Try `--render-driver=direct3d` or lower `-b` bitrate in *cast.bat* |

---

## 📝 `cast.bat` template (v 2.0)

```bat
@echo off
:: If %1 (serial) is supplied use it, otherwise pick first device
if "%~1"=="" (
    scrcpy --render-driver=opengl ^
           --crop 1600:900:2017:510 ^
           --no-audio -b4M --max-size 1024 ^
           --video-codec=h264 --video-encoder=OMX.qcom.video.encoder.avc ^
           -n
) else (
    scrcpy -s %1 --render-driver=opengl ^
           --crop 1600:900:2017:510 ^
           --no-audio -b4M --max-size 1024 ^
           --video-codec=h264 --video-encoder=OMX.qcom.video.encoder.avc ^
           -n
)
```

---

## 🗒️ Changelog

* **2.0 (2025-07-05)**   Wi-Fi toggle, auto-disconnect(not yet implemented), serial-aware `cast.bat`, Pylint clean-up, UI polish.  
* **1.x**               Initial USB-only release.

---

## 🤝 Contributing

1. Fork → create feature branch (`git checkout -b feat/your-idea`).  
2. Commit using **Conventional Commits** (`feat: …`, `fix: …`).  
3. Open a PR — small, focused changes are easiest to review.

---

## 📜 License

All rights reserved to **LoginVR**. Internal use only.
