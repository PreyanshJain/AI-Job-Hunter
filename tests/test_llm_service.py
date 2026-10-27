from app.llm.llm_service import LLMService


def test_llm_service_generate(monkeypatch):
    def fake_chat(*args, **kwargs):
        return {
            "message": {
                "content": '{"match": true, "resume_skill": "llms"}'
            }
        }

    monkeypatch.setattr(
        "app.llm.llm_service.chat",
        fake_chat
    )

    llm_service = LLMService("qwen3:4b")

    response = llm_service.generate("Match LLM with LLMs.")

    assert response == {
        "match": True,
        "resume_skill": "llms"
    }


def test_llm_service_generate_handles_error(monkeypatch):
    def fake_chat(*args, **kwargs):
        raise Exception("Simulated LLM failure")

    monkeypatch.setattr(
        "app.llm.llm_service.chat",
        fake_chat
    )

    llm_service = LLMService("qwen3:4b")
    response = llm_service.generate("Match LLM with LLMs.")
    assert response == {
        "match": False,
        "resume_skill": None
    }