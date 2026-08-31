# Nomos AI · MCP 插件占位（Model Context Protocol）

> 指纹 **FP-MX-6999EE1111DE** ｜ 2026-08-28 ｜ 品牌占位 · 待开发
> 让每一份人机信任都可被法则守护

## 定位

Nomos AI MCP Server 是一组**人与 AI 治理工具**的 MCP 插件占位。
目标：让任何支持 MCP 的 Agent（Claude / Cursor / Coze / 飞书 / 微信 / WorkBuddy 等）
都能直接调用 Nomos AI 治理能力——审计证据、A³ 评估、护照查询、合规清单。

## 规划中的 MCP Tools（占位）

| Tool | 功能 | 对应支柱 |
|---|---|---|
| `audit_evidence_chain` | 生成 ISO 42001 / NIST 六类证据工件模板 | XCGS 治理系统 |
| `a3_assess` | A³ 法则四维评分卡（意图/影响/可逆性/监督）| A³ 法则 |
| `passport_lookup` | 查询技能/智能体身份码与溯源信息 | AI 护照机制 |
| `compliance_checklist` | EU AI Act 52a / GB/Z 185 合规清单 | XCGS 治理系统 |
| `gov_scan` | 治理声明 / PII / 版权 / 指纹扫描 | AI 护照机制 |

## 当前状态

- ✅ **stdio 已实现并跑通**（2026-08-28）：`tech/mcp-server/nomos_mcp_server.py`，5 工具全部可用（initialize/tools/list/tools/call 已实测）
- 🅿️ 远程（HTTP/Streamable）待阶段 2
- 平台：任何支持 MCP 的 Agent 宿主（~30+）
- 待办：接入各宿主配置（Claude/Cursor/Coze/飞书/WorkBuddy）+ 安全测试 + 上架

## 目录结构（已实现）

```
MCP/
├── README.md            ← 本文件（占位说明）
├── mcp-config.json      ← MCP 配置骨架
└── tools/               ← 已实现于 tech/mcp-server/nomos_mcp_server.py
```

## mcp-config.json（骨架）

```json
{
  "name": "nomos-ai-governance-mcp",
  "version": "1.0.0",
  "fingerprint": "FP-MX-6999EE1111DE",
  "tools": [
    "audit_evidence_chain",
    "a3_assess",
    "passport_lookup",
    "compliance_checklist",
    "gov_scan"
  ],
  "transport": "stdio",
  "status": "placeholder"
}
```

## 治理与溯源

本插件占位承载 Nomos AI 人与 AI 治理体系（理念承自 MedXpert「注册老炮」体系）。
> 版权 Nomos AI · MIT ｜ 时间戳 2026-08-28 ｜ 指纹 **FP-MX-6999EE1111DE**
