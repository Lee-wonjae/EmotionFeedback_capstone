from fastapi import APIRouter
from langchain.schema import BaseOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List
from api.routers.schemas.commaOutputParser import CommaOutputParser
from api.routers.schemas.profileData import profileData
    
router=APIRouter()


@router.post("/byProfile")
async def RSbyProfile(data:profileData):
    
    subject_chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.3)
    subject_template = ChatPromptTemplate.from_messages([
    ("system", "Based on the detailed profile including interest, recommend direct and not boring subjects for discussion. Generate a COMMA-SEPARATED LIST of 5 topics in Korean. Like this: Topic 1, Topic 2, Topic 3, Topic 4, Topic 5"),
    ("human", "Based on my interests of {interest}, could you suggest topics we could discuss?")
    ])
    subject_prompt = subject_template.format_messages(interest=data.interests)
    subject_response = subject_chat.invoke(subject_prompt)
    subject_list = CommaOutputParser().parse(subject_response.content)
    subject_list
    return subject_list