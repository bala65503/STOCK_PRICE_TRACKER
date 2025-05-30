# Enhanced Stock Tracker with Tkinter UI and Additional Features

import yfinance as yf
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Function to fetch stock data
def get_stock_data(symbol, period='7d'):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {symbol}: {e}")
        return None

# Function to compare two stocks and plot their trends
def compare_stocks():
    sym1 = entry_symbol1.get().upper().strip()
    sym2 = entry_symbol2.get().upper().strip()
    period = period_var.get()

    if not sym1 or not sym2:
        messagebox.showwarning("Input Required", "Please enter both stock symbols.")
        return

    data1 = get_stock_data(sym1, period)
    data2 = get_stock_data(sym2, period)

    if data1 is not None and data2 is not None:
        fig, ax = plt.subplots(figsize=(6, 4))
        data1['Close'].plot(ax=ax, label=sym1)
        data2['Close'].plot(ax=ax, label=sym2)
        ax.set_title(f"{sym1} vs {sym2} - Close Price Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.grid(True)
        ax.legend()

        for widget in frame_plot.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Export stock data to CSV
def export_data():
    sym1 = entry_symbol1.get().upper().strip()
    sym2 = entry_symbol2.get().upper().strip()
    period = period_var.get()

    data1 = get_stock_data(sym1, period)
    data2 = get_stock_data(sym2, period)

    if data1 is not None:
        data1.to_csv(f"{sym1}_{period}.csv")
    if data2 is not None:
        data2.to_csv(f"{sym2}_{period}.csv")

    messagebox.showinfo("Exported", "Stock data exported successfully.")

# View detailed stock info
def show_stock_info():
    sym1 = entry_symbol1.get().upper().strip()
    sym2 = entry_symbol2.get().upper().strip()
    try:
        info1 = yf.Ticker(sym1).info
        info2 = yf.Ticker(sym2).info
        details = f"{sym1} Info:\nMarket Cap: {info1.get('marketCap')}\nPE Ratio: {info1.get('trailingPE')}\nDividend Yield: {info1.get('dividendYield')}\n\n"
        details += f"{sym2} Info:\nMarket Cap: {info2.get('marketCap')}\nPE Ratio: {info2.get('trailingPE')}\nDividend Yield: {info2.get('dividendYield')}"
        messagebox.showinfo("Stock Info", details)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve stock info: {e}")

# Setup UI
root = tk.Tk()
root.title("📊 Stock Price Tracker and Comparator")
root.geometry("800x600")
root.configure(bg="#2e3f4f")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2e3f4f", foreground="white")
style.configure("TButton", background="#3c4f65", foreground="white")
style.configure("TEntry", fieldbackground="#ffffff", foreground="black")

# Stock input
frame_input = ttk.Frame(root)
frame_input.pack(pady=10)

label1 = ttk.Label(frame_input, text="Stock Symbol 1:")
label1.grid(row=0, column=0, padx=5)
entry_symbol1 = ttk.Entry(frame_input)
entry_symbol1.grid(row=0, column=1, padx=5)

label2 = ttk.Label(frame_input, text="Stock Symbol 2:")
label2.grid(row=0, column=2, padx=5)
entry_symbol2 = ttk.Entry(frame_input)
entry_symbol2.grid(row=0, column=3, padx=5)

# Period selection
ttk.Label(frame_input, text="Select Period:").grid(row=1, column=0, padx=5, pady=5)
period_var = tk.StringVar()
period_choices = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"]
period_menu = ttk.Combobox(frame_input, textvariable=period_var, values=period_choices, state="readonly")
period_menu.set("7d")
period_menu.grid(row=1, column=1, columnspan=2)

# Buttons
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

btn_compare = ttk.Button(frame_buttons, text="Compare Stocks", command=compare_stocks)
btn_compare.grid(row=0, column=0, padx=10)

btn_export = ttk.Button(frame_buttons, text="Export Data", command=export_data)
btn_export.grid(row=0, column=1, padx=10)

btn_info = ttk.Button(frame_buttons, text="Stock Info", command=show_stock_info)
btn_info.grid(row=0, column=2, padx=10)

# Plot frame
frame_plot = ttk.Frame(root)
frame_plot.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()
