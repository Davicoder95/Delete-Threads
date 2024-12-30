import json
import os

from dotenv import load_dotenv
# from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')


# app = Flask(__name__)
# client = WebClient(token=SLACK_BOT_TOKEN)

slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)


@slack_app.shortcut("delete-all-threads")
def delete_all_threads(ack, shortcut, client: WebClient):
    ack()

    print()
    print(shortcut)
    print()
    channel_id = shortcut['channel']['id']
    thread_ts = shortcut['message_ts']

    # # Llamar a la función para eliminar los mensajes del hilo
    delete_thread_messages(client, channel_id, thread_ts)
    client.chat_postMessage(
        channel=channel_id, text="Se han eliminado todos los mensajes del hilo.")


# @app.route('/actions', methods=['POST'])
# def interactive():
#     payload = request.form.get('payload')  # Obtener el payload de la acción del botón
#     if not payload: return jsonify({"text": "No se procesó ninguna acción."})

#     data = json.loads(payload)

#     print(data)

#     # Verificar si la acción es "eliminar todos"
#     # if data['callback_id'] == 'delete-all-threads':
#     #     channel_id = data['channel']['id']
#     #     thread_ts = data['message_ts']

#     # #     # Llamar a la función para eliminar los mensajes del hilo
#     #     delete_thread_messages(channel_id, thread_ts)
#     #     return jsonify({"text": "Se han eliminado todos los mensajes del hilo."})


def delete_thread_messages(client: WebClient, channel_id, thread_ts):
    response = client.conversations_replies(
        channel=channel_id, ts=thread_ts)

    print()
    print({'response': response})
    print()

    messages = response['messages']

    print()
    print({'response': response})
    print()

    for message in messages:

        client.chat_delete(channel=channel_id, ts=message['ts'])
        print(f"Mensaje eliminado: {message['ts']}")
    # try:
    # except SlackApiError as e:
    #     print(f"Error al eliminar mensajes: {e.response['error']}")


# @app.route('/add-button', methods=['POST'])
# def add_button():
#     data = request.json
#     channel_id = data['channel_id']
#     message_ts = data['message_ts']  # Obtiene el timestamp del mensaje al que agregar el botón

#     try:
#         # Agregar un botón al mensaje enviado
#         response = client.chat_postMessage(
#             channel=channel_id,
#             text="Opciones avanzadas:",  # Mensaje con el botón
#             thread_ts=message_ts,  # Usar thread_ts si se trata de un mensaje en un hilo
#             blocks=[  # Estructura del botón
#                 {
#                     "type": "actions",
#                     "elements": [
#                         {
#                             "type": "button",
#                             "text": {
#                                 "type": "plain_text",
#                                 "text": "Eliminar todos"  # Texto que aparecerá en el botón
#                             },
#                             "action_id": "delete_all",  # Identificador de la acción
#                             "value": message_ts  # Enviamos el timestamp del mensaje como valor
#                         }
#                     ]
#                 }
#             ]
#         )

#         # Respondemos con éxito
#         return jsonify({"status": "success"})
#     except SlackApiError as e:
#         print(f"Error al agregar botón: {e.response['error']}")
#         return jsonify({"status": "error", "error": e.response['error']})

if __name__ == "__main__":
    SocketModeHandler(slack_app, SLACK_APP_TOKEN).start()
