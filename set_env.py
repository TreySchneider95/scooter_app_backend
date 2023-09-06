from dotenv import set_key
from pathlib import Path
from datetime import datetime

env_file_path = Path(".env")

def bird_set(access, refresh, uuid):
    # Save some values to the file.
    set_key(dotenv_path=env_file_path, key_to_set="BIRD_ACCESS", value_to_set=access)
    set_key(dotenv_path=env_file_path, key_to_set="BIRD_REFRESH", value_to_set=refresh)
    set_key(dotenv_path=env_file_path, key_to_set="BIRD_LAST_REFRESH", value_to_set=str(datetime.now()))
    set_key(dotenv_path=env_file_path, key_to_set="BIRD_UUID", value_to_set=str(uuid))
    return "set new bird keys"
