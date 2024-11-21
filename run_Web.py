import os
import socket

import uvicorn
from datetime import datetime
from django.conf import settings
# import config file
log_ini_file = "log_config_Web.ini"
logs_path = "logs"
if not os.path.exists(logs_path):
    os.makedirs(logs_path)
print("Start service at %s" %(str(datetime.now())))
print("Press CTRL+C to quit")
if __name__ == "__main__":
    print(socket.gethostbyname(socket.gethostname()))
    config = uvicorn.Config("DuckBubi.asgi:application", host=socket.gethostbyname(socket.gethostname()), port=80,
    log_level="info", reload=True, use_colors=False, log_config=log_ini_file)
    server = uvicorn.Server(config)
    server.run()

#socket.gethostbyname(socket.gethostname())