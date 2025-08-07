import json
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')

slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)


@slack_app.shortcut("delete-all-threads")
def delete_all_threads(ack, shortcut, client: WebClient):
    try:
        ack()
        print("\nAtajo invocado con éxito:\n", shortcut, "\n")

        channel_id = shortcut['channel']['id']
        thread_ts = shortcut['message_ts']

        # Llamar a la función para eliminar los mensajes del hilo
        delete_thread_messages(client, channel_id, thread_ts)
        client.chat_postMessage(
            channel=channel_id, 
            text=" "
        )
        print("Mensaje de confirmación enviado.")
    except SlackApiError as e:
        print(f"Error al ejecutar el atajo: {e.response['error']}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")


def delete_thread_messages(client: WebClient, channel_id, thread_ts):
    try:
        response = client.conversations_replies(channel=channel_id, ts=thread_ts)
        messages = response.get('messages', [])


        for message in messages:
            try:
                if message.get("user") == client.auth_test()["user_id"]:
                    client.chat_delete(channel=channel_id, ts=message['ts'])
                    print(f"Mensaje eliminado: {message['ts']}")
                else:
                    print(f"No se puede eliminar el mensaje: {message['ts']} (no es del bot)")
            except SlackApiError as e:
                print(f"Error al eliminar mensaje {message['ts']}: {e.response['error']}")
    except SlackApiError as e:
        print(f"Error al obtener los mensajes del hilo: {e.response['error']}")
    except Exception as e:
        print(f"Error inesperado al eliminar mensajes: {str(e)}")


if __name__ == "__main__":
    try:
        print("Iniciando la aplicación Slack...")
        SocketModeHandler(slack_app, SLACK_APP_TOKEN).start()
    except Exception as e:
        print(f"Error crítico al iniciar la aplicación: {str(e)}")
