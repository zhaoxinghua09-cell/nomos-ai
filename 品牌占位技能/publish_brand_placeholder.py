#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nomos AI · 三平台品牌占位发布脚本（凭证到位后执行）
=====================================================
用法：
  python publish_brand_placeholder.py --platform clawhub --token clh_xxx
  python publish_brand_placeholder.py --platform skillhub --token <key>
  python publish_brand_placeholder.py --platform skillpie --token <key>
  python publish_brand_placeholder.py --all --clawhub clh_xxx --skillhub <key> --skillpie <key>

品牌占位技能：nomos-ai-brand（指纹 FP-MX-2B16BF9C85F4）
发布纪律：发布前须用户确认（发什么/发到哪/版本）；发布后回填台账。
"""
import argparse, json, os, sys, subprocess, urllib.request, urllib.parse

SKILL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nomos-ai-brand")
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")

PAYLOAD = {
    "slug": "nomos-ai-brand",
    "displayName": "Nomos AI · 诺摩斯智能（品牌占位）",
    "version": "1.0.0",
    "changelog": "品牌占位首发：远景/四支柱/服务/即将上线技能清单",
    "tags": ["ai-governance", "brand", "nomos", "governance"],
    "acceptLicenseTerms": True,
}

def read_skill_md():
    with open(SKILL_MD, encoding="utf-8") as f:
        return f.read()

def publish_clawhub(token):
    """ClawHub multipart API：字段名必须是 payload（踩坑点）。"""
    try:
        import requests
    except ImportError:
        print("!! 需要 requests：pip install requests")
        return False
    # 构造 multipart：payload JSON + 技能文件
    data = {k: v for k, v in PAYLOAD.items()}
    # 用 json 序列化的 payload 字段
    multipart = {
        "payload": (None, json.dumps(data, ensure_ascii=False)),
        "skill": (os.path.basename(SKILL_MD), read_skill_md(), "text/markdown"),
    }
    # 上传 SKILL.md 内容（实际平台可能要求 zip 或直接文件；此处先按文件传）
    headers = {"Authorization": f"Bearer {token}"}
    # 端点以 clawhub.ai 官方文档为准（占位，待 token 后实测）
    url = "https://clawhub.ai/api/v1/skills"
    print(f"[ClawHub] 发布 {PAYLOAD['slug']} v{PAYLOAD['version']} ...")
    r = requests.post(url, headers=headers, files=multipart, timeout=60)
    print(f"   HTTP {r.status_code}: {r.text[:300]}")
    return r.status_code in (200, 201)

def publish_skillhub(token):
    """SkillHub：优先 skillhub CLI（已登录态），否则尝试 API。"""
    # 方式1：CLI（需要 skillhub login 已做过浏览器 OAuth）
    try:
        r = subprocess.run(["skillhub", "init", "--name", PAYLOAD["slug"], "--category", "AI治理"],
                           capture_output=True, text=True, timeout=30)
        print("[SkillHub] init:", r.stdout.strip()[:200] or r.stderr.strip()[:200])
    except FileNotFoundError:
        print("[SkillHub] 未安装 skillhub CLI（npm i -g skillhub-cli）。改用 API Key 模式（待平台 API 文档确认）。")
    print("[SkillHub] 发布占位：请确保已 skillhub login（微信 OAuth + 实名认证）。")
    print("[SkillHub] 待 API 端点确认后自动 push/publish；当前由用户网页/CLI 完成更稳。")
    return False

def publish_skillpie(token):
    print("[SkillPie] API 端点待确认；当前建议网页登录后上传 nomos-ai-brand.zip。")
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", choices=["clawhub", "skillhub", "skillpie"])
    ap.add_argument("--token")
    ap.add_argument("--clawhub"); ap.add_argument("--skillhub"); ap.add_argument("--skillpie")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    if not (a.platform or a.all):
        print("用法见脚本头。必须 --platform 或 --all。")
        return

    if a.all:
        ok = True
        if a.clawhub: ok &= publish_clawhub(a.clawhub)
        else: print("--all 需提供 --clawhub token")
        if a.skillhub: ok &= publish_skillhub(a.skillhub)
        else: print("--all 需提供 --skillhub key")
        if a.skillpie: ok &= publish_skillpie(a.skillpie)
        else: print("--all 需提供 --skillpie key")
        print("品牌占位三平台发布完成" if ok else "部分平台待补凭证/API")
    elif a.platform == "clawhub":
        publish_clawhub(a.token)
    elif a.platform == "skillhub":
        publish_skillhub(a.token)
    elif a.platform == "skillpie":
        publish_skillpie(a.token)

if __name__ == "__main__":
    main()
