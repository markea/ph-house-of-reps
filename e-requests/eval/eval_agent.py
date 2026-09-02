import os
import json
import time
from typing import Dict, Any, List
from app.agent.triage_agent import triage_agent

def run_evaluation_suite(dataset_path: str = None) -> Dict[str, Any]:
    if not dataset_path:
        dataset_path = os.path.join(os.path.dirname(__file__), "eval_dataset.json")

    with open(dataset_path, "r") as f:
        test_cases = json.load(f)

    total_tests = len(test_cases)
    passed_intent = 0
    total_entities_expected = 0
    matched_entities = 0
    latencies = []
    results = []

    for tc in test_cases:
        prompt = tc["prompt"]
        expected_svc = tc["expected_service"]
        expected_entities = tc.get("expected_entities", {})

        # Run triage
        res = triage_agent.triage_request(prompt)
        actual_svc = res["suggested_service_code"]
        actual_entities = res["extracted_fields"]
        latencies.append(res["latency_ms"])

        # Intent evaluation
        intent_match = (actual_svc == expected_svc)
        if intent_match:
            passed_intent += 1

        # Entity evaluation
        tc_entity_total = len(expected_entities)
        tc_entity_matched = 0
        for k, v in expected_entities.items():
            total_entities_expected += 1
            if k in actual_entities:
                if isinstance(v, str) and v.lower() in str(actual_entities[k]).lower():
                    matched_entities += 1
                    tc_entity_matched += 1
                elif actual_entities[k] == v:
                    matched_entities += 1
                    tc_entity_matched += 1

        results.append({
            "id": tc["id"],
            "category": tc["category"],
            "prompt": prompt,
            "expected_service": expected_svc,
            "actual_service": actual_svc,
            "intent_match": intent_match,
            "confidence": res["confidence_score"],
            "latency_ms": res["latency_ms"],
            "entity_score": f"{tc_entity_matched}/{tc_entity_total}" if tc_entity_total > 0 else "N/A",
            "passed": intent_match and (tc_entity_matched == tc_entity_total if tc_entity_total > 0 else True)
        })

    intent_accuracy = round((passed_intent / total_tests) * 100, 2)
    entity_recall = round((matched_entities / total_entities_expected) * 100, 2) if total_entities_expected > 0 else 100.0
    avg_latency = round(sum(latencies) / len(latencies), 2)

    summary = {
        "agent_name": triage_agent.agent_name,
        "agent_version": triage_agent.version,
        "total_test_cases": total_tests,
        "intent_accuracy_percent": intent_accuracy,
        "entity_recall_percent": entity_recall,
        "average_latency_ms": avg_latency,
        "overall_grade": "A+ (Excellent)" if intent_accuracy >= 95 and entity_recall >= 90 else "B (Good)",
        "results": results
    }

    return summary

def print_terminal_report(summary: Dict[str, Any]):
    print("\n" + "="*80)
    print(f" 🎯 HRep ADK Service Triage Agent - Quality Evaluation Benchmark Report")
    print("="*80)
    print(f" Agent: {summary['agent_name']} (Version: {summary['agent_version']})")
    print(f" Total Test Cases Evaluated: {summary['total_test_cases']}")
    print(f" Intent Classification Accuracy: {summary['intent_accuracy_percent']}%")
    print(f" Entity Extraction Recall:       {summary['entity_recall_percent']}%")
    print(f" Average Latency:                {summary['average_latency_ms']} ms")
    print(f" Overall Quality Grade:          {summary['overall_grade']}")
    print("-"*80)
    print(f"{'ID':<8} {'Category':<20} {'Expected':<16} {'Actual':<16} {'Score':<8} {'Status':<6}")
    print("-"*80)
    for r in summary["results"]:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"{r['id']:<8} {r['category'][:18]:<20} {r['expected_service']:<16} {r['actual_service']:<16} {r['entity_score']:<8} {status}")
    print("="*80 + "\n")

if __name__ == "__main__":
    report = run_evaluation_suite()
    print_terminal_report(report)
