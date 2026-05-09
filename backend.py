#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情侣正缘姻缘测算 - Python 极简后端 v2.0
2026 抖音爆火 H5 网站专用 | 支持塔罗牌占卜

【使用方法】
1. 安装依赖: pip install flask flask-cors requests
2. 运行服务: python backend.py
3. 访问地址: http://localhost:5000

【新增功能 v2.0】
- 塔罗牌占卜 API
- 更严谨的契合度算法
- 缓存机制优化响应速度
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import random
import hashlib
from datetime import datetime
from functools import wraps
import time

# ==================== 配置区域 ====================

# 【API Key 密钥粘贴位置】
API_KEY = "your-api-key-here"

# 【AI 接口地址填写位置】
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 服务配置
HOST = "0.0.0.0"
PORT = 5000

# ==================== Flask 应用 ====================

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# ==================== 缓存机制 ====================

cache = {}
CACHE_DURATION = 300  # 5分钟缓存

def get_cache_key(*args):
    """生成缓存键"""
    return hashlib.md5(str(args).encode()).hexdigest()

def cached(func):
    """简单缓存装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = get_cache_key(func.__name__, *args, **kwargs)
        if key in cache:
            cached_data, timestamp = cache[key]
            if time.time() - timestamp < CACHE_DURATION:
                return cached_data
        result = func(*args, **kwargs)
        cache[key] = (result, time.time())
        return result
    return wrapper

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

# ==================== 塔罗牌数据 ====================

MAJOR_ARCANA = [
    {"name": "愚人", "icon": "0", "meaning": "新的开始、自由、纯真", "advice": "勇敢迈出第一步，相信直觉"},
    {"name": "魔术师", "icon": "I", "meaning": "创造力、技能、沟通", "advice": "发挥你的才能，善用资源"},
    {"name": "女祭司", "icon": "II", "meaning": "直觉、神秘、内在智慧", "advice": "倾听内心的声音"},
    {"name": "女皇", "icon": "III", "meaning": "丰盛、孕育、情感", "advice": "珍惜身边的美好"},
    {"name": "皇帝", "icon": "IV", "meaning": "权威、领导、规则", "advice": "建立稳定的秩序"},
    {"name": "教皇", "icon": "V", "meaning": "信仰、传统、精神", "advice": "寻求智慧指引"},
    {"name": "恋人", "icon": "VI", "meaning": "爱情、选择、和谐", "advice": "跟随心的选择"},
    {"name": "战车", "icon": "VII", "meaning": "意志、胜利、决心", "advice": "坚定向前"},
    {"name": "力量", "icon": "VIII", "meaning": "勇气、耐心、内在力量", "advice": "用温柔展现力量"},
    {"name": "隐士", "icon": "IX", "meaning": "内省、孤独、指引", "advice": "在独处中找到答案"},
    {"name": "命运之轮", "icon": "X", "meaning": "命运、转变、循环", "advice": "接受生命的变化"},
    {"name": "正义", "icon": "XI", "meaning": "公正、真相、法律", "advice": "诚实面对一切"},
    {"name": "倒吊人", "icon": "XII", "meaning": "等待、牺牲、换位思考", "advice": "换个角度看世界"},
    {"name": "死神", "icon": "XIII", "meaning": "结束、转变、释放", "advice": "放下过去，迎接新生"},
    {"name": "节制", "icon": "XIV", "meaning": "平衡、调节、中庸", "advice": "找到内心的平衡"},
    {"name": "恶魔", "icon": "XV", "meaning": "束缚、欲望、物质", "advice": "摆脱无形的枷锁"},
    {"name": "塔", "icon": "XVI", "meaning": "突变、觉醒、解放", "advice": "破茧成蝶的阵痛"},
    {"name": "星星", "icon": "XVII", "meaning": "希望、灵感、宁静", "advice": "黑暗中总有光明"},
    {"name": "月亮", "icon": "XVIII", "meaning": "幻觉、恐惧、潜意识", "advice": "穿越迷雾看清真相"},
    {"name": "太阳", "icon": "XIX", "meaning": "快乐、成功、活力", "advice": "拥抱生命的温暖"},
    {"name": "审判", "icon": "XX", "meaning": "重生、复兴、觉醒", "advice": "给自己一个重新开始的机会"},
    {"name": "世界", "icon": "XXI", "meaning": "完成、成就、圆满", "advice": "旅程即将圆满结束"}
]

MINOR_ARCANA = {
    "wands": [
        {"name": "权杖Ace", "meaning": "新的热情、创意火花", "advice": "点燃你的激情"},
        {"name": "权杖二", "meaning": "决定、计划、领导力", "advice": "规划你的方向"},
        {"name": "权杖三", "meaning": "扩张、远见、胸怀", "advice": "展望更广阔的世界"},
        {"name": "权杖四", "meaning": "和谐、庆祝、繁荣", "advice": "享受当下的美好"},
        {"name": "权杖五", "meaning": "竞争、冲突、多样性", "advice": "在差异中成长"},
        {"name": "权杖六", "meaning": "胜利、荣誉、认可", "advice": "庆祝你的成就"},
        {"name": "权杖七", "meaning": "挑战、坚守、勇气", "advice": "捍卫你的立场"},
        {"name": "权杖八", "meaning": "行动、速度、扩张", "advice": "快速推进计划"},
        {"name": "权杖九", "meaning": "防御、困难、坚持", "advice": "坚持就是胜利"},
        {"name": "权杖十", "meaning": "负担、压力、责任", "advice": "学会适当放手"}
    ],
    "cups": [
        {"name": "圣杯Ace", "meaning": "新感情、爱、机会", "advice": "敞开心扉迎接爱"},
        {"name": "圣杯二", "meaning": "关系、吸引、选择", "advice": "珍惜眼前的缘分"},
        {"name": "圣杯三", "meaning": "庆祝、友谊、欢乐", "advice": "与朋友共度时光"},
        {"name": "圣杯四", "meaning": "不满足、幻想、选择", "advice": "看清真正的渴望"},
        {"name": "圣杯五", "meaning": "失落、悲伤、接受", "advice": "失去中有收获"},
        {"name": "圣杯六", "meaning": "回忆、纯真、 nostalgia", "advice": "珍藏美好回忆"},
        {"name": "圣杯七", "meaning": "幻想、选择、迷茫", "advice": "分清现实与幻想"},
        {"name": "圣杯八", "meaning": "离开、追寻、放弃", "advice": "勇敢追寻真正想要的"},
        {"name": "圣杯九", "meaning": "满足、欲望、愿塑", "advice": "感恩所拥有的"},
        {"name": "圣杯十", "meaning": "圆满、家庭、和谐", "advice": "家庭是温暖的港湾"}
    ],
    "swords": [
        {"name": "宝剑Ace", "meaning": "新思想、清晰、真相", "advice": "用智慧斩断困惑"},
        {"name": "宝剑二", "meaning": "僵局、决定、平衡", "advice": "冷静做出选择"},
        {"name": "宝剑三", "meaning": "伤心、痛苦、背叛", "advice": "伤痛终会愈合"},
        {"name": "宝剑四", "meaning": "休息、恢复、沉思", "advice": "给自己喘息空间"},
        {"name": "宝剑五", "meaning": "失败、冲突、失去", "advice": "失败是成功之母"},
        {"name": "宝剑六", "meaning": "离开、过渡、疗愈", "advice": "带着伤痕前行"},
        {"name": "宝剑七", "meaning": "策略、智谋、生存", "advice": "用智慧解决问题"},
        {"name": "宝剑八", "meaning": "限制、困境、囚禁", "advice": "挣脱束缚找出口"},
        {"name": "宝剑九", "meaning": "恐惧、焦虑、噩梦", "advice": "恐惧只是幻象"},
        {"name": "宝剑十", "meaning": "结束、痛苦、失败", "advice": "最坏的已经过去"}
    ],
    "pentacles": [
        {"name": "星币Ace", "meaning": "新财运、物质、开始", "advice": "财富即将到来"},
        {"name": "星币二", "meaning": "平衡、适应、管理", "advice": "学会分配资源"},
        {"name": "星币三", "meaning": "技能、工作、团队", "advice": "团队协作创佳绩"},
        {"name": "星币四", "meaning": "保守、占有、安全", "advice": "学会分享与给予"},
        {"name": "星币五", "meaning": "困难、分离、援助", "advice": "困境中仍有希望"},
        {"name": "星币六", "meaning": "给予、慷慨、富足", "advice": "施比受更有福"},
        {"name": "星币七", "meaning": "等待、耐心、投资", "advice": "耐心等待回报"},
        {"name": "星币八", "meaning": "技能、奉献、精进", "advice": "专注提升自我"},
        {"name": "星币九", "meaning": "独立、繁荣、成就", "advice": "你的努力得到回报"},
        {"name": "星币十", "meaning": "财富、繁荣、传承", "advice": "家族繁荣昌盛"}
    ]
}

ALL_TAROT_CARDS = (
    MAJOR_ARCANA +
    MINOR_ARCANA["wands"] + MINOR_ARCANA["cups"] +
    MINOR_ARCANA["swords"] + MINOR_ARCANA["pentacles"]
)

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

# ==================== 依恋人格测试 API ====================

@app.route("/api/attachment/analyze", methods=["POST"])
def attachment_analyze():
    """依恋人格测试深度分析接口"""
    try:
        data = request.get_json()
        primary_type = data.get("primaryType", "secure")
        secondary_type = data.get("secondaryType")
        scores = data.get("scores", {})
        prompt = data.get("prompt", "")
        
        # 调用AI生成深度分析
        messages = [
            {"role": "system", "content": """你是一位资深的情感心理咨询师，精通依恋理论（Attachment Theory）。
