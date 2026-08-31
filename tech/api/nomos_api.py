#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SynomosAI · OpenAPI 治理 API（最小版）
======================================
FastAPI 实现 5 个治理端点（本地可跑，部署后为 api.synomosai/v1/*）：
  POST /v1/audit/evidence-chain  生成六类证据工件模板
  POST /v1/a3/assess            A³ 四维评分卡评估
  GET  /v1/passport/{id}        查询智能体身份码/溯源
  GET  /v1/compliance/checklist 合规清单（EU AI Act 52a / GB/Z 185）
  POST /v1/gov/scan             治理/PII/版权/指纹扫描

本地运行：
  uvicorn nomos_api:app --reload --port 8000
  curl http://127.0.0.1:8000/v1/gov/scan ...

指纹 FP-MX-B625B4F5BD10 ｜ 版权 SynomosAI · MIT ｜ 2026-08-28
"""
import re
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="SynomosAI Governance API",
    version="1.0.0",
    description="人与 AI 治理 API（最小版）。指纹 FP-MX-B625B4F5BD10",
    license_info={"name": "MIT", "identifier": "MIT"},
)

FINGERPRINT = "FP-MX-B625B4F5BD10"

PASSPORT_LEDGER = {
    "nomos-ai-brand": {"fp": "FP-MX-2B16BF9C85F4", "version": "1.0.0", "owner": "SynomosAI"},
    "ai-governance-audit-chain": {"fp": "FP-MX-4386B5FB95AB", "version": "1.0.0", "owner": "SynomosAI"},
    "a3-law-operational": {"fp": "FP-MX-B8B8C32E5E6F", "version": "1.0.0", "owner": "SynomosAI"},
}


class EvidenceReq(BaseModel):
    system_name: str = "AI 系统"


class A3Req(BaseModel):
    intent: int = Field(3, ge=1, le=5)
    impact: int = Field(3, ge=1, le=5)
    reversibility: int = Field(3, ge=1, le=5)
    oversight: int = Field(3, ge=1, le=5)


class ScanReq(BaseModel):
    text: str


@app.get("/v1/health")
def health():
    return {"status": "ok", "fingerprint": FINGERPRINT, "ts": datetime.now(timezone.utc).isoformat()}


@app.post("/v1/audit/evidence-chain")
def audit_evidence_chain(req: EvidenceReq):
    items = [
        ("决策日志", f"{req.system_name} 每次高影响决策的时间/输入/输出/理由"),
        ("风险登记册", f"{req.system_name} 风险清单 + 等级 + 缓解"),
        ("模型卡", f"{req.system_name} 模型/版本/数据/局限"),
        ("变更记录", f"{req.system_name} 变更版本/时间/影响/审批"),
        ("人类监督证明", f"{req.system_name} 关键动作人类审批"),
        ("事件处置台账", f"{req.system_name} 异常处理时间线 + 结果"),
    ]
    return {"system": req.system_name, "standard": "ISO/IEC 42001 + NIST AI RMF", "artifacts": [{"type": t, "template": d} for t, d in items]}


@app.post("/v1/a3/assess")
def a3_assess(req: A3Req):
    total = req.intent + req.impact + req.reversibility + req.oversight
    verdict = "放行（低风险）" if total >= 16 else ("有条件放行（需人工复核）" if total >= 12 else "拒绝 / 升级评审")
    return {"scores": {"intent": req.intent, "impact": req.impact, "reversibility": req.reversibility, "oversight": req.oversight}, "total": total, "max": 20, "verdict": verdict}


@app.get("/v1/passport/{skill_id}")
def passport_lookup(skill_id: str):
    entry = PASSPORT_LEDGER.get(skill_id)
    if not entry:
        raise HTTPException(status_code=404, detail="台账未找到该智能体身份码")
    return {"found": True, "skill": skill_id, **entry}


@app.get("/v1/compliance/checklist")
def compliance_checklist():
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
    }


@app.post("/v1/gov/scan")
def gov_scan(req: ScanReq):
    text = req.text
    findings = []
    pats = {
        "真名": r"zhaoxinghua|xinghua|Steven_HK25",
        "手机": r"(?<![0-9.])1[3-9][0-9]{9}(?![0-9])",
        "本地路径": r"C:\\Users|C:/Users|/c/Users",
        "邮箱": r"[\w.+-]+@(qq|foxmail|163|gmail|outlook)[\w.-]*\.[\w.]+",
    }
    for label, pat in pats.items():
        if re.search(pat, text):
            findings.append({"type": label, "severity": "high"})
    if "FP-MX-" not in text:
        findings.append({"type": "指纹缺失", "severity": "medium"})
    return {"findings": findings, "clean": len(findings) == 0, "verdict": "通过" if not findings else "驳回"}
