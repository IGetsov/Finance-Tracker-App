import os
from dotenv import load_dotenv
from services import user_service as us
import yaml
from yaml.loader import SafeLoader



def test_method():
    # result = us.view_users()
    # users = dict()
    # for res in result:
    #     users[res.user_id] = [res.username, res.password_hash]
    # print(users)
    # return users
    with open("credentials.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)
        print(config)
        return config


if __name__ == "__main__":
    test_method()
