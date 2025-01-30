from transformers import pipeline
from huggingface_hub import InferenceClient



# Generate the summary using LLM - summarization model
def generate_summary(news_data, use_local_llm=True):

    # Extract input prompts from dict
    input_prompts = news_data['input_prompts']

    # Initalize LLM summary pipeline
    if use_local_llm:
        llm_client = pipeline("summarization", model="facebook/bart-large-cnn")
    else:
        llm_client = InferenceClient(model="facebook/bart-large-cnn")

    out_dict = {}
    # Iterate over each prompt
    for news_title, news_content in input_prompts.items():

        # Calculate summary
        if use_local_llm:
            out_summary = llm_client(news_content, do_sample=False)
        else:
            out_summary = llm_client.summarization(news_content)
            
        if len(out_summary) != 0:
            
            # Save summary
            out_dict[news_title] = out_summary[0]['summary_text']

    return out_dict
