from llm_summary.summary_data_pull import get_data
from llm_summary.llm_summary import generate_summary
from discord_webhook import send_discord_message


def generate_summary_output():
    data = get_data()
    summary = generate_summary(text_to_summarize=data)
    send_discord_message(summary)

    return summary

if __name__ == "__main__":
    output = generate_summary_output()
    print(output)