# 💕 情侣正缘姻缘缘分测算 H5 网站

> 2026 抖音当下全网爆火风格，纯娱乐合规不违规不封号

## ✨ 功能特色

- 💑 **姓名灵魂宿命配对** - AI智能解析姓名命理
- ⭐ **十二星座双向合盘** - 深度星座兼容性分析
- 📅 **八字五行夫妻合婚** - 中式传统命理解读
- 🔮 **前世今生因果轮回** - 神秘灵性解读
- 💌 **专属命运缘分海报** - 一键生成高清海报
- 🎴 **月老专属姻缘签** - 摇晃动画抽签

## 🎨 视觉特效

- 全屏动态星云背景
- 飘落爱心蝴蝶粒子
- 金色流光粒子动画
- 磨砂玻璃卡片设计
- 闪光边框呼吸灯效
- 弹性翻转页面转场
- 百分比进度条动画

## 🚀 快速部署

### 本地运行

**方式一：仅前端（使用本地模拟数据）**
```bash
# 直接双击 index.html 文件用浏览器打开即可
```

**方式二：完整前后端（需要AI生成真实内容）**

1. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

2. 启动后端服务：
```bash
python backend.py
```

3. 浏览器打开 `index.html` 文件

### GitHub Pages 部署

1. 将 `index.html` 推送到 GitHub 仓库
2. 开启 GitHub Pages 功能
3. 访问 `https://你的用户名.github.io/仓库名/`
4. 注意：前端单独部署时使用本地模拟数据

### EdgeOne Pages 部署

1. 登录 EdgeOne Pages
2. 导入项目或上传文件
3. 配置自定义域名（如需要）
4. 部署完成

## ⚙️ 配置说明

### 广告模式切换

在 `index.html` 文件中找到以下代码：
```javascript
// 【广告模式开关】设为 false = 无广告模式（默认），设为 true = 广告解锁模式
const AD_MODE = false;
```

- `false`：无广告模式，完整功能直接解锁
- `true`：广告解锁模式，需观看激励视频

### 后端API地址

在 `index.html` 文件中修改：
```javascript
const API_BASE = 'http://localhost:5000/api';
```

部署到服务器后，改为实际的后端地址。

### AI 接口配置

在 `backend.py` 文件中修改：
```python
# 【API Key 密钥粘贴位置】
API_KEY = "你的API密钥"

# 【AI 接口地址填写位置】
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
```

## 📱 手机适配

- 全响应式设计，完美适配所有手机屏幕
- 竖屏优化，适合抖音/微信内打开
- 海报 9:16 比例，适配手机壁纸
- 触摸优化，操作流畅

## 🔥 裂变玩法

- 分享到微信/QQ/朋友圈可免广告
- 专属缘分ID生成，情侣唯一标识
- 契合段位评级：天生绝配、灵魂伴侣等
- 一键保存海报，适配晒图传播

## 📂 项目结构

```
姻缘网站项目/
├── index.html          # 单文件前端（包含HTML+CSS+JS）
├── backend.py         # Python后端
├── requirements.txt   # Python依赖
└── README.md          # 使用说明
```

## ⚠️ 免责声明

本项目仅供娱乐消遣，测算结果纯属娱乐，请勿封建迷信。

## 📝 技术栈

- **前端**：HTML5 + CSS3 + JavaScript（原生）
- **后端**：Python + Flask
- **AI**：智谱 GLM-4-Flash
- **动画**：Canvas 2D
- **海报**：Canvas 绘图

## 🌟 Star History

如果这个项目对你有帮助，请给我一个 Star ⭐

---

Made with 💕 for 2026
