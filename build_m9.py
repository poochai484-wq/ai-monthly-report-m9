#!/usr/bin/env python3
"""
生成9月份AI月报HTML
基于8月份模板，更新内容和图片
"""

import base64
import os
import re
from pathlib import Path

# 路径配置
BASE_DIR = Path("/Users/aaa/Desktop/客服系统/AI工作/AI月报")
M8_HTML = BASE_DIR / "2026-M8" / "客服中心AI月报-M8.html"
M9_DIR = BASE_DIR / "2026-M9"
M9_IMAGES = M9_DIR  # M9图片直接在2026-M9目录下
OUTPUT_HTML = M9_DIR / "客服中心AI月报-M9.html"

# 9月份物料内容
M9_CONTENT = {
    "title": "客服中心AI月报 · 2026年9月",
    "stats": {
        "launched": 6,      # 已上线项目数
        "in_progress": 3,   # 进行中项目数
        "ai_ratio": "77%"   # AI服务占比
    },
    "launched_projects": [
        {
            "name": "智能客服前端交互改版：全量上线",
            "tag": "全量发布 · 前端交互",
            "desc": "为用户提供更智能、更流畅的在线客服体验",
            "image": "智能客服改版案例图.jpeg"
        },
        {
            "name": "坐席助手 - 多轮对话探寻",
            "tag": "智能引导 · 多轮对话",
            "desc": "当用户未回答询问时，助手会自动生成新一轮探寻话术，帮助客服快速完成二次引导，提升问题解决效率",
            "image": "坐席助手-多轮对话探寻 .png"
        },
        {
            "name": "坐席助手 - 大模型图片理解",
            "tag": "图片识别 · 智能理解",
            "desc": "通过大模型实现图片理解能力，助手可直接识别用户发送的图片内容，通话更流畅、服务更高效",
            "image": "坐席助手-大模型图片理解.png"
        },
        {
            "name": "抖音爱奇艺小程序-用户反馈自动化处理",
            "tag": "自动化 · 工单处理",
            "desc": "系统自动调取抖音反馈查询接口，查询反馈数据后AI自动创建工单并回复，大幅提升反馈处理效率",
            "image": "抖音爱奇艺小程序.png"
        },
        {
            "name": "猜你想问推送逻辑优化",
            "tag": "策略升级 · 精准匹配",
            "desc": "①热门问题逻辑重构：按入口维度取最近一小时Top10，不足则取前一天Top10<br>②检索逻辑优化：根据用户设备或浏览记录等探索类猜你想问优化匹配逻辑，准确率提升约27%"
        },
        {
            "name": "高频客诉skill对话流畅度优化",
            "tag": "技能优化 · 差异化答复",
            "desc": "针对退费skill和修改手机号skill进行对话流畅度优化，针对用户重复要求退费的诉求，给予差异化答复",
            "image": "高频客诉skill对话流畅度优化.png"
        }
    ],
    "ongoing_projects": [
        {
            "name": "智能客服质量闭环",
            "tag": "自动化迭代 · 质量提升",
            "desc": "搭建 \"评估-定位-归因-修复-验证-上线\" 自动化迭代链路，按月迭代，目前已完成基础评分体系，待实现自动化归因及迭代等完整飞轮",
            "image": "智能客服质量闭环.png"
        },
        {
            "name": "\"猜你想问\"效果闭环",
            "tag": "效果追踪 · 持续优化",
            "desc": "建立猜你想问效果闭环体系，追踪点击率、解决率等核心指标，持续优化推送策略和内容质量",
            "image": "猜你想问效果闭环.png"
        }
    ],
    "tech_exploration": {
        "name": "Jev（TypeSafe AI）",
        "tag": "System One模型 · 类型化决策",
        "desc": "Jev是TypeSafe AI推出的决策型API，由前OpenAI研究员Diogo Almeida（GPT-4、ChatGPT、RLHF核心合著者）创立。与传统文本生成模型不同，Jev属于「System One模型」——专为软件设计的结构化判断引擎，输出类型化的概率评分而非自由文本。<br><br>在客服场景中，Jev正好能切入几个关键环节：<br><br><b>意图分类/路由：</b>传统做法靠LLM写Prompt判断，慢且贵；Jev直接输出类别概率，亚秒级完成。<br><b>工单分级：</b>传统规则引擎维护成本高；Jev输出结构化决策，置信度可信可追溯。<br><b>兜底判断：</b>以往阈值靠拍脑袋；Jev给出校准过的概率，可直接定阈值做自动化。<br><b>满意度预测：</b>传统离线模型延迟高；Jev支持在线实时评分。<br><br>一句话总结：用代码管规则，用Jev管判断，用LLM管生成——把「判断」这件事从文本生成里拆出来，交给专门的模型做。"
    }
}

