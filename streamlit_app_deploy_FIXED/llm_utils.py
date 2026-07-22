import os
from groq import Groq

try:
    import streamlit as st
except Exception:
    st = None


def _get_groq_api_key() -> str:
    # 1) Kalau dijalankan di Google Colab
    try:
        from google.colab import userdata
        key = userdata.get("GROQ_API_KEY")
        if key:
            return key
    except Exception:
        pass

    # 2) Streamlit Cloud / lokal (.streamlit/secrets.toml) — paling diutamakan
    #    karena paling konsisten dibanding mengandalkan mirror ke os.environ.
    if st is not None:
        try:
            key = st.secrets["GROQ_API_KEY"]
            if key:
                return key
        except Exception:
            pass

    # 3) Environment variable biasa (misal saat dijalankan lokal lewat .env)
    return os.getenv("GROQ_API_KEY", "MASUKKAN_API_KEY_GROQ_DI_SINI")


GROQ_API_KEY = _get_groq_api_key()

if GROQ_API_KEY == "MASUKKAN_API_KEY_GROQ_DI_SINI" or not GROQ_API_KEY:
    if st is not None:
        st.error(
            "GROQ_API_KEY tidak ditemukan. Pastikan sudah diisi di "
            "App settings → Secrets dengan format:\n\nGROQ_API_KEY = \"gsk_xxxx\""
        )

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