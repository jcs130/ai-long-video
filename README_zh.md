# 🎬 AI Long Video Generator

> **首尾帧控制 + 无限时长 + 角色一致性** - 开源 AI 视频生成工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Volcengine](https://img.shields.io/badge/Powered%20by-Volcengine-orange)](https://www.volcengine.com/)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/jcs130/ai-long-video)

**语言**: [🇬🇧 English](README.md) | **🇨🇳 中文**

**生产环境已验证** - 基于项目 001/002/003 完整测试通过

---

## 🎯 项目案例

### Project 001: AI 做视频介绍视频（25 秒）
- **内容**：介绍 AI 视频生成工具
- **时长**：25.22 秒
- **场景**：5 个镜头
- **成本**：约 5 元
- **特点**：首个完整案例，验证工作流

### Project 002: 一拳超人 vs 鸣人（2 分 10 秒）
- **内容**：动漫角色对战分析
- **时长**：130 秒
- **场景**：10 个镜头
- **成本**：约 20 元
- **特点**：长视频测试，角色一致性验证

### Project 003: 木屋烧烤宣传片（38 秒）✅ 最新
- **内容**：中年男性友情故事
- **时长**：38 秒
- **场景**：10 个镜头
- **成本**：约 18 元
- **特点**：
  - ✅ 角色设计文档（老张/老李）
  - ✅ 关键帧一致性（20 张图）
  - ✅ 多角色配音（旁白 + 老张 + 老李）
  - ✅ 音画同步（视频裁剪匹配配音）
  - ✅ 硬字幕嵌入
- **经验**：
  - ⚠️ 充分利用视频时长（支持 4-12 秒，不要固定 5 秒）
  - ⚠️ 生成关键帧前先设计角色（避免长相不一致）

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/jcs130/ai-long-video.git
cd ai-long-video

# 安装依赖
pip install volcenginesdkarkruntime requests pillow
```

### 2. 获取 API Key

**步骤 1**: 访问火山引擎 ARK 控制台  
👉 https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

**步骤 2**: 创建或选择 API Key
- 如果没有，点击"创建 API Key"
- 复制生成的 key（UUID 格式）

**步骤 3**: 设置环境变量
```bash
# Linux/Mac
export ARK_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:ARK_API_KEY="your-api-key-here"

# Windows (CMD)
set ARK_API_KEY=your-api-key-here
```

**说明**: 
- 有免费额度可供测试
- 价格：约 ¥0.05 元/5 秒视频
- 详见 [官方定价](https://www.volcengine.com/docs/82379/1399008)

### 3. 基本用法

```python
from volc_video_sdk import VolcVideo

# 使用 API key 初始化
video = VolcVideo(api_key="your-api-key")

# 使用首尾帧控制生成视频
task_id = video.create_task_with_first_last_frames(
    first_frame_path="frame1.jpeg",
    last_frame_path="frame2.jpeg",
    prompt="人物从微笑过渡到挥手，自然动作",
    duration=5,
    watermark=False
)
```

---

## ✨ 核心功能

### 🎯 首尾帧精准控制

**业界领先的首尾帧生成** + 关键帧插值技术：

- ✅ **首帧控制** - 指定视频开头（logo/产品/人物）
- ✅ **尾帧控制** - 指定视频结尾（二维码/联系方式/行动号召）
- ✅ **平滑过渡** - AI 自动生成中间帧，自然流畅
- ✅ **无缝拼接** - 多个片段连接无硬切痕迹

```python
# 首尾帧生成示例
video = sdk.generate_from_first_last_frames(
    first_frame_path="logo.png",      # 首帧：公司 logo
    last_frame_path="qrcode.png",     # 尾帧：二维码
    prompt="科技粒子特效过渡",
    duration=10                        # 10 秒平滑过渡
)
```

### ♾️ 无限时长视频

**理论上支持任意时长** - 通过首尾帧链式实现：

- ✅ **单片段**：4-12 秒（火山引擎限制）
- ✅ **链式方法**：前一段的尾帧 = 下一段的首帧
- ✅ **无缝连接**：AI 自动过渡，无硬切痕迹
- ✅ **无限扩展**：1 分钟、5 分钟、10 分钟...理论上无限

```python
# 生成 60 秒视频示例（5 个片段 × 12 秒）
frames = []
for i in range(6):
    # 生成关键帧
    frame = sdk.generate_frame(f"场景{i}，渐进变化")
    frames.append(frame)

# 链式生成完整视频
videos = []
for i in range(len(frames) - 1):
    video = sdk.generate_from_first_last_frames(
        first_frame_path=frames[i],
        last_frame_path=frames[i+1],
        prompt="平滑过渡",
        duration=12  # 每段 12 秒
    )
    videos.append(video)

# 合并所有片段（使用 FFmpeg）
# 总时长：5 段 × 12 秒 = 60 秒
```

**实际应用场景**：
- 📺 **微电影**：3-5 分钟（15-25 段链式）
- 🎓 **教育视频**：10-30 分钟（50-150 段链式）
- 🎬 **宣传片**：1-3 分钟（5-15 段链式）
- 📖 **有声书插画**：任意时长（按章节链式）

### 🎭 角色一致性

**解决 AI 视频最大痛点** - 角色/场景不一致：

- ✅ **角色锁定** - 固定角色描述模板
- ✅ **参考图** - 使用参考图保持一致性
- ✅ **多图融合** - 最多支持 4 张参考图融合
- ✅ **专业术语** - 支持舞蹈、体育等专业动作描述

### ⏱️ 12 秒长视频

**突破 5 秒限制**，充分利用 API 能力：

- ✅ **4-12 秒支持** - 单视频最长 12 秒
- ✅ **时长优势** - 支持 4-12 秒（大多数 AI 视频工具仅 5 秒）
- ✅ **多段链式** - 多段链式生成更长视频

---

## 💼 应用场景

### 企业宣传片
- 首帧：公司 logo + 名称
- 中间：AI 生成产品展示/团队风采
- 尾帧：联系方式 + 二维码

### 产品广告
- 首帧：产品特写
- 中间：使用场景演示
- 尾帧：购买链接 + 优惠信息

### 课程推广
- 首帧：讲师照片 + 课程标题
- 中间：课程亮点展示
- 尾帧：报名二维码

### 活动预告
- 首帧：活动主题海报
- 中间：活动亮点/嘉宾介绍
- 尾帧：时间/地点 + 报名入口

---

## 📊 技术对比

| 功能 | 标准 AI 视频 | 本工具 |
|------|-------------|--------|
| **首帧控制** | ❌ 不支持 | ✅ 精准控制 |
| **尾帧控制** | ❌ 不支持 | ✅ 精准控制 |
| **中间过渡** | ❌ 硬切/跳跃 | ✅ AI 平滑插值 |
| **角色一致性** | ⚠️ 易变形 | ✅ 参考图锁定 |
| **单段时长** | 5 秒 | 4-12 秒 |
| **总时长** | 5 秒 | ♾️ 无限（链式） |
| **无缝拼接** | ❌ 不支持 | ✅ 首尾帧连接 |
| **应用场景** | 短视频 | 微电影/教育/宣传片 |

---

## 📁 项目结构

```
ai-long-video/
├── volc_video_sdk.py       # 核心 SDK
├── volc_image_sdk.py       # 图片生成 SDK
├── SKILL.md                # 完整文档
├── README.md               # 英文 README
├── README_zh.md            # 中文 README（本文件）
├── CONFIG.md               # 配置指南
├── TROUBLESHOOTING.md      # ⭐ 踩坑指南 - 必读！
├── LICENSE                 # MIT 许可证
├── examples/
│   ├── project_001/        # 项目 001 示例
│   ├── project_002/        # 项目 002 示例
│   └── project_003_v2/     # 项目 003 V2 自动化脚本
└── docs/
    ├── API_REFERENCE.md    # API 参考
    └── BEST_PRACTICES.md   # 最佳实践
```

---

## 🔧 API 参数

### generate_from_first_last_frames

```python
def generate_from_first_last_frames(
    first_frame_path: str,    # 首帧图片路径
    last_frame_path: str,     # 尾帧图片路径
    prompt: str = "",         # 视频描述（可选）
    model: str = "ep-20260227022253-b67vh",  # 模型 ID
    watermark: bool = True,   # 是否加水印
    duration: int = 5         # 时长（4-12 秒）
) -> dict
```

**返回值**:
```python
{
    "task_id": "cgt-20260322123456-xxxxx",
    "video_url": "https://...",
    "status": "success",
    "duration": 5
}
```

---

## 💰 价格

**火山引擎 Seedance 1.5 Pro**:

- 5 秒视频：约 ¥0.05 元
- 10 秒视频：约 ¥0.10 元
- 首尾帧功能：**免费**（包含在基础 API 中）

详细定价见：https://www.volcengine.com/docs/82379/1399008

---

## 🎓 代码示例

### 示例 1: 企业宣传片

```python
from volc_video_sdk import VolcVideoSDK

sdk = VolcVideoSDK(api_key="your-api-key")

# 生成企业宣传片
video = sdk.generate_from_first_last_frames(
    first_frame_path="company_logo.png",
    last_frame_path="contact_qrcode.png",
    prompt="科技蓝色粒子特效，光线流动，专业氛围",
    duration=10,
    watermark=False
)

print(f"企业宣传片生成完成：{video['video_url']}")
```

### 示例 2: 产品广告

```python
# 生成产品广告
video = sdk.generate(
    prompt="智能手机展示，360 度旋转，屏幕点亮展示功能",
    duration=5,
    watermark=False
)
```

### 示例 3: 多段长视频

```python
# 生成 3 个片段
video1 = sdk.generate(prompt="开场动画", duration=5)
video2 = sdk.generate_from_first_last_frames(
    first_frame="product.jpg",
    last_frame="price.png",
    prompt="产品展示过渡",
    duration=10
)
video3 = sdk.generate(prompt="结束动画", duration=5)

# 使用 FFmpeg 合并
# ffmpeg -i video1.mp4 -i video2.mp4 -i video3.mp4 -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0" output.mp4
```

---

## 🤝 作为 Agent 技能使用

本工具已打包为 CoPaw Skill，可供 AI Agent 集成：

```python
# 在 Agent 中调用
from volc_video_sdk import VolcVideo

video = VolcVideo()
result = video.generate_from_first_last_frames(
    first_frame_path="logo.png",
    last_frame_path="qrcode.png",
    prompt="科技粒子特效过渡",
    duration=10
)
```

详细 Skill 文档见：[SKILL.md](SKILL.md)

---

## 📚 重要文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 技能使用指南 |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | ⭐ **踩坑指南** - 必读！ |
| [CONFIG.md](CONFIG.md) | 配置与路径设置 |
| [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) | 维护指南 |
| [SECURITY_CHECK.md](SECURITY_CHECK.md) | 安全审计报告 |

**强烈建议先阅读 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**，避免常见踩坑！

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **火山引擎** - 提供强大的视频生成 API
- **CoPaw** - 提供 Agent 框架支持
- **社区贡献者** - 感谢所有提交 Issue 和 PR 的同学

---

## 📮 问题反馈

如有问题或建议，请提交 [Issue](https://github.com/jcs130/ai-long-video/issues)

---

## ⭐ Star 历史

如果本项目对你有帮助，请给个 Star！🌟

[![Star History Chart](https://api.star-history.com/svg?repos=jcs130/ai-long-video&type=Date)](https://star-history.com/#jcs130/ai-long-video&Date)

---

*最后更新：2026-03-29*

---

## 📝 更新日志

### 2026-03-29
- ✅ 项目 003 完成（木屋烧烤宣传片）
- ✅ 添加角色设计工作流
- ✅ 添加视频时长充分利用经验（4-12 秒）
- ✅ 更新 SKILL.md 踩坑#12/#14/#15
- ✅ 添加完整自动化工作流脚本

### 2026-03-28
- ✅ 项目 002 完成（一拳超人 vs 鸣人）
- ✅ 添加多角色配音支持
- ✅ 添加音画同步工作流

### 2026-03-27
- ✅ 项目 001 完成（AI 做视频介绍）
- ✅ 首尾帧工作流验证通过
