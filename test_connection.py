import os
from dotenv import load_dotenv
from services import user_service as us
import yaml
from yaml.loader import SafeLoader

from services.income_service import get_user_incomes



def test_method():
    result = get_user_incomes(3)
    res_obj = dict()
    for res in result:
        res_obj[res.user_id] = [res.income_id, res.month, res.amount_encrypted, res.income_type_id, res.income_frequency_id]
    print(res_obj)
    return res_obj
    


if __name__ == "__main__":
    test_method()
