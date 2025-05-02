import yfinance as yf
import matplotlib.pyplot as plt
import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Say the stock symbol (e.g., AAPL, TSLA): ")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        return query.upper().strip()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return None


def get_stock_price_and_plot(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="7d")  # Last 7 days
        price = data["Close"].iloc[-1]

        # Plotting
        data["Close"].plot(title=f"{symbol} - Last 7 Days Price Trend")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        return price
    except Exception as e:
        print(f"Error: {e}")
        return None
def check_price_alert(symbol, threshold):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        current_price = data["Close"].iloc[-1]

        print(f"🔍 Current price of {symbol} is {current_price:.2f}")
        
        if current_price >= threshold:
            alert_msg = f"Alert! {symbol} has reached {current_price:.2f}, which is above your threshold."
            print(alert_msg)
            speak(alert_msg)
        else:
            print(f"No alert. Current price is below your threshold of {threshold}")
    except Exception as e:
        print(f"Error checking alert: {e}")
        speak("There was an error checking the price alert.")


if __name__ == "__main__":
    symbol = listen()
    if symbol:
        price = get_stock_price_and_plot(symbol)
        if price:
            result = f"The current price of {symbol} is {price:.2f} dollars."
            print(result)
            speak(result)
        else:
            speak("Sorry, I couldn't find that stock.")
if symbol:
    try:
        # Ask user to enter a price threshold
        threshold = float(input(f"Enter your price alert threshold for {symbol}: "))
        check_price_alert(symbol, threshold)

        # Also fetch and plot the price trend
        price = get_stock_price_and_plot(symbol)
        if price:
            result = f"The current price of {symbol} is {price:.2f} dollars."
            speak(result)
        else:
            speak("Sorry, I couldn't fetch the price.")
    except ValueError:
        speak("Invalid threshold value entered.")

