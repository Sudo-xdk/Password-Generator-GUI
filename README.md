# 🔒 Password Generator GUI

A **Streamlit-based password generator** that creates **strong, unique, and customizable passwords** for different services using **PBKDF2-HMAC-SHA384**.  
It includes a **password strength meter**, **quick-access buttons for popular services**, and options to **copy or download passwords securely**.  
Your **master password is never stored or transmitted**, making it a **safe and private solution** for password management.

---

## ✨ Features
- 🛡️ **Secure Password Generation** using PBKDF2-HMAC-SHA384 with 150,000 iterations.  
- 🔑 **Master Password Based** – remember one key, generate unique passwords for each service.  
- ⚡ **Customizable Options** – choose password length, symbols, digits, exclude ambiguous characters.  
- 📊 **Password Strength Meter** – real-time strength analysis.  
- 🚀 **Quick Access** – preloaded with popular services (Google, GitHub, Facebook, etc.).  
- 📋 **Copy to Clipboard** or **Download Password** as a text file.  
- 🎨 **Streamlit Web GUI** with modern, hacker-style ASCII startup for Linux.  

---

## 🖥️ Installation

### Linux
```bash
# Clone repository
git clone https://github.com/Sudo-xdk/Password-Generator-GUI.git
cd Password-Generator-GUI
```

# Make scripts executable
```
chmod +x password_generator.sh
```
# Install dependencies
```
pip install -r requirements.txt
```
---
Windows

Install Python 3.12+ and pip.

Clone the repo using GitHub Desktop or Git Bash:
```
git clone https://github.com/Sudo-xdk/Password-Generator-GUI.git
cd Password-Generator-GUI
```
Install dependencies:
```
pip install -r requirements.txt
```
---
🚀 Usage
Linux

Run the GUI with:
```
./password_generator.sh
```
Windows
Run with:
```
streamlit run password_generator.py
```
---
📂 Project Structure
Password-Generator-GUI/
├── password_generator.py     # Main Streamlit GUI app
├── password_generator.sh     # Linux launcher with ASCII banner
├── install_deps.sh           # Linux dependency installer
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Ignore cache & venv files









