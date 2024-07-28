from Stephany import Stephany

api_key = 'AIzaSyDR-yzVIRiFoQqWsdT3tNX2BcR_T4TcAQQ'

db_config = {
    'user': 'avnadmin',
    'password': 'AVNS_fOnqMRAe1yWi236icem',
    'host': 'mysql-luthymakeup-luthymakeup.i.aivencloud.com',
    'database': 'defaultdb',
    'port': '13214'
}

chatbot = Stephany(api_key, db_config)
while(True):
    message = input()
    response = chatbot.send_message(message)
    print(response)