你擅长用温暖专业的方式帮助用户深度理解自己的依恋类型。
你的分析要：
1. 深度剖析依恋成因，结合原生家庭和成长经历
2. 描述典型恋爱表现，帮助用户识别自己的行为模式
3. 指出相处痛点，给出具体可操作的建议
4. 用治愈系语言，像知心姐姐/哥哥一样给予支持
5. 每个维度的分析150-200字，结尾的改善建议200字
6. 适当使用emoji增加亲切感"""},
            {"role": "user", "content": prompt}
        ]
        
        analysis = call_ai_api(messages, 1500)
        
        return jsonify({
            "status": "success",
            "analysis": analysis
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ==================== 情感解忧室聊天 API ====================

@app.route("/api/chat", methods=["POST"])
def chat():
    """情感解忧室聊天接口"""
    try:
        data = request.get_json()
        messages = data.get("messages", [])
        
        if not messages:
            return jsonify({
                "status": "error",
                "message": "消息不能为空"
            }), 400
        
        # 构建系统提示和用户消息
        system_prompt = """你是一位温柔专业、充满同理心的情感咨询师和恋爱军师。你的职责是：
1. 认真倾听用户的情感困惑，不敷衍、不套模板
2. 用温暖治愈的语气回应，让用户感受到被理解
3. 深度分析用户的情感模式和相处问题
4. 给出落地可行的相处建议和解决方案
5. 疏导用户的情绪内耗，帮助理清思路
6. 不评判、不指责，始终保持包容和理解

