from fastapi import APIRouter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List
from api.routers.schemas.commaOutputParser import CommaOutputParser
from api.routers.schemas.scenarioData import ScenarioData

router=APIRouter()

@router.post("/byScenario")
async def RSbyScenario(data:ScenarioData):
    # 첫 번째 단계: 시나리오를 바탕으로 주제 추출
    subject_chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.1)
    subject_template = ChatPromptTemplate.from_messages([
        ("system", "Based on scenarios, tell human what is the subject of each scenario. Generate a COMMA-SEPARATED LIST of one topic."),
        ("human", "Tell me what topic you are talking about based on the {scenario}.")
    ])

    # 주제 추출 프롬프트 생성 및 호출
    subject_prompt = subject_template.format_messages(scenario=data.scenarios)
    subject_response = subject_chat.invoke(subject_prompt)
    subject_list = CommaOutputParser().parse(subject_response.content)

    # 두 번째 단계: 추출된 주제를 바탕으로 대화 주제 추천
    recommend_subject_chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.1)
    recommend_template = ChatPromptTemplate.from_messages([
        ("system", "You are a subject generator. Generate a COMMA-SEPARATED LIST of 5 topics in Korean. Like this: Topic 1, Topic 2, Topic 3, Topic 4, Topic 5"),
        ("human", "Recommend conversation topics based on {subject} and {likeability}")
    ])

    # 추천 대화 주제 프롬프트 생성 및 호출
    recommend_prompt = recommend_template.format_messages(subject=subject_list, likeability=data.likeabilities)
    recommend_response = recommend_subject_chat.invoke(recommend_prompt)
    recommend_subject_list = CommaOutputParser().parse(recommend_response.content)

    return recommend_subject_list