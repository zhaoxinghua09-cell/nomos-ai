#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nomos AI · 全库一键改名引擎（品牌占位 ⇄ skill 发布 同步兜底）
===============================================================
用法（任意目录）：
    python D:/Workbuddy/.../nomos-ai/品牌/rebrand_all.py --dry-run   # 只看会改哪些（安全）
    python D:/Workbuddy/.../nomos-ai/品牌/rebrand_all.py --apply     # 实际执行

覆盖两个库：
  A. nomos-ai 品牌资产（logo/远景图/官网 HTML）—— 品牌字符串同步
  B. huawei-ecosystem 发布产物（67 技能 SKILL.md 治理段 / Coze 包 / staging /
     台账 / 占位页 / 全景图）—— 品牌声明模板替换

核心安全原则：
  - 只替换「品牌声明模板」（版权行 / 治理段承载品牌 / frontmatter author /
    Coze 品牌行 / 台账品牌）→ 不碰技能名 medxpert-* 与正文业务描述
  - 品牌参数单一来源 = 品牌/brand.json；改它再跑本脚本 = 一键全库改名
  - dry-run 默认，先看影响面再 apply
"""
import json, os, re, sys, glob

BRAND_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand.json")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # nomos-ai/
ECO = os.path.join(os.path.dirname(ROOT), "huawei-ecosystem")               # 发布产物库

def log(*a): print(*a)

# 当前资产内嵌的旧品牌值（默认 = MedXpert 系 / 与 brand.json 对照）
CURRENT = {
    "name_en": "NOMOS",
    "name_cn": "诺摩斯智能",
    "copyright": "Nomos AI · MIT",
    "fp_prefix": "FP-MX-",
    "medxpert_entity": "MedXpert 美达信医疗科技（香港）有限公司 · 注册老炮",
    "medxpert_brand": "MedXpert",
    "medxpert_author": "注册老炮@MedXpert",
    "gov_medxpert": "MedXpert「注册老炮」AI 治理体系",
    "gov_medxpert2": "MedXpert 人与 AI 治理体系",
    "coze_copy": "版权：MedXpert·MIT",
    "coze_copy2": "版权 MedXpert·MIT",
}

def build_mapping(brand):
    """brand.json 新参数 → 精确替换映射（长串优先，避免误伤技能名/正文）。"""
    en = brand.get("name_en", "NOMOS")
    cn = brand.get("name_cn", "诺摩斯智能")
    cop = brand.get("copyright", "Nomos AI · MIT")
    fp = brand.get("fp_prefix", "FP-MX-")
    entity_new = f"{en} · {cn}" if cn else en
    return [
        # 版权主体长串（最高优先级）
        (re.compile(r"版权 © \d{4} MedXpert 美达信医疗科技（香港）有限公司 · 注册老炮 \(MIT 许可\)"),
         f"版权 © 2026 {entity_new} (MIT 许可)"),
        (re.compile(r"版权[：:] MedXpert[·\s]?MIT"), f"版权：{cop}"),
        (re.compile(r"版权[：:] MedXpert·MIT"), f"版权：{cop}"),
        # 治理段承载品牌（来源可保留，品牌主体换成新）
        (re.compile(r"承载 MedXpert「注册老炮」AI 治理体系"), f"承载 {en} 人与 AI 治理体系（理念承自 MedXpert「注册老炮」体系）"),
        (re.compile(r"承载 MedXpert 人与 AI 治理体系"), f"承载 {en} 人与 AI 治理体系（理念承自 MedXpert 体系）"),
        (re.compile(r"本技能承载 MedXpert"), f"本技能承载 {en}"),
        (re.compile(r"本 Bot 承载 MedXpert"), f"本 Bot 承载 {en}"),
        # frontmatter author
        (re.compile(r"author: 注册老炮@MedXpert"), f"author: {en}"),
        (re.compile(r"作者[:：]\s*注册老炮@MedXpert"), f"作者：{en}"),
        # 指纹前缀（可选；默认保留 FP-MX-）
    ] + ([(re.compile(r"FP-MX-(?=[A-F0-9]{12})"), fp)] if fp != CURRENT["fp_prefix"] else [])

def iter_text_files(root):
    exts = (".md", ".txt", ".html", ".json", ".yaml", ".yml", ".py", ".sh", ".css")
    for dirpath, _, files in os.walk(root):
        if "node_modules" in dirpath or ".git" in dirpath:
            continue
        for f in files:
            if f.endswith(exts) and f not in ("rebrand.py", "rebrand_all.py"):
                yield os.path.join(dirpath, f)

def apply_to_root(root, mappings, dry):
    changed_files = 0
    total_hits = 0
    for p in iter_text_files(root):
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        orig = t
        hits = 0
        for pat, rep in mappings:
            if pat.search(t):
                t2, n = pat.subn(rep, t)
                hits += n
                t = t2
        if hits:
            if not dry:
                open(p, "w", encoding="utf-8").write(t)
            changed_files += 1
            total_hits += hits
            rel = os.path.relpath(p, root)
            log(f"   {rel}  (+{hits})")
    return changed_files, total_hits

def main():
    dry = "--dry-run" in sys.argv or len(sys.argv) == 1
    apply = "--apply" in sys.argv
    brand = json.load(open(BRAND_JSON, encoding="utf-8"))
    mappings = build_mapping(brand)
    if not mappings:
        log("!! 无映射：brand.json 与当前品牌一致，无需改名")
        return
    mode = "DRY-RUN（预览）" if dry else "APPLY（执行）"
    log(f"=== 全库一键改名：{mode} ===")
    log(f"品牌目标: {brand.get('name_en')} · {brand.get('name_cn')} ｜ 版权 {brand.get('copyright')}")

    log(f"\n[A] nomos-ai 品牌资产:")
    cf, ch = apply_to_root(ROOT, mappings, dry)
    log(f"    → {cf} 个文件 / {ch} 处命中")

    if os.path.isdir(ECO):
        log(f"\n[B] huawei-ecosystem 发布产物:")
        cf2, ch2 = apply_to_root(ECO, mappings, dry)
        log(f"    → {cf2} 个文件 / {ch2} 处命中")
    else:
        log(f"\n[B] 未找到发布产物库 {ECO}，跳过")

    log(f"\n{'预览完成（无改动）。确认后加 --apply 执行' if dry else '执行完成。'}")
    if apply and not dry:
        log("→ 校验提示：执行后建议重跑 PII 扫描（真名/手机/路径=0）与指纹唯一性核验")

if __name__ == "__main__":
    main()
