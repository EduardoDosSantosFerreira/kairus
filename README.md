Here's the complete README in English:

```markdown
# KAIRUS

<div align="center">

<img src="./icon.png" width="120">

# KAIRUS

> Secure note-taking application with encryption.
> 100% offline.
</div>

---

# 📸 Interface

## Registration Screen

<div align="center">
  <img src="./web/img/cadastro.png" width="850">
</div>

---

## Dashboard

<div align="center">
  <img src="./web/img/dashboard.png" width="850">
</div>

---

# 🔐 Features

## AES-256 Encryption

All notes are protected using AES-256-CBC with modern encryption practices.

* AES-256-CBC Encryption
* PBKDF2 Key Derivation
* 100,000 iterations
* Unique salt per encryption
* PKCS7 Padding

---

## 📁 Password-Protected Folders

Organize your notes in secure folders with custom passwords.

* Individual folder protection
* Secure password hashing
* Encrypted local storage

---

## 💾 Smart Auto-Save

KAIRUS automatically saves your work to prevent data loss.

* Auto-save system
- Automatic recovery
- Vault fallback

---

## 🚀 Quick Note Capture

Create notes instantly from anywhere using a global shortcut.

| Action     | Shortcut        |
| ---------- | --------------- |
| Quick Note | `Ctrl + Insert` |

---

## 📄 File Export

Export your notes quickly.

Supported formats:

* PDF
* TXT

---

## 🔒 100% Offline

KAIRUS works completely offline.

* No cloud
* No tracking
* No telemetry
* No subscriptions
- Full local data control

---

# 🛡️ Security Architecture

KAIRUS is built with a focus on local data protection and user privacy.

```text
╔══════════════════════════╗
║   AES-256-CBC            ║
║   PBKDF2 (100k iters)    ║
║   Unique Salt per Note   ║
║   PKCS7 Padding          ║
╚══════════════════════════╝
```

## Encryption Details

| Component                | Implementation             |
| ------------------------- | --------------------------- |
| Encryption Algorithm     | AES-256-CBC                 |
| Key Derivation           | PBKDF2                      |
| Iterations               | 100,000                     |
| Padding                  | PKCS7                       |
| Salt Strategy            | Unique salt per encryption  |

---

# ⌨️ Keyboard Shortcuts

| Action                    | Shortcut           |
| ------------------------- | ------------------ |
| Save Note                 | `Ctrl + S`         |
| New Note                  | `Ctrl + N`         |
| New Folder                | `Ctrl + Shift + N` |
| Global Quick Note         | `Ctrl + Insert`    |
| Focus on Folder Tree      | `Ctrl + F`         |
| Refresh                   | `F5`               |
| Clear Editor              | `Ctrl + W`         |
| Delete Item               | `Delete`           |

---

# ❓ FAQ

## Is KAIRUS really free?

Yes. KAIRUS can be used for free.

---

## Can I sync notes between devices?

Currently not. The system is designed to work locally and offline.

---

## What happens if I forget my password?

For security reasons, passwords cannot be recovered. The encryption is designed to prevent unauthorized access.

---

## Is KAIRUS available for Mac or Linux?

Currently the main focus is Windows 10 and 11.

---

## How secure is the encryption?

KAIRUS uses AES-256-CBC with PBKDF2 and 100,000 iterations, following modern security practices for local data protection.

---

## Can I export my notes?

Yes. You can export notes as PDF or TXT.

---

# ⚙️ Requirements

* Python 3.8+
* Windows 10/11
* 100MB free space

---

# 🧩 Project Structure

```bash
KAIRUS/
│
├── build/
├── core/
├── dist/
├── security/
├── storage/
├── ui/
├── utils/
├── web/
│   ├── css/
│   └── img/
│
├── main.py
├── kairus.spec
├── requirements.txt
├── build.bat
└── README.md
```

---

# 🛠️ Technologies

* Python
* AES-256 Encryption
* PBKDF2
* Local Storage
* PDF/TXT Export

---

# 📜 License

This project is licensed under the MIT License.

---

<div align="center">

# KAIRUS
© 2026 KAIRUS — All rights reserved.

</div>
```