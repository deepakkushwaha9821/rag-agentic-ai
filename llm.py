from gpt4all import GPT4All
import os

MODEL_NAME = "qwen2.5-3b-instruct-q4_k_m.gguf"  # 👈 EXACT filename
MODEL_PATH = os.path.join(os.getcwd(), "models")

llm = GPT4All(
    model_name=MODEL_NAME,
    model_path=MODEL_PATH,
    device="cpu",
    allow_download=False   # 🔒 prevents 404
)

def generate(prompt: str) -> str:
    with llm.chat_session():
        return llm.generate(
            prompt,
            max_tokens=200,
            temp=0.4,
            top_k=65,
            top_p=1.0
        )
