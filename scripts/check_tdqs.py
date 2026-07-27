"""TDQS (Tool Definition Quality Score) Evaluator for Sophos Firewall MCP Server."""

from typing import Any, Dict
from sophos_firewall_mcp.server import mcp


def evaluate_tdqs() -> None:
    """Evaluate Tool Definition Quality Score (TDQS) across all registered tools."""
    tm = mcp._tool_manager  # type: ignore[attr-defined]
    tools: Dict[str, Any] = tm._tools  # type: ignore[attr-defined]

    total_tools = len(tools)
    tools_with_annotations = 0
    tools_with_100pct_param_descs = 0
    tools_with_usage_guidelines = 0

    print("================ TDQS EVALUATION REPORT ================")
    print(f"Total Registered Tools: {total_tools}\n")

    for name, tool in tools.items():
        if name in ("route_tools", "call_routed_tool"):
            # Exclude meta/router control tools from quality audit
            total_tools -= 1
            continue

        has_annotations = tool.annotations is not None
        if has_annotations:
            tools_with_annotations += 1

        doc = tool.description or ""
        has_usage = (
            "use when" in doc.lower()
            or "retrieves" in doc.lower()
            or "list" in doc.lower()
            or "create" in doc.lower()
            or "delete" in doc.lower()
            or "enable" in doc.lower()
            or "retrieve" in doc.lower()
        )
        if has_usage:
            tools_with_usage_guidelines += 1

        params = tool.parameters or {}
        props = params.get("properties", {})
        param_count = len([p for p in props if p not in ("ctx", "client")])
        described_count = 0

        for pname, pinfo in props.items():
            if pname in ("ctx", "client"):
                continue
            if pinfo.get("description"):
                described_count += 1

        is_100pct_params = (param_count == 0) or (described_count == param_count)
        if is_100pct_params:
            tools_with_100pct_param_descs += 1

        status_anno = "✓" if has_annotations else "✗"
        status_param = "✓" if is_100pct_params else "✗"
        status_usage = "✓" if has_usage else "✗"
        print(f"[{status_anno} Anno | {status_param} Param | {status_usage} Doc] {name}")

    if total_tools == 0:
        print("No domain tools found.")
        return

    pct_anno = (tools_with_annotations / total_tools) * 100
    pct_param = (tools_with_100pct_param_descs / total_tools) * 100
    pct_usage = (tools_with_usage_guidelines / total_tools) * 100

    score = ((pct_anno / 100) * 1.5 + (pct_param / 100) * 2.0 + (pct_usage / 100) * 1.5)

    print("\n---------------- SCORECARD METRICS ----------------")
    print(f"Tools Evaluated              : {total_tools}")
    print(f"Behavioral Annotations      : {tools_with_annotations} / {total_tools} ({pct_anno:.1f}%)")
    print(f"100% Parameter Descriptions : {tools_with_100pct_param_descs} / {total_tools} ({pct_param:.1f}%)")
    print(f"Usage Guidelines (Docstrings): {tools_with_usage_guidelines} / {total_tools} ({pct_usage:.1f}%)")
    print(f"Overall TDQS Score           : {score:.2f} / 5.00")

    tier = "Tier A+" if score >= 4.8 else ("Tier A" if score >= 4.5 else ("Tier B" if score >= 4.0 else "Tier C"))
    print(f"TDQS Quality Tier            : {tier}")
    print("========================================================")


if __name__ == "__main__":
    evaluate_tdqs()
