# Nomos AI · Coze 插件占位（扣子 Plugin）

> 指纹 **FP-MX-FE8DB3780BBB** ｜ 2026-08-28 ｜ 品牌占位 · 待开发
> 让每一份人机信任都可被法则守护

## 定位

Coze（扣子）**插件（Plugin）** 占位——区别于 Bot。
Bot 是完整助手；Plugin 是可供其他 Bot 调用的能力单元。
目标：把 Nomos AI 治理能力（审计 / A³ / 护照 / 合规）封装为 Coze 插件，任何 Coze Bot 可挂载。

## 规划插件工具（占位）

| 工具 | 类型 | 功能 |
|---|---|---|
| `nomos_audit_evidence` | 插件 | 生成 ISO 42001/NIST 证据工件模板 |
| `nomos_a3_assess` | 插件 | A³ 四维评分卡评估 |
| `nomos_passport_query` | 插件 | 智能体身份码/溯源查询 |
| `nomos_compliance_list` | 插件 | 合规清单（EU AI Act 52a / GB/Z 185）|

## 插件元信息（占位）

```json
{
  "name": "nomos_ai_governance",
  "display_name": "Nomos AI 治理工具",
  "version": "1.0.0",
  "fingerprint": "FP-MX-FE8DB3780BBB",
  "description": "Nomos AI 人与 AI 治理插件：审计证据链 / A³ 评估 / 护照查询 / 合规清单",
  "tools": [
    "nomos_audit_evidence",
    "nomos_a3_assess",
    "nomos_passport_query",
    "nomos_compliance_list"
  ],
  "status": "placeholder"
}
```

## 与 Coze Bot 上架包的关系

| 类型 | 状态 | 位置 |
|---|---|---|
| Coze **Bot** 上架包 | ✅ 已就绪（67 个） | `huawei-ecosystem/publish-ready/Coze/` |
| Coze **Plugin** 占位 | 🅿️ 本包 | `插件占位/Coze-Plugin/` |

## 当前状态

- 🅿️ **占位中**：插件定义已备，待品牌定版后开发实现 + 挂载测试
- 发布前：实现插件逻辑 + Coze 开发者后台注册 + 安全测试

## 治理与溯源

本插件占位承载 Nomos AI 人与 AI 治理体系（理念承自 MedXpert「注册老炮」体系）。
> 版权 Nomos AI · MIT ｜ 时间戳 2026-08-28 ｜ 指纹 **FP-MX-FE8DB3780BBB**
