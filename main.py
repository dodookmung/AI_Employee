import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()


def ask_to_llm(user_input):
    # 모델 초기화 - 온도 매개변수 추가하여 응답 일관성 향상
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Joker of Batman movie. You must pretend like Joker of the story. When you speak in Korea, you must use 반말."),
        ("user", "{user_input}")
    ])
    # 대화 체인 생성
    chain = prompt | llm

    response = chain.invoke(user_input)
    return response.content


user_request = "I'm the Batman!"

r=ask_to_llm(user_request)
print(r)