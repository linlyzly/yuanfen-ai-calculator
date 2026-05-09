#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情侣正缘姻缘测算 - Python 极简后端
2026 抖音爆火 H5 网站专用

【使用方法】
1. 安装依赖: pip install flask flask-cors requests
2. 运行服务: python backend.py
3. 访问地址: http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import random
import hashlib
from datetime import datetime

# ==================== 配置区域 ====================

# 【API Key 密钥粘贴位置】
API_KEY = "9a88f1cb029c42b8884d8021c75397ab.W2pezDaUtUcN1Mv3"

# 【AI 接口地址填写位置】
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 服务配置
HOST = "0.0.0.0"
PORT = 5000

# ==================== Flask 应用 ====================

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# ==================== 星座数据 ====================

ZODIAC_TRAITS = {
    "白羊座": {"element": "火", "trait": "热情奔放、积极进取、勇往直前", "ruling_planet": "火星"},
    "金牛座": {"element": "土", "trait": "稳重踏实、忠诚可靠、追求稳定", "ruling_planet": "金星"},
    "双子座": {"element": "风", "trait": "聪明机智、善于交际、好奇心强", "ruling_planet": "水星"},
    "巨蟹座": {"element": "水", "trait": "温柔细腻、家庭导向、敏感念旧", "ruling_planet": "月亮"},
    "狮子座": {"element": "火", "trait": "自信大方、领导力强、慷慨热情", "ruling_planet": "太阳"},
    "处女座": {"element": "土", "trait": "追求完美、细致周到、分析力强", "ruling_planet": "水星"},
    "天秤座": {"element": "风", "trait": "优雅和谐、追求平衡、社交能力强", "ruling_planet": "金星"},
    "天蝎座": {"element": "水", "trait": "深沉专一、直觉敏锐、意志力强", "ruling_planet": "冥王星"},
    "射手座": {"element": "火", "trait": "乐观开朗、热爱自由、冒险精神", "ruling_planet": "木星"},
    "摩羯座": {"element": "土", "trait": "务实上进、责任心强、耐心持久", "ruling_planet": "土星"},
    "水瓶座": {"element": "风", "trait": "独立创新、博爱友善、理性客观", "ruling_planet": "天王星"},
    "双鱼座": {"element": "水", "trait": "浪漫梦幻、同理心强、艺术气质", "ruling_planet": "海王星"}
}

ZODIAC_COMPATIBILITY = {
    "白羊座": ["狮子座", "射手座", "双子座", "水瓶座"],
    "金牛座": ["处女座", "摩羯座", "巨蟹座", "双鱼座"],
    "双子座": ["天秤座", "水瓶座", "白羊座", "狮子座"],
    "巨蟹座": ["双鱼座", "天蝎座", "金牛座", "处女座"],
    "狮子座": ["白羊座", "射手座", "双子座", "天秤座"],
    "处女座": ["金牛座", "摩羯座", "巨蟹座", "天蝎座"],
    "天秤座": ["双子座", "水瓶座", "狮子座", "射手座"],
    "天蝎座": ["巨蟹座", "双鱼座", "处女座", "摩羯座"],
    "射手座": ["白羊座", "狮子座", "天秤座", "水瓶座"],
    "摩羯座": ["金牛座", "处女座", "天蝎座", "双鱼座"],
    "水瓶座": ["双子座", "天秤座", "白羊座", "射手座"],
    "双鱼座": ["巨蟹座", "天蝎座", "金牛座", "摩羯座"]
}

ELEMENTS = {
    "火": {"strong": ["白羊座", "狮子座", "射手座"], "harmony": "风"},
    "土": {"strong": ["金牛座", "处女座", "摩羯座"], "harmony": "水"},
    "风": {"strong": ["双子座", "天秤座", "水瓶座"], "harmony": "火"},
    "水": {"strong": ["巨蟹座", "天蝎座", "双鱼座"], "harmony": "土"}
}

# ==================== 工具函数 ====================

