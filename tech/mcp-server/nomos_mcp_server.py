#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SynomosAI · MCP Server（stdio）— 人与 AI 治理工具集
====================================================
5 个工具：
  audit_evidence_chain  生成 ISO 42001/NIST 六类证据工件模板
  a3_assess             A³ 法则四维评分卡（意图/影响/可逆性/监督）
  passport_lookup       查询技能/智能体身份码与溯源（本地台账）
  compliance_checklist  EU AI Act 52a / GB/Z 185 合规清单
  gov_scan              治理/PII/版权/指纹扫描（对文本做规则扫描）

本地运行（stdio）：
  python nomos_mcp_server.py
  或配置到 agent 宿主：mcpServers -> nomos-governance -> command=python, args=[本文件]

指纹 FP-MX-6999EE1111DE ｜ 版权 SynomosAI · MIT ｜ 2026-08-28
"""
import json
import re
import sys
from datetime import datetime, timezone

VERSION = "1.0.0"
FINGERPRINT = "FP-MX-6999EE1111DE"
TOOLS = [
    {
        "name": "audit_evidence_chain",
        "description": "生成 ISO/IEC 42001 + NIST AI RMF 可审计证据工件模板（六类：决策日志/风险登记册/模型卡/变更记录/人类监督证明/事件处置台账）",
        "inputSchema": {"type": "object", "properties": {"system_name": {"type": "string", "description": "AI 系统/智能体名称"}}},
    },
    {
        "name": "a3_assess",
        "description": "A³ 法则四维评分卡评估（意图/影响/可逆性/监督），返回总分与放行建议",
        "inputSchema": {"type": "object", "properties": {
            "intent": {"type": "integer", "minimum": 1, "maximum": 5},
            "impact": {"type": "integer", "minimum": 1, "maximum": 5},
            "reversibility": {"type": "integer", "minimum": 1, "maximum": 5},
            "oversight": {"type": "integer", "minimum": 1, "maximum": 5},
        }},
    },
    {
        "name": "passport_lookup",
        "description": "查询技能/智能体身份码与溯源（本地台账）",
        "inputSchema": {"type": "object", "properties": {"skill": {"type": "string"}}},
    },
    {
        "name": "compliance_checklist",
        "description": "EU AI Act Art 52a / GB/Z 185 合规清单（面向自主 agent 注册就绪）",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "gov_scan",
        "description": "对文本做治理/PII/版权/指纹扫描（命中即告警）",
        "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}},
    },
]

# 本地身份码台账（示例：nomos-ai-brand + 两个治理技能）
PASSPORT_LEDGER = {
    "nomos-ai-brand": {"fp": "FP-MX-2B16BF9C85F4", "version": "1.0.0", "owner": "SynomosAI"},
    "ai-governance-audit-chain": {"fp": "FP-MX-4386B5FB95AB", "version": "1.0.0", "owner": "SynomosAI"},
    "a3-law-operational": {"fp": "FP-MX-B8B8C32E5E6F", "version": "1.0.0", "owner": "SynomosAI"},
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def tool_audit_evidence_chain(args):
    name = args.get("system_name", "AI 系统")
    items = [
        ("决策日志", f"{name} 每次高影响决策的时间/输入/输出/理由"),
        ("风险登记册", f"{name} 识别的风险清单 + 等级 + 缓解措施"),
        ("模型卡", f"{name} 使用的模型/版本/训练数据/局限"),
        ("变更记录", f"{name} 每次变更的版本/时间/影响/审批"),
        ("人类监督证明", f"{name} 关键动作的人类审批记录"),
        ("事件处置台账", f"{name} 异常/事件的处理时间线 + 处置结果"),
    ]
    return {
        "system": name,
        "standard": "ISO/IEC 42001 + NIST AI RMF",
        "artifacts": [{"type": t, "template": d} for t, d in items],
        "note": "六类证据工件模板已生成，可按此采集证据形成可审计证据链。",
    }


def tool_a3_assess(args):
    intent = int(args.get("intent", 3))
    impact = int(args.get("impact", 3))
    reversibility = int(args.get("reversibility", 3))
    oversight = int(args.get("oversight", 3))
    total = intent + impact + reversibility + oversight  # 满分 20
    # 四维评分卡：分数越高越安全/越受控
    if total >= 16:
        verdict = "放行（低风险）"
    elif total >= 12:
        verdict = "有条件放行（需人工复核）"
    else:
        verdict = "拒绝 / 升级评审（A³ 三关不过）"
    return {
        "scores": {"intent": intent, "impact": impact, "reversibility": reversibility, "oversight": oversight},
        "total": total,
        "max": 20,
        "verdict": verdict,
        "rule": "A³ 法则：AI 造/改 AI 或高影响自主动作须过三关（触发阈值→事前评估→事后复盘）",
    }


def tool_passport_lookup(args):
    skill = args.get("skill", "")
    entry = PASSPORT_LEDGER.get(skill)
    if entry:
        return {"found": True, "skill": skill, **entry}
    return {"found": False, "skill": skill, "message": "台账中未找到，可用 nomos-ai-brand 示例测试"}


def tool_compliance_checklist(_args):
    return {
        "checklist": [
            {"item": "agent 唯一身份码（GB/Z 185）", "status": "待确认"},
            {"item": "agent 注册表登记（EU AI Act Art 52a）", "status": "待确认"},
            {"item": "可审计证据链（ISO 42001）", "status": "待确认"},
            {"item": "A³ 触发阈值 + 评估记录", "status": "待确认"},
            {"item": "人类监督机制", "status": "待确认"},
            {"item": "数据合规（PIPL/GDPR，若涉个保）", "status": "待确认"},
        ],
        "window": "EU AI Act Art 52a 自主 agent 强制注册期 Q3 2026",
        "message": "对照清单逐项补齐后即可形成注册就绪包。",
    }


def tool_gov_scan(args):
    text = args.get("text", "")
    findings = []
    pats = {
        "真名": r"zhaoxinghua|xinghua|Steven_HK25",
        "手机": r"(?<![0-9.])1[3-9][0-9]{9}(?![0-9])",
        "本地路径": r"C:\\Users|C:/Users|/c/Users",
        "邮箱": r"[\w.+-]+@(qq|foxmail|163|gmail|outlook)[\w.-]*\.[\w.]+",
        "指纹缺失": None,
    }
    for label, pat in pats.items():
        if pat and re.search(pat, text):
            findings.append({"type": label, "severity": "high", "hit": True})
    if "FP-MX-" not in text:
        findings.append({"type": "指纹缺失", "severity": "medium", "hit": True})
    return {
        "findings": findings,
        "clean": len(findings) == 0,
        "verdict": "通过" if len(findings) == 0 else "驳回（存在风险命中）",
    }


TOOL_HANDLERS = {
    "audit_evidence_chain": tool_audit_evidence_chain,
    "a3_assess": tool_a3_assess,
    "passport_lookup": tool_passport_lookup,
    "compliance_checklist": tool_compliance_checklist,
    "gov_scan": tool_gov_scan,
}


def handle_initialize(req):
    return {
        "jsonrpc": "2.0",
        "id": req.get("id"),
        "result": {
            "protocolVersion": "2025-03-26",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "synomosai-governance-mcp", "version": VERSION},
        },
    }


def handle_tools_list(req):
    return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"tools": TOOLS}}


def handle_tools_call(req):
    params = req.get("params", {})
    name = params.get("name", "")
    args = params.get("arguments", {})
    if name not in TOOL_HANDLERS:
        return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32602, "message": f"unknown tool: {name}"}}
    try:
        result = TOOL_HANDLERS[name](args)
        return {"jsonrpc": "2.0", "id": req.get("id"), "result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32603, "message": str(e)}}


def main():
    # stdio transport：逐行读取 JSON-RPC，响应写 stdout
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = req.get("method")
        if method == "initialize":
            resp = handle_initialize(req)
        elif method == "tools/list":
            resp = handle_tools_list(req)
        elif method == "tools/call":
            resp = handle_tools_call(req)
        elif method == "notifications/initialized":
            continue
        else:
            resp = {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32601, "message": f"method not found: {method}"}}
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
