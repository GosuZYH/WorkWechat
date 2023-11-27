import os

ROAMING_PATH = os.getenv("APPDATA")  #Users/user/Appdata/Roaming
DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
LOG_PATH = os.path.join(DATA_PATH, "log")
appdata = os.getenv("APPDATA")       
   #Roaming/SMR path

# data_path = os.path.join(appdata, "SMR")
# if not os.path.exists(data_path):
#     os.mkdir(data_path)

# log_path = os.path.join(data_path, "log")   #Roaming/SMR/log
# if not os.path.exists(log_path):
#     os.mkdir(log_path)

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)