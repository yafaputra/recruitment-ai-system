import re
from typing import TypedDict, Dict, Any

from llm_utils import call_llm
from rag_utils import retrieve
from data_mining_utils import predict_hiring_decision


class AgentState(TypedDict):
    candidate_id: str
    cv_text: str
    job_description: str
    candidate_data: Dict[str, Any]
    hr_check: Dict[str, Any]
    skill_match: Dict[str, Any]
    finance_check: Dict[str, Any]
    legal_check: Dict[str, Any]
    prediction_result: Dict[str, Any]
    final_recommendation: str


def hr_agent(state: AgentState) -> dict:
    system = (
        "Kamu adalah HR Agent pada sistem rekrutmen. Tugasmu memeriksa apakah CV kandidat "
        "mencantumkan informasi wajib: data kontak, riwayat pendidikan, dan pengalaman kerja. "
        "Jawab dengan format persis:\nSTATUS: Lengkap / Tidak Lengkap\nALASAN: <penjelasan singkat>"
    )
    user = f"CV Kandidat:\n{state['cv_text']}"
    result = call_llm(system, user)
    status = "Lengkap" if "STATUS: Lengkap" in result else "Tidak Lengkap"
    return {"hr_check": {"status": status, "detail": result}}


def skill_matching_agent(state: AgentState) -> dict:
    system = (
        "Kamu adalah Skill Matching Agent. Bandingkan skill dan pengalaman pada CV kandidat "
        "dengan requirement pada Job Description. Beri skor kecocokan 0-100. Jawab dengan format persis:\n"
        "SKOR: <angka 0-100>\nALASAN: <penjelasan singkat>"
    )
    user = f"CV Kandidat:\n{state['cv_text']}\n\nJob Description:\n{state['job_description']}"
    result = call_llm(system, user)
    match = re.search(r"SKOR:\s*(\d+)", result)
    score = int(match.group(1)) if match else None
    return {"skill_match": {"score": score, "detail": result}}


def finance_agent(state: AgentState) -> dict:
    expected_salary = state["candidate_data"]["expected_salary"]
    position_level = state["candidate_data"]["position_level"]

    query = f"Apakah ekspektasi gaji Rp{expected_salary:,} untuk level posisi {position_level} sesuai kebijakan gaji perusahaan?"
    retrieved = retrieve(query, top_k=2)
    context = "\n\n".join(retrieved["documents"][0])

    system = (
        "Kamu adalah Finance Agent. Jawab HANYA berdasarkan konteks Kebijakan HR berikut. "
        "Jawab dengan format persis:\nSTATUS: Sesuai / Tidak Sesuai / Perlu Review\nALASAN: <penjelasan singkat>"
    )
    user = f"Konteks Kebijakan HR:\n{context}\n\nPertanyaan: {query}"
    result = call_llm(system, user)

    sources = [m["source"] for m in retrieved["metadatas"][0]]
    return {"finance_check": {"detail": result, "sources": sources}}


def legal_agent(state: AgentState) -> dict:
    candidate_docs = state["candidate_data"]["legal_documents"]

    query = "Dokumen legal apa saja yang wajib dilengkapi kandidat sebelum penandatanganan kontrak?"
    retrieved = retrieve(query, top_k=2)
    context = "\n\n".join(retrieved["documents"][0])

    system = (
        "Kamu adalah Legal Agent. Berdasarkan konteks SOP/Kebijakan HR berikut, periksa apakah dokumen "
        f"yang sudah dimiliki kandidat ({', '.join(candidate_docs)}) sudah lengkap. Jawab dengan format persis:\n"
        "STATUS: Lengkap / Tidak Lengkap\nDOKUMEN_KURANG: <daftar dokumen yang belum ada, atau '-' jika lengkap>\nALASAN: <penjelasan singkat>"
    )
    user = f"Konteks Dokumen:\n{context}"
    result = call_llm(system, user)

    sources = [m["source"] for m in retrieved["metadatas"][0]]
    return {"legal_check": {"detail": result, "sources": sources}}


def data_mining_agent(state: AgentState) -> dict:
    features = state["candidate_data"]["features"]
    result = predict_hiring_decision(features)
    return {"prediction_result": result}


def coordinator_agent(state: AgentState) -> dict:
    summary = f'''
Ringkasan evaluasi kandidat {state['candidate_id']}:

1. HR Agent — Kelengkapan CV: {state['hr_check']['status']}
2. Skill Matching Agent — Skor kecocokan skill: {state['skill_match']['score']}/100
3. Finance Agent — {state['finance_check']['detail']}
4. Legal Agent — {state['legal_check']['detail']}
5. Data Mining Agent — Prediksi: {state['prediction_result']['label']} (probabilitas {state['prediction_result']['probability']:.2%})
'''
    system = (
        "Kamu adalah Coordinator Agent pada sistem rekrutmen. Berdasarkan ringkasan hasil seluruh agent berikut, "
        "susun rekomendasi akhir dengan format persis:\n"
        "KEPUTUSAN: Lanjut ke Interview / Tidak Lanjut / Perlu Review Manual\n"
        "RINGKASAN: <ringkasan 2-3 kalimat yang mudah dipahami HRD>"
    )
    result = call_llm(system, summary, max_tokens=300)
    return {"final_recommendation": result}
