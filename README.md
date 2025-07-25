# 🎮 Tic Tac Toe

This project allows you to play the classic **Tic Tac Toe** game in two different ways: through a graphical interface using **PyQt**, or via a **Telegram bot**.

---

## 🖥️ GUI Version (PyQt)

To play the game with a visually appealing window:

- Run the `pyqt_XO.py` file.
- A new window will open where you can play the game locally using a clean and intuitive interface.

---

## 🤖 Telegram Bot Version

To play the game directly in Telegram:

- Inside the script, find the `bot token` field and replace it with the token of your own Telegram bot.
- Run the `tbot_XO.py` file.
- Once updated, you can play the game through **your own bot** in Telegram.

---

## ⚙️ Features

- **Two Game Modes**:
  - 🟢 **Easy Mode** – A casual mode where you can win with some basic strategy.
  - 🔴 **Hard Mode** – Uses a **perfect algorithm** that guarantees the bot won't lose. You can only draw at best!

- **Character Selection**:
  - Choose whether you want to play as **X** or **O** before starting the game.

---

## 📦 Installation

To install the required dependencies, make sure you have Python 3 installed. Then run:

```bash
pip install -r requirements.txt
