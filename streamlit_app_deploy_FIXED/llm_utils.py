from groq import Groq

try:
    from google.colab import userdata
    GROQ_API_KEY = userdata.get('GROQ_API_KEY')
except Exception:
    import os
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'MASUKKAN_API_KEY_GROQ_DI_SINI')

groq_client = Groq(api_key=GROQ_API_KEY)
LLM_MODEL = 'llama-3.3-70b-versatile'


def call_llm(system_prompt, user_prompt, temperature=0.2, max_tokens=350):
    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
