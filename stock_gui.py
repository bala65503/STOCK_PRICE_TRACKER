import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import matplotlib.pyplot as plt
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="7d")
    if data.empty:
        raise ValueError("Invalid stock symbol")
    price = data["Close"].iloc[-1]
    
    # Plotting
    data["Close"].plot(title=f"{symbol.upper()} - Last 7 Days")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return price

def track_stock():
    symbol = symbol_entry.get().strip()
    threshold_str = threshold_entry.get().strip()

    if not symbol:
        messagebox.showwarning("Input Error", "Please enter a stock symbol.")
        return

    try:
        threshold = float(threshold_str) if threshold_str else None
        price = get_stock_price(symbol)
        
        result_text = f"Current price of {symbol.upper()}: {price:.2f} USD"
        result_label.config(text=result_text)
        speak(result_text)

        if threshold and price >= threshold:
            alert_msg = f"Alert! {symbol.upper()} has crossed {threshold:.2f}."
            messagebox.showinfo("Price Alert", alert_msg)
            speak(alert_msg)
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        messagebox.showerror("Error", error_msg)
        speak("Sorry, could not fetch stock data.")

# GUI Window
app = tk.Tk()
app.title("Stock Price Tracker")
app.geometry("400x300")
app.config(padx=20, pady=20)

tk.Label(app, text="Stock Symbol:").pack()
symbol_entry = tk.Entry(app)
symbol_entry.pack()

tk.Label(app, text="Price Alert Threshold (optional):").pack()
threshold_entry = tk.Entry(app)
threshold_entry.pack()

tk.Button(app, text="Track Stock", command=track_stock).pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 12), fg="green")
result_label.pack()

app.mainloop()
