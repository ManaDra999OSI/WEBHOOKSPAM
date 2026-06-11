import os
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("URL_DISCORD")

def executar_bloco_10s():
    """
    Quando o cronjob de 1 minuto bater aqui, este loop vai rodar
    6 vezes (6 x 10 segundos = 60 segundos), cobrindo o minuto inteiro.
    """
    if not DISCORD_WEBHOOK_URL:
        print("ERRO: Variável 'URL_DISCORD' não configurada.")
        return

    payload = {
        "content": "Aviso automático enviado a cada 10 segundos via Cronjob! 🚀"
    }

    for i in range(6):
        try:
            resposta = requests.post(DISCORD_WEBHOOK_URL, json=payload)
            print(f"Disparo {i+1}/6 enviado ao Discord. Status: {resposta.status_code}")
        except Exception as e:
            print(f"Falha na conexão no disparo {i+1}: {e}")
        
        # Espera 10 segundos antes do próximo disparo dentro do mesmo minuto
        time.sleep(10)

@app.route("/disparar-discord", methods=["GET", "POST"])
def webhook_receptor():
    # O cronjob externo bate aqui a cada 1 minuto, e o Python assume o controle dos 10s
    executar_bloco_10s()
    return jsonify({"status": "sucesso", "mensagem": "Bloco de 10 segundos finalizado"}), 200

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