def calculate_bazi(birthday_str):
    """根据生日计算基本八字信息（简化版）"""
    try:
        birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
        year = birthday.year
        month = birthday.month
        day = birthday.day
        
        # 简化天干地支计算
        heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        year_stem = heavenly_stems[(year - 4) % 10]
        year_branch = earthly_branches[(year - 4) % 12]
        
        # 生肖
        zodiac_animals = ["猴", "鸡", "狗", "猪", "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊"]
        zodiac_animal = zodiac_animals[(year - 4) % 12]
        
        return {
            "year_stem": year_stem,
            "year_branch": year_branch,
            "zodiac_animal": zodiac_animal,
            "year_ganzhi": f"{year_stem}{year_branch}"
        }
    except:
        return {"year_stem": "未知", "year_branch": "未知", "zodiac_animal": "未知", "year_ganzhi": "未知"}

def get_zodiac_from_date(birthday_str):
    """根据生日计算星座"""
    try:
        birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
        month = birthday.month
        day = birthday.day
        
        zodiac_dates = [
            (1, 20, "摩羯座"), (2, 19, "水瓶座"), (3, 21, "双鱼座"),
            (4, 20, "白羊座"), (5, 21, "金牛座"), (6, 22, "双子座"),
            (7, 23, "巨蟹座"), (8, 23, "狮子座"), (9, 23, "处女座"),
            (10, 24, "天秤座"), (11, 22, "天蝎座"), (12, 22, "射手座"),
            (12, 31, "摩羯座")
        ]
        
        for i in range(len(zodiac_dates) - 1):
            if (month < zodiac_dates[i][0]) or \
               (month == zodiac_dates[i][0] and day < zodiac_dates[i][1]):
                return zodiac_dates[i-1][2]
        return zodiac_dates[-1][2]
    except:
        return "未知"

def generate_couple_id():
    """生成唯一的缘分ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = random.randint(100, 999)
    return f"YUAN{timestamp[-6:]}{random_suffix}"

# ==================== AI 接口调用 ====================

def call_ai_api(messages, max_tokens=800):
    """
    调用智谱AI的 glm-4-flash 模型
    
    参数:
        messages: 消息列表
        max_tokens: 最大返回token数
    
    返回:
        AI生成的文本内容
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "glm-4-flash",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.8,
        "top_p": 0.95
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "API返回格式异常"
    except requests.exceptions.Timeout:
        return "请求超时，请重试"
    except requests.exceptions.RequestException as e:
        return f"请求失败: {str(e)}"
    except Exception as e:
        return f"发生错误: {str(e)}"

# ==================== 姻缘分析生成 ====================

def generate_name_analysis(name1, name2):
    """生成姓名灵魂配对分析"""
    prompt = f"""你是一位资深的姓名学大师，请为"{name1}"和"{name2}"这对情侣进行深度的姓名灵魂配对分析。

请从以下角度分析：
1. 两人姓名的笔画数与五行属性
2. 姓名中的偏旁部首所蕴含的性格暗示
3. 两人名字的音韵配合度
4. 姓名组合所蕴含的缘分密码
5. 对这段感情发展的预示

要求：
- 语言要充满宿命感和神秘感
- 内容要细腻走心
- 200-300字左右
- 使用富有诗意的表达方式
- 强调这是命中注定的缘分"""
    
    messages = [
        {"role": "system", "content": "你是一位精通中国传统文化、姓名学和命理学的资深大师，说话富有诗意和神秘感。"},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages, 500)

def generate_zodiac_analysis(zodiac1, zodiac2, name1, name2):
    """生成星座合盘分析"""
    trait1 = ZODIAC_TRAITS.get(zodiac1, {})
    trait2 = ZODIAC_TRAITS.get(zodiac2, {})
    
    compatibility_score = 0
    compatible_list = ZODIAC_COMPATIBILITY.get(zodiac1, [])
    if zodiac2 in compatible_list:
        compatibility_score += 30
    
    # 元素相生相助
    elem1 = trait1.get("element", "")
    elem2 = trait2.get("element", "")
    if (elem1 in ["火", "风"] and elem2 in ["火", "风"]) or \
       (elem1 in ["土", "水"] and elem2 in ["土", "水"]):
        compatibility_score += 25
    elif elem1 == ELEMENTS.get(elem2, {}).get("harmony"):
        compatibility_score += 20
    
    # 基础分数
    base_score = 40 + random.randint(0, 10)
    total_score = min(base_score + compatibility_score, 99)
    
    prompt = f"""请为{name1}（{zodiac1}）和{name2}（{zodiac2}）进行深度星座合盘分析。

已知信息：
- {zodiac1}：{trait1.get('trait', '独特魅力')}，属于{ trait1.get('element', '') }元素
- {zodiac2}：{trait2.get('trait', '独特魅力')}，属于{ trait2.get('element', '') }元素

请分析：
1. 太阳星座的契合程度
2. 性格特点的互补或相似之处
3. 在感情相处中的优势和挑战
4. 最佳的相处模式建议
5. 这段星座配对在12星座中的稀有程度

要求：
- 充满浪漫和神秘感
- 精准描述两个星座的性格碰撞
- 200-300字
- 让用户感受到这是独特的缘分"""
    
    messages = [
        {"role": "system", "content": "你是一位精通西方占星术的资深星座分析师，擅长解读星座之间的化学反应和灵魂共鸣。"},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages, 500)