def image_to_base64(image_path: Path) -> str:
    """将图片转换为base64编码"""
    if not image_path.exists():
        print(f"警告: 图片不存在 {image_path}")
        return ""

    with open(image_path, "rb") as f:
        image_data = f.read()

    # 根据文件扩展名确定MIME类型
    suffix = image_path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif"
    }
    mime_type = mime_types.get(suffix, "image/png")

    base64_data = base64.b64encode(image_data).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"

def get_image_display_width(image_name: str) -> int:
    """根据图片原始尺寸，计算合适的显示宽度"""
    # 默认宽度
    return 580

def build_single_project_card(project: dict) -> str:
    """构建单个项目卡片（上下结构：文字在上，图片在下）"""
    image_html = ""
    if "image" in project and project["image"]:
        image_path = M9_IMAGES / project["image"]
        base64_src = image_to_base64(image_path)
        if base64_src:
            display_width = get_image_display_width(project["image"])
            image_html = f'''
        <tr><td style="padding-top:14px;">
            <img src="{base64_src}" alt="{project['name']}" width="{display_width}" style="display:block; max-width:{display_width}px; width:100%; height:auto; border:1px solid #e8e8e8;" />
        </td></tr>'''

    return f'''
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:20px;">
    <tr><td bgcolor="#f8f9fa" style="background-color:#f8f9fa; padding:20px; border:1px solid #e8e8e8;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr><td style="font-family:Arial, sans-serif; font-size:15px; font-weight:bold; color:#1a1a2e; padding-bottom:2px;">{project['name']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:11px; color:#999999; padding-bottom:12px;">{project['tag']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:13px; color:#666666; line-height:1.8; padding-bottom:14px;">{project['desc']}</td></tr>
        {image_html}
        </table>
    </td></tr>
    </table>'''

def build_project_html(project: dict, index: int, is_launched: bool = True) -> str:
    """构建单个项目的HTML"""
    return build_single_project_card(project)

