from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import tempfile
import os
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

from .models import ExtractionResponse, ReformulationResponse, SessionData, ExportRequest, CostEstimate
from .session_manager import SessionManager
from .token_optimizer import TokenOptimizer
from .extraction import doc_parser, extraire_exigences
from .reformulation import reformuler_selection
from .export_service import export_to_word, export_to_excel

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

app = FastAPI(
    title="Cahier des charges IA",
    description="API optimisée pour extraction et reformulation d'exigences",
    version="2.0.0"
)

session_manager = SessionManager(ttl_hours=24)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "API opérationnelle - v2.0"}


@app.post("/extract")
async def extract(fichier: UploadFile = File(...), max_tokens: int = 3000):
    if not fichier.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Le document doit être un fichier .docx")

    contenu = await fichier.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(contenu)
        chemin_tmp = tmp.name

    try:
        texte = doc_parser(chemin_tmp)
        requirements = extraire_exigences(texte, max_tokens=max_tokens)

        session_id = session_manager.create_session(fichier.filename, requirements)
        session = session_manager.get_session(session_id)

        cost = TokenOptimizer.format_cost_estimate(
            "claude-sonnet-4-20250514",
            TokenOptimizer.count_tokens(texte),
            TokenOptimizer.count_tokens(str(requirements))
        )

        return {
            "session_id": session_id,
            "requirements": [r.dict() for r in session.requirements],
            "total_requirements": len(requirements),
            "extraction_cost": cost,
            "timestamp": datetime.now().isoformat()
        }
    finally:
        os.unlink(chemin_tmp)


@app.get("/session/{session_id}")
def get_session(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable ou expirée")

    return {
        "session_id": session.session_id,
        "filename": session.filename,
        "requirements": [r.dict() for r in session.requirements],
        "reformulations": session.reformulations.dict() if session.reformulations else None,
        "created_at": session.created_at.isoformat(),
        "updated_at": session.updated_at.isoformat()
    }


@app.post("/reformulate/{session_id}")
def reformulate(session_id: str, requirement_ids: list = None, batch_size: int = 10, model: str = "claude-haiku-4-5-20251001"):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable ou expirée")

    requirements = [r.dict() for r in session.requirements]
    reformulations, token_usage = reformuler_selection(requirements, requirement_ids, model)

    session_manager.update_reformulations(session_id, reformulations)

    cost = TokenOptimizer.format_cost_estimate(model, token_usage["input_tokens"], token_usage["output_tokens"])

    return {
        "session_id": session_id,
        "reformulations": {k: v.dict() for k, v in reformulations.items()},
        "completed_count": len(reformulations),
        "cost": cost,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/cost-estimate/{session_id}")
def cost_estimate(session_id: str, model: str = "claude-haiku-4-5-20251001"):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable ou expirée")

    remaining = len([r for r in session.requirements if session.reformulations is None or r.id not in session.reformulations])
    estimated_tokens = remaining * 150
    cost = TokenOptimizer.estimate_cost(model, estimated_tokens, estimated_tokens * 2)

    return {
        "remaining_requirements": remaining,
        "estimated_tokens": estimated_tokens,
        "estimated_usd": round(cost, 4),
        "model": model
    }


@app.post("/export/{session_id}")
def export_data(session_id: str, export_request: ExportRequest):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable ou expirée")

    requirements = [r.dict() for r in session.requirements]
    reformulations = {k: v.dict() for k, v in session.reformulations.items()} if session.reformulations else {}
    selections = export_request.selected_requirements or {}

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if export_request.format == "word":
        file_content = export_to_word(session.filename, requirements, selections)
        filename = f"cahier_reformule_{timestamp}.docx"
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif export_request.format == "excel":
        file_content = export_to_excel(session.filename, requirements, reformulations, selections)
        filename = f"exigences_{timestamp}.xlsx"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        raise HTTPException(status_code=400, detail="Format d'export non supporté (word, excel)")

    with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name

    try:
        return FileResponse(tmp_path, media_type=media_type, filename=filename)
    except:
        os.unlink(tmp_path)
        raise


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    if session_manager.delete_session(session_id):
        return {"message": "Session supprimée"}
    raise HTTPException(status_code=404, detail="Session introuvable")


@app.get("/cleanup")
def cleanup_sessions():
    expired_count = session_manager.cleanup_expired()
    return {"expired_sessions_removed": expired_count}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))