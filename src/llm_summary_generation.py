from llm_summary.summary_data_pull import get_data
from llm_summary.llm_summary import generate_summary


def generate_summary_output():
    data = get_data()
    summary = generate_summary(text_to_summarize=data)

    return summary

if __name__ == "__main__":
    output = generate_summary_output()
    print(output)