def generate_bazi_analysis(birthday1, birthday2, name1, name2):
    """生成八字五行合婚分析"""
    bazi1 = calculate_bazi(birthday1)
    bazi2 = calculate_bazi(birthday2)
    
    prompt = f"""请为{name1}（生日：{birthday1}，八字：{bazi1.get('year_ganzhi')}年）和{name2}（生日：{birthday2}，八字：{bazi2.get('year_ganzhi')}年）进行专业的八字五行合婚分析。

请从以下方面解读：
1. 两人年柱、月柱的相生相合关系
2. 日柱天干地支的配对分析
3. 五行（金木水火土）的互补情况
4. 生肖属相的三合六合关系
5. 对婚姻运势的影响

要求：
- 使用传统命理学的专业术语但要通俗解释
- 充满祥瑞和祝福之意
- 200-300字
- 强调这是天作之合"""
    
    messages = [
        {"role": "system", "content": "你是一位精通中国传统文化、八字命理和五行学的资深命理大师。"},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages, 500)

def generate_past_life_analysis(name1, name2):
    """生成前世今生因果分析"""
    prompt = f"""请用充满灵性和神秘感的方式，解读{name1}和{name2}的前世今生因果羁绊。

请描述：
1. 你们可能在哪一世相遇（可以选择古代、近代等不同时代背景）
2. 那段前世关系中你们扮演什么角色
3. 未完成的因果约定是什么
4. 今生相遇是为了完成什么使命
5. 你们灵魂层面最深的羁绊是什么

要求：
- 充满浪漫主义和神秘色彩
- 富有画面感和故事性
- 200-300字
- 让人感到心灵的触动
- 可以融入中国神话或佛教、道教的轮回概念"""
    
    messages = [
        {"role": "system", "content": "你是一位通灵师和灵魂摆渡人，擅长前世回溯和灵魂解读。"},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages, 600)

def generate_love_forecast(name1, name2, know_duration):
    """生成感情运势预测"""
    prompt = f"""请为{name1}和{name2}预测他们感情的未来运势。

背景：他们目前的关系状态是「{know_duration}」

请预测：
1. 2026年的感情运势走向
2. 2027年的感情发展趋势
3. 2028年可能的重要转折点
4. 未来五年感情的总体走向
5. 适合他们的感情升温方式

要求：
- 充满希望和正能量
- 分年份详细阐述
- 200-300字
- 让人对这段感情充满信心"""
    
    messages = [
        {"role": "system", "content": "你是一位命运预言家，擅长解读感情的未来走向。"},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages, 500)

def generate_warning_advice(name1, name2, zodiac1, zodiac2):
    """生成矛盾预警和建议"""
    prompt = f"""请为{name1}（{zodiac1}）和{name2}（{zodiac2}）提供感情相处指南。

请指出：
1. 可能出现的沟通障碍或矛盾点
2. 两个星座在相处中容易产生的摩擦
3. 如何避免这些问题的建议
4. 维持感情长久的关键
5. 给双方的专属相处建议

要求：
- 善意的提醒而非负面的预言
- 实用且接地气的建议
- 150-200字
- 充满关心和祝福"""
    
    messages = [
        {"role": "system", "content": "你是一位情感咨询师和心灵导师，擅长调和情侣关系。"},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages, 400)

