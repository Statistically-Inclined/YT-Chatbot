
transcript_map_prompt = '''
You are analyzing a segment of a YouTube video transcript.
Your task is to identify and summarize the **main ideas, insights, or recurring themes** in this transcript chunk.

Guidelines:
- Focus on key arguments, events, or opinions.
- Avoid repeating details or filler content.
- Use bullet points if it enhances clarity.

Transcript Segment:
{text}

Summary:
'''


transcript_combine_prompt = '''
You are an expert summarizer reviewing multiple segment-level summaries of a YouTube video transcript.
Your task is to create a **final, cohesive summary** that accurately represents the overall content of the video.

Instructions:
- Structure the summary logically and concisely.
- Reflect the key ideas and themes across all segments.
- Use clear, professional language throughout.
- Bullet points are encouraged for major themes.
- Optionally, end with a brief concluding insight or takeaway.

Partial Summaries:
{text}

Final Summary:
'''
