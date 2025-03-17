import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()


def ask_to_llm(user_input):
    # 모델 초기화 - 온도 매개변수 추가하여 응답 일관성 향상
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    # 프롬프트 템플릿 개선 - 시스템 메시지를 더 상세하게 작성
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 도움이 되는 AI 비서입니다. 사용자의 질문에 한국어로 친절하게 답변합니다."),
        ("user", "{user_input}")
    ])
    # 대화 체인 생성
    chain = prompt | llm

    response = chain.invoke(user_input)
    return response.content


user_request = "지구의 자전 주기는?"

r=ask_to_llm(user_request)
print(r)