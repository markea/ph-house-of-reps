from fastapi import APIRouter
from app.schemas import AgentTriageRequest, AgentTriageResponse
from app.agent.triage_agent import triage_agent
from eval.eval_agent import run_evaluation_suite

router = APIRouter(prefix="/api/agent", tags=["AI Triage Agent"])

@router.post("/triage", response_model=AgentTriageResponse)
def triage_issue(payload: AgentTriageRequest):
    result = triage_agent.triage_request(payload.user_prompt)
    return AgentTriageResponse(
        suggested_service_code=result["suggested_service_code"],
        suggested_service_name=result["suggested_service_name"],
        extracted_fields=result["extracted_fields"],
        confidence_score=result["confidence_score"],
        reasoning=result["reasoning"],
        next_question=result["next_question"]
    )

@router.get("/eval")
def get_evaluation_metrics():
    """Runs the ADK agent quality evaluation benchmark suite and returns live statistical metrics."""
    return run_evaluation_suite()
