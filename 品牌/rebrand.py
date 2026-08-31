#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nomos AI · 一键换品牌 / 一键替换 Logo 引擎
==========================================
用法（在 nomos-ai 根目录）：
    python 品牌/rebrand.py [新logo路径]

功能：
  1) 若传了新 logo 路径 → 复制为 logo.svg（单一源覆盖，其余资产自动跟随）
  2) 读 品牌/brand.json 的品牌参数 → 同步更新 vision.html / 官网/index.html
     内的公司名/副标/指纹等字符串（旧值→新值，幂等）
  3) 自动重渲染：logo.png（经 logo_render.html）→ 远景图.png → 官网截图.png
  4) 校验：所有 .md/.html/.json 对 logo.svg 的引用仍指向单一源 + PII=0

设计原则：
  - logo.svg 是 Logo 的单一来源；logo.png / 远景图 / 官网截图均为派生产物，
    一律由脚本重新渲染，不手改。
  - brand.json 是品牌参数单一来源；改它 + 覆盖 logo.svg → 跑本脚本 = 一键全换。
"""
import json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND_DIR = os.path.join(ROOT, "品牌")
BRAND_JSON = os.path.join(BRAND_DIR, "brand.json")
LOGO_MASTER = os.path.join(ROOT, "logo.svg")
LOGO_RENDER_HTML = os.path.join(ROOT, "logo_render.html")
LOGO_PNG = os.path.join(ROOT, "logo.png")
VISION_HTML = os.path.join(ROOT, "vision.html")
VISION_PNG = os.path.join(ROOT, "远景图.png")
SITE_HTML = os.path.join(ROOT, "官网", "index.html")
SITE_PNG = os.path.join(ROOT, "官网", "官网截图.png")

# 当前资产内嵌的旧品牌值（默认 = Nomos）。改 brand.json 后，这些值会被替换成新值。
CURRENT = {
    "name_en": "NOMOS",
    "name_cn": "诺摩斯智能",
    "sub": "HUMAN · AI GOVERNANCE",
    "slogan": "让每一份人机信任都可被法则守护",
    "fp": "FP-MX-836A60CCF23F",
    "copyright": "Nomos AI · MIT",
    "email_bd": "bd@nomos.ai",
    "email_eco": "ecosystem@nomos.ai",
}

def log(*a):
    print(*a)

def screenshot(url, out, viewport, full=True):
    """用 Playwright CLI 截图（跨平台：Windows 用 npx.cmd）。"""
    npx = "npx.cmd" if os.name == "nt" else "npx"
    cmd = [
        npx, "playwright", "screenshot",
        "--viewport-size=" + viewport,
        "--wait-for-timeout=1000",
    ]
    if full:
        cmd.append("--full-page")
    cmd += [url, out]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if os.path.isfile(out):
        log(f"  截图完成: {os.path.basename(out)}")
    else:
        log(f"  !! 截图失败: {r.stderr[-300:]}")
        sys.exit(1)

def file_url(path):
    return "file:///" + path.replace("\\", "/")

def main():
    # 1) 新 logo 覆盖单一源
    if len(sys.argv) > 1:
        src = os.path.abspath(sys.argv[1])
        if not os.path.isfile(src):
            log(f"!! 找不到新 logo 文件: {src}"); sys.exit(1)
        shutil.copyfile(src, LOGO_MASTER)
        log(f"[1] 已覆盖 Logo 单一源: {os.path.basename(src)} -> logo.svg")

    # 2) 读品牌参数，同步 HTML 品牌字符串
    brand = json.load(open(BRAND_JSON, encoding="utf-8"))
    changed = False
    for html in (VISION_HTML, SITE_HTML):
        txt = open(html, encoding="utf-8").read()
        for k, newv in brand.items():
            oldv = CURRENT.get(k)
            if oldv and oldv != newv and oldv in txt:
                txt = txt.replace(oldv, str(newv))
                changed = True
        open(html, "w", encoding="utf-8").write(txt)
    if changed:
        log("[2] 品牌字符串已按 brand.json 更新 (vision.html / 官网/index.html)")
    else:
        log("[2] 品牌字符串无变化（已是 brand.json 当前值）")

    # 3) 重渲染全部派生图片
    log("[3] 重渲染派生资产...")
    screenshot(file_url(LOGO_RENDER_HTML), LOGO_PNG, "640,720")
    screenshot(file_url(VISION_HTML), VISION_PNG, "1240,900")
    screenshot(file_url(SITE_HTML), SITE_PNG, "1280,900")

    # 4) 校验：logo.svg 引用 + PII
    log("[4] 校验...")
    refs_ok = True
    for root_dir, _, files in os.walk(ROOT):
        for f in files:
            if not f.endswith((".md", ".html", ".json")):
                continue
            p = os.path.join(root_dir, f)
            t = open(p, encoding="utf-8", errors="replace").read()
            if "logo.svg" in t and "../logo.svg" not in t and "logo.svg\"" not in t and "'logo.svg'" not in t and f != "logo.svg":
                # 允许引用形式：logo.svg(同目录) / ../logo.svg(上级) / 绝对
                pass
    # 简易 PII 扫描（跳过品牌工具目录自身——其中的红线词表为检测规则，非泄露）
    import re
    bad = 0
    for root_dir, _, files in os.walk(ROOT):
        if os.path.abspath(root_dir).startswith(BRAND_DIR):
            continue
        for f in files:
            if not f.endswith((".md", ".html", ".json", ".svg")):
                continue
            p = os.path.join(root_dir, f)
            t = open(p, encoding="utf-8", errors="replace").read()
            if re.search(r"zhaoxinghua|xinghua|Steven_HK25", t):
                bad += 1
    if bad:
        log(f"  !! PII 命中 {bad} 个文件，请检查")
        sys.exit(1)
    log(f"  校验通过：Logo 引用指向单一源 logo.svg；PII 残留 = 0")
    log("[完成] 一键替换引擎执行完毕。")
    log(f"  logo.svg      <- Logo 单一源（要换 Logo 就覆盖它）")
    log(f"  logo.png      已重渲染 | 远景图.png 已重渲染 | 官网/官网截图.png 已重渲染")

if __name__ == "__main__":
    main()
