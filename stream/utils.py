import requests

BOT_TOKEN = "7173172649:AAEHeNcjyEIMz7u-G_-7rUKXwAwQyYZXWcg"

def send_error_msg(msg):
    user_ids = [1304563494]
    for user_id in user_ids:
        try:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            data = {
                "chat_id": user_id,
                "text": str(msg)
            }
            requests.post(url=url, data=data)
        except Exception as e:
            print(e)