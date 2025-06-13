
comment_map_prompt = '''
You are analyzing YouTube video comments.
Your task is to summarize the **main points, recurring opinions, and common themes** expressed by users in the following comments.

Instructions:
- Make the summary concise and informative.
- Use bullet points if it improves clarity.
- Focus on what users are collectively saying — not individual opinions.

Comments:
{text}
'''


comment_combine_prompt = '''
You are aggregating multiple summaries of YouTube video comments.
Based on the partial summaries below, write a **clear and concise final summary** that reflects the overall viewer sentiment and discussion.

Include:
- Common viewer sentiments
- Frequently discussed topics
- Notable praise, criticism, or contrasting opinions

Summaries:
{text}

Final Summary:
'''
