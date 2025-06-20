# LoginVR Quest Caster 

A lightweight **Python + Tkinter** desktop launcher that makes mirroring your **Meta Quest 2** headset to a Windows PC a one‑click task. Under the hood it simply drives ADB and [scrcpy](https://github.com/Genymobile/scrcpy), but it adds quality‑of‑life features such as colour‑coded connection status, auto‑refresh, and built‑in help.

---

## ✨ Features

|  Feature                     |  Details                                                                          |
| ---------------------------- | --------------------------------------------------------------------------------- |
| **Traffic‑light indicator**  |  Red = not detected, Yellow = USB debugging not authorised, Green = ready to cast |
| **Auto‑refresh loop**        |  Polls `adb get‑state` every 5 seconds (negligible CPU)                           |
| **Cast button**              |  Runs `cast.bat` which launches scrcpy with your preferred parameters             |
| **Instructions / About**     |  Accessible from both the top menu and a dedicated button                         |
| **Clickable e‑mail link**    |  Opens the user’s default mail client via `mailto:`                               |
| **Custom window & EXE icon** |  Easy branding out‑of‑the‑box                                                     |

---

## 🖥️ Prerequisites

|  Component                      |  Why you need it                                                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Python ≥ 3.8**                |  Run the app from source or package with PyInstaller                                                                      |
| **scrcpy + adb**                |  Actual screen casting & USB comms                                                                                        |
| **Oculus ADB Driver (Windows)** |  Quest 2 recognised properly by ADB – [download here](https://developer.oculus.com/downloads/package/oculus-adb-drivers/) |

> **Tip •** On macOS & Linux no extra driver is required.

---

## 📂 Folder layout (in‑repo)

```text
casting/
├─ main.py            ← Tkinter GUI
├─ src/               ← Runtime resources kept as‑is inside the EXE
│  ├─ adb.exe
│  ├─ scrcpy.exe
│  ├─ cast.bat
│  └─ icon.ico
└─ README.md
```

The application always looks for resources relative to `src/`, both when run from source *and* when packed.

---

## 🚀 Running from source

```bash
# clone & cd into repo
git clone https://github.com/Avi-Kohen/casting.git
cd casting

python -m venv .venv && .\.venv\Scripts\activate  # (optional)
pip install -r requirements.txt                      # tkinter is in stdlib
python main.py                                       # launch the GUI
```

---

## 🏗️ Building a portable EXE

pyinstaller --noconsole --onefile --add-data "src;src" --icon src/temp.ico main.py

```bash
pyinstaller --noconsole --onefile \
  --add-data "src;src" \
  --icon src/icon.ico \
  main.py
```

The resulting `dist/main.exe` contains **everything**, including the `src/` folder, so you can copy the single file to any Windows 10/11 PC.

---

## 📖 Usage

1. **Enable developer mode** in the Quest mobile app.
2. Plug the headset into your PC with a data‑capable USB‑C cable.
3. Put the headset on ‑> **Allow USB debugging**.
4. Start *Quest 2 Caster* → indicator turns **Green**.
5. Click **Cast Screen** → scrcpy launches with the crop, bitrate, and codec you set in `cast.bat`.

If the circle stays **Yellow**, you haven’t accepted the USB‑debug prompt yet.

---

## 🛠️ Troubleshooting

|  Symptom                          |  Fix                                                                               |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| Indicator stays **Red**           |  • Check cable / port \  • `adb devices` shows nothing → install Oculus ADB driver |
| Indicator is **Yellow**           |  Put the headset on → tap **Allow**                                                |
| scrcpy window is black / flickers |  Try `--render-driver=direct3d` or a lower bitrate in `cast.bat`                   |

---

## 🤝 Contributing

1. Fork → create feature branch (`git checkout -b feat/your-idea`).
2. Commit using **Conventional Commits**; reference issues with `Fixes #n`.
3. Push & open a Pull Request — small, focused PRs make reviews easier.

---

## 📝 License

All rights reserved to **LoginVR**. Not for sale or distribution — internal use only.

---

### MIT License

```
Copyright (c) 2025 LoginVR

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### BSD 3‑Clause License

```
Copyright (c) 2025, LoginVR
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of LoginVR nor the names of its contributors may be used to
   endorse or promote products derived from this software without specific
   prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

