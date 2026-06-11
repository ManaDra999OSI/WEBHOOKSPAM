import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# O Python agora vai buscar a URL de forma segura dentro das configurações da Render
DISCORD_WEBHOOK_URL = os.environ.get("URL_DISCORD")


def enviar_para_discord():
    print("Acordando o script... Enviando mensagem para o Discord!")

    # Se você esqueceu de configurar a variável na Render, o código avisa o erro
    if not DISCORD_WEBHOOK_URL:
        print(
            "ERRO: A variável de ambiente 'URL_DISCORD' não foi encontrada na Render!"
        )
        return

    payload = {
        "content": "Olá! Este é um aviso automático enviado a cada 30 minutos direto da nuvem! 🚀"
    }

    try:
        resposta = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if resposta.status_code == 204:
            print("Mensagem enviada com sucesso ao Discord!")
        else:
            print(
                f"Erro ao enviar para o Discord: {resposta.status_code} - {resposta.text}"
            )
    except Exception as e:
        print(f"Falha na conexão: {e}")


@app.route("/disparar-discord", methods=["GET", "POST"])
def webhook_receptor():
    enviar_para_discord()
    return (
        jsonify({"status": "sucesso", "mensagem": "Comando enviado ao Discord"}),
        200,
    )


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)
