from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAASlPe5YthwBO3KG926GZCpkdBNkDAtp2noWycJZA81gP5F7URezL4rHRSrEGl5DYeXJRJjZCOU43AGlZCR01SxZBNiZCnJikuPQqmrOoeLGF1FtgXIKFJQWuxktNdBLnu0O337hnQlRsZAOxBCi4DjQZAO0OA6WZCeXfZBDjtmJVjXqTJD7GoLYHDBFs2kAaMl5dEZBrk8401nrkmBAv9OGBkZAX4dGx02n"
PHONE_NUMBER_ID = "529601030236944"

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

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Billing App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        input, button {
            margin: 10px 0;
            padding: 10px;
            width: 100%;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
        }
    </style>
</head>
<body>
    <h1>Billing App</h1>
    <form id="billForm">
        <label for="customerNumber">Customer WhatsApp Number:</label>
        <input type="text" id="customerNumber" placeholder="Enter WhatsApp Number" required>

        <label for="itemDetails">Item Details:</label>
        <textarea id="itemDetails" placeholder="Enter item details here" rows="5" required></textarea>

        <label for="totalAmount">Total Amount:</label>
        <input type="text" id="totalAmount" placeholder="Enter total amount" required>

        <button type="button" onclick="sendBill()">Send Bill</button>
    </form>
    <p id="response"></p>
    <script>
        async function sendBill() {
            const customerNumber = document.getElementById('customerNumber').value;
            const itemDetails = document.getElementById('itemDetails').value;
            const totalAmount = document.getElementById('totalAmount').value;

            const responseElement = document.getElementById('response');
            responseElement.textContent = "Sending...";

            const response = await fetch('/send-bill', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ customerNumber, itemDetails, totalAmount })
            });

            const result = await response.json();
            responseElement.textContent = result.message || "Bill sent successfully!";
        }
    </script>
</body>
</html>

"""
@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

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
