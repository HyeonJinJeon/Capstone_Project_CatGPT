import uvicorn
import openai
import json
from hwp_reader import get_hwp_text
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from fastapi import FastAPI, File, UploadFile, Form
from typing import List
from key import api_key

openai.api_key = api_key
origins = [
    "http://localhost:8080",
]

app = FastAPI()
#CORS 보안 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"
es = Elasticsearch("http://127.0.0.1:9200", request_timeout=300, max_retries=5)

@app.post("/create", description="create_elasticindex")
async def create(index_name):
    if es.indices.exists(index = index_name):
        return False
    with open("setting.json") as f:
        setting = json.load(f)
    es.indices.create(index=index_name, body= setting)
    return True

@app.post("/upload", description="upload_txt")
async def upload(files: List[UploadFile]=File(...), text = Form(...)):
    index_name = text
    print(index_name)
    if not es.indices.exists(index = index_name):
        with open("setting.json") as f:
                setting = json.load(f)
        es.indices.create(index=index_name, body= setting)
    for file in files:
        contents = await file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)
        content = get_hwp_text(file.filename)
        if not es.indices.exists(index = index_name):
            print(f"index({index_name}) is not in es")
            return False
        doc = {
            "title" : file.filename,
            "content": content
        }
        es.index(index=index_name, document=doc)
    return True

messages = [
        {"role": "system", "content": "You are a helpful assistant."},

    ]

@app.post("/chat", description="input text to model and return result")
async def chat(req:Request):
    answer = ""
    data = await req.body()
    data = eval(data.decode("utf-8"))
    text = data["text"]
    index_name = data["index_name"]
    query = {
        # "min_score": 0.5,
        "query": {
            "bool": {
                "must": [
                    {"match": {"content": f"{text}"}}
                ]
            }
        }
    }
    print(query)
    res = es.search(index=index_name, body=query, size=1)
    print(res)
    if res["hits"]["hits"]:
        chat = f"{res['hits']['hits'][0]['_source']['content']} 에서 {text}"
    else:
        answer = "해당 질문에 대한 문서를 찾지 못했습니다 따라서 해당 답변은 chat gpt에서 문서 정보 없이 생성한 문장입니다. \n \n"
        chat = text
    messages.append({"role": "user", "content": f"{chat}"})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer += response['choices'][0]['message']['content']
    messages.append({"role": "system", "content": answer})
    return answer


if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port=8002)