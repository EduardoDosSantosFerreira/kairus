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