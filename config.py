# Author: Yuanhao(Michael) Zheng - Email: likeping13@gmail.com  
#         Sachin Malik           - Email: Sachin.Malik@intersystems.com
#         Jianjie(Quentin) Yu    - Email: Jianjie.Yu@InterSystems.com
#         Harshitha Acha         - Email: Harshitha.Acha@InterSystems.com
#
#This file is used to put the Azure application credentials
#Chaneg the MicrosoftAppId and MicrosoftAppPassword to meet your own Azure app details

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "bc4fdbe8-a324-4513-bcc7-5510260dd85d")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "jfor5qLdi8pf8t5Cjj-Hz_~9-KjA.vgb4_")
