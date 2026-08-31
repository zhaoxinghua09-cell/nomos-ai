# Nomos AI · OpenAPI 插件占位（HTTP / REST）

> 指纹 **FP-MX-B625B4F5BD10** ｜ 2026-08-28 ｜ 品牌占位 · 待开发
> 让每一份人机信任都可被法则守护

## 定位

Nomos AI **治理 API**（OpenAPI 3.0 规范）占位。目标：
- 各 AI 平台插件（Coze / 百宝箱 / 元器 / 文心 / 飞书等）可直接 import OpenAPI spec 生成 HTTP 插件
- 企业侧可把 Nomos AI 治理能力接入自有系统

## 规划端点（占位）

| Method | Path | 功能 | 支柱 |
|---|---|---|---|
| POST | `/v1/audit/evidence-chain` | 生成六类证据工件模板 | XCGS |
| POST | `/v1/a3/assess` | A³ 四维评分卡评估 | A³ |
| GET | `/v1/passport/{id}` | 查询身份码与溯源 | AI 护照 |
| GET | `/v1/compliance/checklist` | EU AI Act 52a / GB/Z 185 清单 | XCGS |
| POST | `/v1/gov/scan` | 治理/PII/版权/指纹扫描 | AI 护照 |

## openapi.yaml（骨架）

```yaml
openapi: 3.0.3
info:
  title: Nomos AI Governance API
  version: 1.0.0
  description: 人与 AI 治理 API（占位）。指纹 FP-MX-B625B4F5BD10
  license:
    name: MIT
    identifier: MIT
servers:
  - url: https://api.nomos.ai/v1
paths:
  /audit/evidence-chain:
    post:
      summary: 生成 ISO 42001/NIST 证据工件模板
      operationId: auditEvidenceChain
      responses:
        '200':
          description: OK
  /a3/assess:
    post:
      summary: A³ 法则四维评分卡评估
      operationId: a3Assess
      responses:
        '200':
          description: OK
  /passport/{id}:
    get:
      summary: 查询智能体身份码与溯源
      operationId: passportLookup
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
  /compliance/checklist:
    get:
      summary: 合规清单（EU AI Act 52a / GB/Z 185）
      operationId: complianceChecklist
      responses:
        '200':
          description: OK
  /gov/scan:
    post:
      summary: 治理/PII/版权/指纹扫描
      operationId: govScan
      responses:
        '200':
          description: OK
```

## 当前状态

- 🅿️ **占位中**：OpenAPI spec 骨架已定义，真实服务待品牌定版后部署
- 发布前：实现后端 + 部署 api.nomos.ai + 各平台插件注册

## 治理与溯源

本插件占位承载 Nomos AI 人与 AI 治理体系（理念承自 MedXpert「注册老炮」体系）。
> 版权 Nomos AI · MIT ｜ 时间戳 2026-08-28 ｜ 指纹 **FP-MX-B625B4F5BD10**
