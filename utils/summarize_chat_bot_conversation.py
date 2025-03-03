from .prompt import get_summarize_prompt
from .llm import run_chat_others

def summarize(convo_data):
  """Gets all data from the stack i.e. conversation history
  and summarizes it using custom prompt and SLM"""
  summarizing_prompt = get_summarize_prompt(convo_data)
  print("Summarizing prompt: ", summarizing_prompt)
  summary = run_chat_others(summarizing_prompt)
  # print(summary)
  return summary