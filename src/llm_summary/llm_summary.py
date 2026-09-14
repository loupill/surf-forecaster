import os
from dotenv import load_dotenv
import anthropic
import pandas as pd

load_dotenv()

client = anthropic.Anthropic()

def generate_summary(text_to_summarize: pd.DataFrame) -> str:
    data_csv = text_to_summarize.to_csv(index=False)
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "You're summarizing a week of forecasted surf scores for Belmar, NJ. "
                    "Identify which days look best, note any standout conditions, and give "
                    "a short overall outlook for the week. Keep it concise and casual, "
                    "suitable for a Discord message.\n\n"
                    f"{data_csv}"
                )
            }
        ]
    )
    for block in response.content:
        if block.type == "text":
            return block.text
    raise ValueError("No text block found in response")