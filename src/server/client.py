import requests
from fastapi import Request
from hwp_reader import get_hwp_text
if __name__ == "__main__":
    while True:
        cmd = list(input().split())
        if cmd[0] == "create":
            params = {"index_name": cmd[1]}
            response = requests.post("http://127.0.0.1:8001/create", params=params)
            if response.json():
                print("index created successfully")
        elif cmd[0] == "upload":
            path = " ".join(cmd[3:])
            content = get_hwp_text(path)
            params = {"index_name": cmd[1], "title": cmd[2], "content": content}
            response = requests.post("http://127.0.0.1:8001/upload", params=params)
            if response.json():
                print("index uploaded successfully")  
        else:
            text= " ".join(cmd[2:])
            params = {"index_name": cmd[1], "text": text}
            response = requests.post("http://127.0.0.1:8001/chat", params=params)
            result = response.json()
            print(f"\nyou: {text}")
            print(f"\ncat-gpt: {result['result']}\n")