def generate_marriage_year(name1, name2):
    """生成最佳结婚年份"""
    prompt = f"""请为{name1}和{name2}分析最佳的结婚年份。

请根据命理学和感情发展规律：
1. 推荐最适合领证/举办婚礼的年份
2. 次推荐的备选年份
3. 分析原因（流年运势、八字合盘等）
4. 最佳月份和季节建议
5. 旺姻缘的风水或方位建议

要求：
- 充满祥瑞和祝福
- 200字左右
- 具体年份要有依据"""
    
    messages = [
        {"role": "system", "content": "你是一位精通婚姻嫁娶的资深命理师。"},
        {"role": "user", "content": prompt}
    ]
    
    return call_ai_api(messages, 400)

def calculate_compatibility(name1, name2, zodiac1, zodiac2):
    """计算综合契合度"""
    score = 50  # 基础分数
    
    # 星座匹配加成
    compatible = ZODIAC_COMPATIBILITY.get(zodiac1, [])
    if zodiac2 in compatible:
        score += 20
    
    # 元素加成
    trait1 = ZODIAC_TRAITS.get(zodiac1, {})
    trait2 = ZODIAC_TRAITS.get(zodiac2, {})
    elem1 = trait1.get("element", "")
    elem2 = trait2.get("element", "")
    
    if elem1 == elem2:
        score += 15
    elif elem1 == ELEMENTS.get(elem2, {}).get("harmony"):
        score += 10
    
    # 名字笔画加成
    name_score = (len(name1) + len(name2)) % 10
    score += name_score
    
    # 随机微调
    score += random.randint(-5, 5)
    
    return min(max(score, 60), 99)

# ==================== API 路由 ====================

@app.route("/")
def index():
    """首页"""
    return jsonify({
        "status": "ok",
        "message": "情侣正缘姻缘测算 API 服务运行中",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/analyze": "提交测算数据，获取完整分析结果"
        }
    })

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """主测算接口"""
    try:
        data = request.get_json()
        
        # 获取表单数据
        name1 = data.get("name1", "")
        name2 = data.get("name2", "")
        gender1 = data.get("gender1", "male")
        gender2 = data.get("gender2", "female")
        birthday1 = data.get("birthday1", "")
        birthday2 = data.get("birthday2", "")
        zodiac1 = data.get("zodiac1", get_zodiac_from_date(birthday1) if birthday1 else "")
        zodiac2 = data.get("zodiac2", get_zodiac_from_date(birthday2) if birthday2 else "")
        know_duration = data.get("knowDuration", "朋友")
        
        # 计算契合度
        compatibility = calculate_compatibility(name1, name2, zodiac1, zodiac2)
        personality = max(60, compatibility - random.randint(3, 8))
        communication = max(60, compatibility - random.randint(5, 12))
        
        # 生成缘分ID
        couple_id = generate_couple_id()
        
        # 依次调用AI生成各项分析
        print(f"正在为 {name1} 和 {name2} 生成分析...")
        
        name_analysis = generate_name_analysis(name1, name2)
        zodiac_analysis = generate_zodiac_analysis(zodiac1, zodiac2, name1, name2)
        bazi_analysis = generate_bazi_analysis(birthday1, birthday2, name1, name2)
        past_life = generate_past_life_analysis(name1, name2)
        love_forecast = generate_love_forecast(name1, name2, know_duration)
        warning_advice = generate_warning_advice(name1, name2, zodiac1, zodiac2)
        marriage_year = generate_marriage_year(name1, name2)
        
        # 组合结果
        result = {
            "status": "success",
            "couple_id": couple_id,
            "compatibility": compatibility,
            "personality": personality,
            "communication": communication,
            "name_analysis": name_analysis,
            "zodiac_analysis": zodiac_analysis,
            "bazi_analysis": bazi_analysis,
            "past_life_analysis": past_life,
            "love_forecast": love_forecast,
            "warning_advice": warning_advice,
            "best_marriage_year": marriage_year,
            "meta": {
                "name1": name1,
                "name2": name2,
                "zodiac1": zodiac1,
                "zodiac2": zodiac2,
                "know_duration": know_duration,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        print(f"分析完成，缘分ID: {couple_id}")
        return jsonify(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/api/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "healthy"})

# ==================== 启动服务 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("💕 情侣正缘姻缘测算后端服务")
    print("=" * 50)
    print(f"服务地址: http://{HOST}:{PORT}")
    print(f"API接口: http://{HOST}:{PORT}/api/analyze")
    print("=" * 50)
    print("\n按 Ctrl+C 停止服务\n")
    
    app.run(host=HOST, port=PORT, debug=False, threaded=True)
