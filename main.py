import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
load_dotenv()



# 세션별 대화 기록 저장소 관리
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """세션별 대화 기록을 저장하고 관리"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def send_message(user_input, session_id):
    # 모델 초기화 - 온도 매개변수 추가하여 응답 일관성 향상
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 도움이 되는 AI 비서입니다. 사용자의 질문에 한국어로 친절하게 답변하고, 이전 대화 내용을 기억하여 맥락에 맞는 응답을 제공합니다."),
        ("placeholder", "{history}"),
        ("human", "{input}")
    ])
    # 대화 체인 생성
    chain = prompt | llm
    # 대화 기록 관리 체인 생성
    conversation_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    # 에러 처리 함수 추가
    try:
        response = conversation_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        return response
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"



def main():
    # 대화 시뮬레이션
    session_id = "user_session_1"


    # 'quit'을 입력할 때까지 실행되는 루프
    while True:
        user_input = input("> ")
        # 사용자가 'quit'을 입력하면 루프를 종료하고 작별 인사
        if user_input.lower() == 'quit':
            print('Goodbye')
            break

        response = send_message(user_input, session_id)
        print(f"Assistant: {response.content}")



if __name__ == '__main__':
    main()
