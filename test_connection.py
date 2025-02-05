import os
from dotenv import load_dotenv
from services import income_service as ins




def test_method():
    result = ins.get_income_categories()
    print(result)
    return result

if __name__ == "__main__":
    test_method()
