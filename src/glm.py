from zhipuai import ZhipuAI
from src import settings

client = ZhipuAI(api_key=settings.api_key)  # 填写您自己的APIKey


def glm(query, system_file_path=r"./data/system_inp.txt"):
    with open(system_file_path, "r", encoding="utf-8") as f:
        system = f.read()
    response = client.chat.completions.create(
        model="glm-4-flash",  # 填写需要调用的模型编码
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": query},
        ],
        # stream=True,
    )

    # for chunk in response:
    #     rtn = chunk.choices[0].delta.content
    #     print(rtn, end="")
    #     yield rtn
    return response.choices[0].message.content


def first_step(query, retry=3):
    rtn = ""
    for i in range(retry):
        rtn = glm(query, system_file_path=r"./data/system_inp.txt")
        if "关键字" in rtn:
            break
    rtn = rtn.replace("关键字", "").replace("：", "").replace(":", "")
    return rtn.strip()



