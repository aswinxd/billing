from flask import Flask, request, jsonify
from flask import render_template
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAASlPe5YthwBO3KG926GZCpkdBNkDAtp2noWycJZA81gP5F7URezL4rHRSrEGl5DYeXJRJjZCOU43AGlZCR01SxZBNiZCnJikuPQqmrOoeLGF1FtgXIKFJQWuxktNdBLnu0O337hnQlRsZAOxBCi4DjQZAO0OA6WZCeXfZBDjtmJVjXqTJD7GoLYHDBFs2kAaMl5dEZBrk8401nrkmBAv9OGBkZAX4dGx02n"
PHONE_NUMBER_ID = "529601030236944"


@app.route('/')
def index():
    return render_template('index.html')

def send_whatsapp_message(number, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


@app.route('/send-bill', methods=['POST'])
def send_bill():
    data = request.json
    customer_number = data['customerNumber']
    item_details = data['itemDetails']
    total_amount = data['totalAmount']

    bill_message = f"Hello! Here is your bill:\n\n{item_details}\n\nTotal: {total_amount}\nThank you for your business!"
    response = send_whatsapp_message(customer_number, bill_message)

    if response.get("messages"):
        return jsonify({"message": "Bill sent successfully!"})
    else:
        return jsonify({"message": "Failed to send bill.", "error": response}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8280)
