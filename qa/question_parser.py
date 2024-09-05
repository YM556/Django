from typing import List

from client.clientfactory import Clientfactory

from qa.prompt_templates import get_question_parser_prompt
from qa.purpose_type import purpose_map
from qa.purpose_type import userPurposeType

from model.KG.search_service import search
from model.KG.search_model import _Value

from icecream import ic


def parse_question(question: str,image_url) -> userPurposeType:

    if "文献" in question :
        return purpose_map["基于文件描述"]
    
    if "搜索" in question:
        return purpose_map["网络搜索"]

    # 在这个函数中我们使用大模型去判断问题类型
    prompt = get_question_parser_prompt(question)
    response = Clientfactory().get_client().chat_with_ai(prompt)
    print(response)

    if response == "图片生成":
        return purpose_map["图片生成"]
    if  response =="视频生成":
        return purpose_map["视频生成"]
    if  response =="PPT生成":
         return purpose_map["PPT生成"]
    if response == "音频生成":
        return purpose_map["音频生成"]
    if response == "图片描述":
        return purpose_map["图片描述"]
    if response == "文本生成":
        return purpose_map["其他"]
    return purpose_map["其他"]



def check_entity(question:str) -> List[_Value]|None:
    code,result = search(question)
    if code == 0:
        return result
    else:
        return None