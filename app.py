from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

# Opening price ko global variable me store karenge
opening_price = None

@app.route('/get_banknifty_price', methods=['GET'])
def get_live_banknifty_price():
    global opening_price

    banknifty = yf.Ticker("^NSEBANK")
    hist = banknifty.history(period="1d", interval="1m")

    if hist.empty:
        return jsonify({"error": "Data fetch nahi ho raha"}), 500

    if opening_price is None:
        opening_price = hist.iloc[0]['Open']

    live_data = banknifty.history(period="1d", interval="1m")
    if live_data.empty:
        return jsonify({"error": "Live data nahi mil raha"}), 500

    current_price = live_data['Close'].iloc[-1]
    change = current_price - opening_price
    trend = "📈 Market Positive Hai!" if change > 0 else "📉 Market Negative Hai!"

    return jsonify({
        "current_price": round(current_price, 2),
        "change": round(change, 2),
        "trend": trend
    })

if __name__ == '__main__':
    app.run(debug=True)
