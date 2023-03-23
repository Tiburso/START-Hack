from flask import Flask, request,Response, jsonify
from base64 import b64encode, b64decode
import requests

app = Flask(__name__)

URL = "http://localhost/api/v1"
api = "token bdbfa48fcab6f150b15b22c07c82ab2c11178425"
api_header = { "Authorization": api }

STOREID = "Apg8Ceso5ZbUuZk7Kww6gkCZ4MJhGjgNveacGRiMCd9N"
GAME = {
    "name": "Idle Paladin", 
    "cost": "5",
    "ipfsLink": b64encode("asdasdasdasdasd".encode()).decode()
}

user = "admin@admin.pt"
password = "admin1"
encoded = b64encode(f"{user}:{password}".encode()).decode()
basic = f"Basic {encoded}"
basic_header = { "Authorization": basic }


@app.route("/user", methods=["GET"])
def users():
    r = requests.get(URL + '/api-keys/current', headers=api_header)
    print(r.content, r.status_code, r.reason)
    print(r.status_code, r.reason)

    print(api_header)


    return Response(status=r.status_code)


@app.route("/pay", methods=["POST"])
def pay():

    body = {
        "metadata": {
            "game-name": GAME["name"],
            "ipfsLink": b64decode(GAME["ipfsLink"]).decode(),
        },
        "checkout": {
            "speedPolicy": "HighSpeed",
            "defaultPaymentMethod": "BTC",
            "expirationMinutes": 90,
            "monitoringMinutes": 90,
            "paymentTolerance": 0,
            "redirectURL": "string", # probably mudar com frontend
            "redirectAutomatically": True,
            "requiresRefundEmail": True,
            "checkoutType": None,
        },
        "receipt": {
            "enabled": True,
            "showQR": True,
            "showPayments": True
        },
        "amount": GAME["cost"],
        "currency": "USD",
        "additionalSearchTerms": [ GAME["ipfsLink"] ]
    }
    
    r = requests.post(URL + '/stores/'+STOREID+'/invoices', json=body, headers=api_header)
    # ver se precisamos mais alguma coisa desta resposta

    if r.status_code != 200:
        return Response(status=r.status_code) 

    return jsonify( r.json() ), 200
    

@app.route("/receive-payment", methods=["POST"])
def payment():
    req = request.get_json()
    
    meta = req["metadata"]  
    timestamp = req["timestamp"]
    
    pay = req["payment"]
    value = pay["value"]
    
    # add the game to the user 
    
    # need to create a pull payment refering to 75% of the payment 
    ret_val = value * 0.75
    
    body = {
        "name": "Return fee",
        "description": "Value returned to vault wallet",
        "amount": ret_val,
        "currency": "BTC",
        "period": 604800,
        "BOLT11Expiration": None,
        "autoApproveClaims": True,
        "startsAt": timestamp,
        "expiresAt": timestamp + 60 * 5, # five minutes to deliver payment to main wallet
        "paymentMethods": 
        [
            "BTC"
        ]
    }
    
    
    res = requests.post(URL + f"/stores/{STOREID}/pull-payments", json=body, headers=api_header)
    
    if res.status_code != 200:
        return Response(status=400)
    
    pullPaymentId = res.json()["id"]
    
    # finalize that pull payment with a payout
    body = {
        "destination": "VAULT_COIN_ADDRESS",
        "amount": ret_val,
        "paymentMethod": "BTC"
    }
    
    res = requests.post(URL + f"/pull-payments/{pullPaymentId}/payouts",json=body, headers=api_header)
    
    return Response(status=res.status_code) 
    

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)