你的风格：
- 温柔但有力量，像知心姐姐/哥哥一样
- 语言温暖细腻，有画面感
- 分析深入但不学术，接地气
- 建议具体可操作
- 适当用emoji增加亲切感
- 每次回复200-300字，不要太长

重要：你不是在生成标准答案，而是在真正理解和回应用户的情感需求。"""
        
        # 构建API消息格式
        api_messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史消息（限制数量以控制token）
        for msg in messages[-8:]:
            role = "user" if msg.get("role") == "user" else "assistant"
            api_messages.append({
                "role": role,
                "content": msg.get("content", "")
            })
        
        response_text = call_ai_api(api_messages, 600)
        
        return jsonify({
            "status": "success",
            "response": response_text
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ==================== 塔罗牌 API ====================

@app.route("/api/tarot/draw", methods=["POST"])
def tarot_draw():
    """塔罗牌抽选接口"""
    try:
        data = request.get_json() or {}
        num_cards = data.get("num_cards", 3)
        name1 = data.get("name1", "你")
        name2 = data.get("name2", "TA")
        
        # 随机抽取指定数量的牌
        drawn_cards = random.sample(ALL_TAROT_CARDS, min(num_cards, len(ALL_TAROT_CARDS)))
        
        # 生成解读
        positions = ["过去", "现在", "未来"]
        interpretation = generate_tarot_interpretation(drawn_cards, name1, name2)
        
        return jsonify({
            "status": "success",
            "cards": drawn_cards,
            "positions": positions[:len(drawn_cards)],
            "interpretation": interpretation
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def generate_tarot_interpretation(cards, name1, name2):
    """生成塔罗牌解读"""
    if len(cards) < 3:
        return "牌数不足"
    
    past, present, future = cards[0], cards[1], cards[2]
    
    interpretation = f"""📖 {name1}与{name2}的塔罗牌解读

【过去 - {past['name']}】
{past['meaning']}
💡 {past['advice']}

【现在 - {present['name']}】
{present['meaning']}
💡 {present['advice']}

【未来 - {future['name']}】
{future['meaning']}
💡 {future['advice']}

✨ 记住，塔罗牌指引的是可能性，真正的未来掌握在你们自己手中。"""
    
    return interpretation

@app.route("/api/tarot/all", methods=["GET"])
def tarot_all():
    """获取所有塔罗牌"""
    return jsonify({
        "status": "success",
        "total": len(ALL_TAROT_CARDS),
        "major_arcana": MAJOR_ARCANA,
        "minor_arcana": MINOR_ARCANA
    })

@app.route("/api/tarot/shuffle", methods=["GET"])
def tarot_shuffle():
    """获取随机洗牌结果"""
    shuffled = random.sample(ALL_TAROT_CARDS, len(ALL_TAROT_CARDS))
    return jsonify({
        "status": "success",
        "cards": shuffled[:10]  # 返回前10张作为展示
    })

# ==================== 启动服务 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("💕 情侣正缘姻缘测算后端服务 v3.0")
    print("   2026 抖音爆款 H5 网站专用")
    print("=" * 60)
    print(f"🚀 服务地址: http://{HOST}:{PORT}")
    print(f"📊 姻缘测算: http://{HOST}:{PORT}/api/analyze")
    print(f"🃏 塔罗占卜: http://{HOST}:{PORT}/api/tarot/draw")
    print(f"🧠 依恋测试: http://{HOST}:{PORT}/api/attachment/analyze")
    print(f"💬 情感聊天: http://{HOST}:{PORT}/api/chat")
    print(f"❤️  健康检查: http://{HOST}:{PORT}/api/health")
    print("=" * 60)
    print(f"📦 塔罗牌总数: {len(ALL_TAROT_CARDS)} 张")
    print("\n✨ 新增功能 v3.0:")
    print("   • 恋爱依恋人格心理测试 + AI深度解析")
    print("   • 情感解忧室AI聊天对话")
    print("\n按 Ctrl+C 停止服务\n")
    
    app.run(host=HOST, port=PORT, debug=False, threaded=True)
