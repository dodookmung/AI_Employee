import os
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 환경 변수 로드
load_dotenv()

# 세션별 대화 기록 저장소 관리
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def send_message(user_input, session_id):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 도움이 되는 AI 비서입니다. 사용자의 질문에 한국어로 친절하게 답변하고, 이전 대화 내용을 기억하여 맥락에 맞는 응답을 제공합니다."),
        ("placeholder", "{history}"),
        ("human", "{input}")
    ])
    chain = prompt | llm
    conversation_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    try:
        response = conversation_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        return response.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

# GUI 구현
def send_button_clicked():
    user_input = user_entry.get()
    user_entry.delete(0, tk.END)

    if user_input.lower() == 'quit':
        window.destroy()
        return

    thinking_popup=show_popup_message(window, "생각 중...")
    window.update_idletasks()

    if user_input.strip():
        chat_display.insert(tk.END, f"You: {user_input}\n", "user")
        response = send_message(user_input, "user_session_1")
        thinking_popup.destroy()
        chat_display.insert(tk.END, f"AI assistant: {response}\n", "ai")
        chat_display.yview(tk.END)

def on_enter(event):
    send_button_clicked()
# 로딩 팝업 창
def show_popup_message(window, message):
    popup = tk.Toplevel(window)
    popup.title('GPT-4o-mini')

    # 팝업 창의 내용
    label=tk.Label(popup, text=message, font=('맑은 고딕', 12))
    label.pack(expand=True, fill=tk.BOTH)
    # 팝업 창의 크기 조절
    popup_width=400
    popup_height=100
    popup.geometry(f"{popup_width}x{popup_height}")
    # 팝업 창의 중간에 위치
    window_x=window.winfo_x()
    window_y=window.winfo_y()
    window_width=window.winfo_width()
    window_height=window.winfo_height()

    popup_x=window_x + window_width // 2 - popup_width // 2
    popup_y=window_y + window_height // 2 - popup_height // 2
    popup.geometry(f"+{popup_x}+{popup_y}")

    popup.transient(window)
    popup.attributes("-topmost", True)
    popup.update()

    return popup

# Tkinter 윈도우 생성
window = tk.Tk()
window.title("Chatbot with LangChain")
# window.geometry("500x600")
font=("맑은 고딕", 10)

# 채팅 표시창
chat_display = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=25, state=tk.NORMAL, bg='#f0f0f0')
chat_display.tag_configure("user", foreground="blue", background="#c9daf8") # 추천 레드?
chat_display.tag_configure("ai", foreground="green", background="#e4e4e4")
chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

input_frame = tk.Frame(window)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# 입력창
user_entry = tk.Entry(input_frame)
user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
user_entry.bind("<Return>", on_enter)

# 전송 버튼
send_button = tk.Button(input_frame, text="Send", command=send_button_clicked)
send_button.pack(side=tk.RIGHT)

# GUI 실행
window.mainloop()
