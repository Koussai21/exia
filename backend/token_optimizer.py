from typing import List, Dict
import anthropic


class TokenOptimizer:
    EXTRACTION_MAX = 3000
    REFORMULATION_MAX = 800
    REFORMULATION_MIN = 400
    BATCH_SIZE = 10

    # Token pricing (May 2024, can be updated)
    PRICING = {
        "claude-opus-4-1-20250805": {"input": 0.003, "output": 0.012},
        "claude-sonnet-4-20250514": {"input": 0.003, "output": 0.015},
        "claude-haiku-4-5-20251001": {"input": 0.00025, "output": 0.00125},
    }

    @staticmethod
    def count_tokens(text: str) -> int:
        client = anthropic.Anthropic()
        try:
            response = client.messages.count_tokens(
                model="claude-opus-4-1-20250805",
                messages=[{"role": "user", "content": text}]
            )
            return response.input_tokens
        except Exception:
            return len(text) // 4

    @staticmethod
    def calculate_complexity(requirement: dict) -> int:
        score = 1
        content = requirement.get("contenu", "")

        if len(content) > 500:
            score += 1
        if "?" in content:
            score += 1
        if not any(word in content.lower() for word in ["doit", "will", "shall", "métriques", "critères"]):
            score += 1

        return min(score, 5)

    @staticmethod
    def allocate_reformulation_tokens(requirements: List[dict], total_budget: int) -> Dict[str, int]:
        total_complexity = sum(req.get("complexity_score", 1) for req in requirements)

        allocations = {}
        for req in requirements:
            complexity = req.get("complexity_score", 1)
            proportion = complexity / total_complexity if total_complexity > 0 else 1 / len(requirements)
            allocated = int(proportion * total_budget)
            allocated = max(
                TokenOptimizer.REFORMULATION_MIN,
                min(allocated, TokenOptimizer.REFORMULATION_MAX)
            )
            allocations[req["id"]] = allocated

        return allocations

    @staticmethod
    def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        pricing = TokenOptimizer.PRICING.get(model, {"input": 0.003, "output": 0.015})
        return (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000

    @staticmethod
    def format_cost_estimate(model: str, input_tokens: int, output_tokens: int) -> dict:
        cost = TokenOptimizer.estimate_cost(model, input_tokens, output_tokens)
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_usd": round(cost, 4),
            "model": model
        }
