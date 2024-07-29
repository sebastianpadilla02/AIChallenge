from BackEnd.Stephany import Stephany
from BackEnd.Stephany_Employees import Stephany2

api_key = 'AIzaSyDR-yzVIRiFoQqWsdT3tNX2BcR_T4TcAQQ'

db_config = {
    'user': 'avnadmin',
    'password': 'AVNS_fOnqMRAe1yWi236icem',
    'host': 'mysql-luthymakeup-luthymakeup.i.aivencloud.com',
    'database': 'defaultdb',
    'port': '13214'
}

dec = input("¿Desea usar el chatbot de empleados? (s/n): ")
if dec == 's':
    chatbot = Stephany2(api_key, db_config)
else:
    chatbot = Stephany(api_key, db_config)
    
while(True):
    message = input()
    response = chatbot.send_message(message)
    print(response)