def build_m9_html() -> str:
    """构建完整的9月份HTML"""
    # 读取8月份模板
    with open(M8_HTML, "r", encoding="utf-8") as f:
        template = f.read()

    # 更新标题和月份
    html = template.replace("客服中心AI月报 · 2026年8月", M9_CONTENT["title"])
    html = html.replace("2026年8月", "2026年9月")

    # 缩窄整体宽度，适配Outlook
    html = html.replace('width="750"', 'width="600"')
    html = html.replace('width="580"', 'width="460"')

    # 修复Outlook居中问题：去掉外层100%宽度，让灰色底框跟随内容宽度
    html = html.replace(
        '<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f0f2f5">\n<tr><td align="center" style="padding:4px 2px;">',
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" bgcolor="#f0f2f5" style="margin:0 auto;">\n<tr><td align="center" style="padding:4px 2px;">'
    )
    # Outlook居中兼容：body加text-align:center
    html = html.replace(
        'background-color:#f0f2f5;',
        'background-color:#f0f2f5; text-align:center;'
    )

    # 更新关键成果数据
    html = re.sub(
        r'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#00c853; line-height:1;">\d+</td>',
        f'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#00c853; line-height:1;">{M9_CONTENT["stats"]["launched"]}</td>',
        html, count=1
    )
    html = re.sub(
        r'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#ff9800; line-height:1;">\d+</td>',
        f'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#ff9800; line-height:1;">{M9_CONTENT["stats"]["in_progress"]}</td>',
        html, count=1
    )
    html = re.sub(
        r'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#2196f3; line-height:1;">\d+%</td>',
        f'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#2196f3; line-height:1;">{M9_CONTENT["stats"]["ai_ratio"]}</td>',
        html, count=1
    )

    # 构建已上线项目HTML
    launched_html = ""
    for i, project in enumerate(M9_CONTENT["launched_projects"]):
        launched_html += build_project_html(project, i, is_launched=True)

    # 构建持续推进项目HTML
    ongoing_html = ""
    for i, project in enumerate(M9_CONTENT["ongoing_projects"]):
        ongoing_html += build_project_html(project, i, is_launched=False)

    # 替换已上线项目内容
    launched_section_start = html.find('<!-- ===== LAUNCHED PROJECTS ===== -->')
    launched_section_end = html.find('<!-- ===== ONGOING PROJECTS ===== -->')

    if launched_section_start != -1 and launched_section_end != -1:
        title_table_start = html.find('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">', launched_section_start + len('<!-- ===== LAUNCHED PROJECTS ===== -->'))
        if title_table_start != -1:
            title_table_end = html.find('</table>', title_table_start) + len('</table>')
            section_header = html[launched_section_start:title_table_end]
            new_launched_section = section_header + '\n\n' + launched_html + '\n    </td></tr>\n</table>\n'
            html = html[:launched_section_start] + new_launched_section + html[launched_section_end:]

    # 替换持续推进项目内容
    ongoing_section_start = html.find('<!-- ===== ONGOING PROJECTS ===== -->')
    ongoing_section_end = html.find('<!-- ===== TECH EXPLORATION ===== -->')

    if ongoing_section_start != -1 and ongoing_section_end != -1:
        title_table_start = html.find('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">', ongoing_section_start + len('<!-- ===== ONGOING PROJECTS ===== -->'))
        if title_table_start != -1:
            title_table_end = html.find('</table>', title_table_start) + len('</table>')
            section_header = html[ongoing_section_start:title_table_end]
            new_ongoing_section = section_header + '\n\n' + ongoing_html + '\n    </td></tr>\n</table>\n'
            html = html[:ongoing_section_start] + new_ongoing_section + html[ongoing_section_end:]

    # 更新技术探索部分
    tech_section_start = html.find('<!-- ===== TECH EXPLORATION ===== -->')
    tech_section_end = html.find('<!-- ===== FOOTER ===== -->')

    if tech_section_start != -1 and tech_section_end != -1:
        title_table_start = html.find('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">', tech_section_start + len('<!-- ===== TECH EXPLORATION ===== -->'))
        if title_table_start != -1:
            title_table_end = html.find('</table>', title_table_start) + len('</table>')
            section_header = html[tech_section_start:title_table_end]

            # 技术探索无图片
            tech = M9_CONTENT["tech_exploration"]
            tech_card = f'''
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:20px;">
    <tr><td bgcolor="#e3f2fd" style="background-color:#e3f2fd; padding:20px; border:1px solid #90caf9;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr><td style="font-family:Arial, sans-serif; font-size:15px; font-weight:bold; color:#1565c0; padding-bottom:2px;">{tech['name']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:11px; color:#64b5f6; padding-bottom:12px;">{tech['tag']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:13px; color:#666666; line-height:1.8; padding-bottom:14px;">{tech['desc']}</td></tr>
        </table>
    </td></tr>
    </table>'''

            new_tech_section = section_header + '\n\n' + tech_card + '\n    </td></tr>\n</table>\n'
            html = html[:tech_section_start] + new_tech_section + html[tech_section_end:]

    return html

def main():
    """主函数"""
    print("开始生成9月份AI月报...")

    # 检查模板文件是否存在
    if not M8_HTML.exists():
        print(f"错误: 找不到8月份模板文件 {M8_HTML}")
        return

    # 生成HTML
    html = build_m9_html()

    # 保存文件
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 9月份AI月报已生成: {OUTPUT_HTML}")
    print(f"📊 关键成果: {M9_CONTENT['stats']['launched']}项已上线, {M9_CONTENT['stats']['in_progress']}项进行中, AI服务占比{M9_CONTENT['stats']['ai_ratio']}")

if __name__ == "__main__":
    main()
