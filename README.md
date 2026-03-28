# 🎬 AI Long Video Generator

> **首尾帧控制 + 无限时长 + 角色一致性** - 开源 AI 视频生成工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Volcengine](https://img.shields.io/badge/Volcengine-Seedance-green.svg)](https://www.volcengine.com/)
[![Status](https://img.shields.io/badge/status-production%20ready-success.svg)](https://github.com/jcs130/ai-long-video)

**生产环境已验证** - 基于 3 个完整项目测试通过

---

## 📺 示例项目

| 项目 | 主题 | 时长 | 场景 | 成本 | 查看 |
|------|------|------|------|------|------|
| **Project 001** | AI 做视频介绍 | 25 秒 | 5 | 5 元 | [📁 示例](examples/project_001/) |
| **Project 002** | 一拳超人 vs 鸣人战力分析 | 2 分 10 秒 | 10 | 20 元 | [📁 示例](examples/project_002/) |
| **Project 003** | 木屋烧烤宣传片 | 55 秒 | 10 | 18 元 | [📁 示例](examples/project_003/) |

### Project 001: AI 做视频介绍视频 ⭐

**25 秒知识分享类短视频**

- **脚本**：124 字，5 个场景
- **关键帧**：6 张 (1920x1920)
- **视频**：5 段 × 5 秒
- **TTS**：火山引擎小何 2.0
- **输出**：3 个版本 (26MB/3.3MB/6.4MB)

```bash
cd examples/project_001
python3 generate_keyframes.py
python3 generate_videos.py
python3 generate_tts.py
ffmpeg -i video_merged.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 video_final.mp4
```

**特点**：完整工作流演示，适合快速上手

---

### Project 002: 一拳超人 vs 鸣人战力分析 🥊

**2 分 10 秒跨次元对决分析**

- **脚本**：537 字，10 个场景
- **关键帧**：20 张 (1920x1920)
- **视频**：10 段 × 12 秒
- **TTS**：288KB，36 秒配音
- **输出**：15MB 完整版

**踩坑记录**：
- TTS API 格式必须用简化版 `{"user": {...}, "req_params": {...}}`
- 角色描述要具体：包含角色名 + 作品名 + 外观特征
- 阿里云盘 API 返回 201 也是成功

```bash
cd examples/project_002
python3 generate_srt.py
python3 generate_tts_correct.py
ffmpeg -i video_merged.mp4 -vf "subtitles=subtitles.srt:force_style='...'" video_with_subs.mp4
ffmpeg -i video_with_subs.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 video_final.mp4
```

**特点**：长视频制作，多 Agent 协作流程

---

### Project 003: 木屋烧烤宣传片 🍖

**55 秒品牌形象片 - 雨夜海边兄弟情**

- **脚本**：165 字，10 个场景，电影质感
- **关键帧**：20 张 (1920x1920)
- **视频**：10 段 (3-10 秒各不同)
- **TTS**：288KB，小何 2.0 知性女声
- **输出**：15MB 完整版

**创意亮点**：
- 雨夜海边场景，暖黄灯光 vs 深蓝雨夜对比
- 兄弟情 + 奋斗回忆 + 人生感悟
- 品牌定位：不只是烧烤店，是情感寄托的地方

**经典台词**：
> "日子啊，就是有人陪你吃肉，有人陪你扛事。"
> "木屋烧烤——有些话，有些肉，只和懂你的人分享。"

**特点**：商业宣传片案例，情感叙事

---

## 🚀 快速开始

### 1. 安装

```bash
git clone https://github.com/jcs130/ai-long-video.git
cd ai-long-video
pip install volcenginesdkarkruntime requests
```

### 2. 配置 API Key

```bash
export ARK_API_KEY="your-api-key-here"
```

获取 API Key: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

### 3. 使用示例

```python
from volc_video_sdk import VolcVideo

video = VolcVideo(api_key="your-api-key")

# 首尾帧生成视频
task_id = video.create_task_with_first_last_frames(
    first_frame_path="frame1.jpeg",
    last_frame_path="frame2.jpeg",
    prompt="人物从微笑到挥手，自然过渡",
    duration=5,
    watermark=False
)
```

---

## 📚 重要文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 技能使用说明 |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) ⭐ | **踩坑指南 - 必读！** |
| [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) | 维护指南 |
| [SECURITY_CHECK.md](SECURITY_CHECK.md) | 安全检查报告 |

**强烈建议先阅读 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)，避免重复踩坑！**

---

## ✨ 核心特性

### 🎯 首尾帧精确控制

**业界领先的首尾帧生成功能**，支持关键帧插值：

- ✅ **首帧控制** - 指定视频开头画面（Logo/产品/人物）
- ✅ **尾帧控制** - 指定视频结尾画面（二维码/联系方式/CTA）
- ✅ **流畅过渡** - AI 自动生成中间帧，过渡自然
- ✅ **无缝拼接** - 多个片段首尾衔接，生成超长视频

```python
# 首尾帧生成示例
video = sdk.generate_from_first_last_frames(
    first_frame_path="logo.png",      # 首帧：公司 Logo
    last_frame_path="qrcode.png",     # 尾帧：二维码
    prompt="科技感粒子特效过渡",
    duration=10                       # 10 秒流畅过渡
)
```

---

### ♾️ 无限时长视频

**理论支持任意时长** - 通过首尾帧拼接实现：

- ✅ **单段时长**: 4-12 秒（火山引擎限制）
- ✅ **拼接方式**: 上一段尾帧 = 下一段首帧
- ✅ **无缝衔接**: AI 自动过渡，无硬切痕迹
- ✅ **无限延长**: 1 分钟、5 分钟、10 分钟... 理论上无限制

```python
# 生成 60 秒视频示例（5 段 × 12 秒）
frames = []
for i in range(6):
    # 生成关键帧
    frame = sdk.generate_frame(f"场景{i}，渐进变化")
    frames.append(frame)

# 拼接成完整视频
videos = []
for i in range(len(frames) - 1):
    video = sdk.generate_from_first_last_frames(
        first_frame_path=frames[i],
        last_frame_path=frames[i+1],
        prompt="流畅过渡",
        duration=12  # 每段 12 秒
    )
    videos.append(video)

# 合并所有片段（使用 FFmpeg）
# 总时长：5 段 × 12 秒 = 60 秒
```

**实际应用案例**:
- 📺 **微电影**: 3-5 分钟（15-25 段拼接）
- 🎓 **教学视频**: 10-30 分钟（50-150 段拼接）
- 🎬 **宣传片**: 1-3 分钟（5-15 段拼接）
- 📖 **有声书配图**: 任意时长（按章节拼接）

---

### 🎭 角色一致性

**解决 AI 视频最大痛点** - 人物/场景不一致：

- ✅ **角色锁定** - 固定人物描述模板
- ✅ **参考图功能** - 使用参考图保持一致性
- ✅ **多帧融合** - 最多 4 张参考图融合
- ✅ **专业术语** - 支持舞蹈、运动等专业动作描述

**角色一致性技巧**:

| 问题 | 解决方案 |
|------|----------|
| 角色长得不像 | prompt 包含角色名 + 作品名 + 外观特征 |
| 不同场景角色不一致 | 使用相同 seed 值 + 参考图 |
| 剪影太抽象 | 用具体服装颜色 + 发型描述 |
| AI 理解偏差 | 加英文角色名：Saitama (One-Punch Man) |

---

### ⏱️ 12 秒长视频

**突破 5 秒限制**，充分利用 API 能力：

- ✅ **4-12 秒支持** - 单段视频最长 12 秒
- ✅ **时长优势** - 支持 4-12 秒视频（普通 AI 视频通常仅 5 秒）
- ✅ **多段拼接** - 可拼接多个片段获得更长视频

---

## 💼 应用场景

### 企业宣传片
- 首帧：公司 Logo + 名称
- 中间：AI 生成产品展示/团队风采
- 尾帧：联系方式 + 二维码

### 产品广告
- 首帧：产品特写
- 中间：使用场景展示
- 尾帧：购买链接 + 优惠信息

### 课程推广
- 首帧：讲师照片 + 课程标题
- 中间：课程内容亮点
- 尾帧：报名二维码

### 活动预告
- 首帧：活动主题海报
- 中间：活动亮点/嘉宾介绍
- 尾帧：时间地点 + 报名入口

### 知识分享短视频
- 开场：痛点/问题/反差（3-5 秒）
- 主体：解决方案/步骤/案例（20-40 秒）
- 结尾：总结 + 行动号召（5-10 秒）

---

## 📊 技术对比

| 功能 | 普通 AI 视频 | 本工具 |
|------|-------------|--------|
| 首帧控制 | ❌ 不支持 | ✅ 精确控制 |
| 尾帧控制 | ❌ 不支持 | ✅ 精确控制 |
| 中间过渡 | ❌ 硬切/跳跃 | ✅ AI 流畅插值 |
| 角色一致性 | ⚠️ 容易变形 | ✅ 参考图锁定 |
| 单段时长 | 5 秒 | 4-12 秒 |
| 总时长 | 5 秒 | ♾️ 无限（通过拼接） |
| 无缝拼接 | ❌ 不支持 | ✅ 首尾帧衔接 |
| 适用场景 | 短视频 | 微电影/教学/宣传片 |

---

## 🔧 API 参数说明

### generate_from_first_last_frames

```python
def generate_from_first_last_frames(
    first_frame_path: str,    # 首帧图片路径
    last_frame_path: str,     # 尾帧图片路径
    prompt: str = "",         # 视频描述（可选）
    model: str = "ep-20260227022253-b67vh",  # 模型 ID
    watermark: bool = True,   # 是否添加水印
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

## 💰 计费说明

**火山引擎 Seedance 1.5 Pro**:

- 图片生成：~0.15 元/张 (1920x1920)
- 5 秒视频：~0.75 元/条
- 10 秒视频：~1.5 元/条
- 12 秒视频：~1.8 元/条
- 首尾帧功能：**免费**（包含在基础 API 中）

**TTS 配音**:
- 新账号免费额度：2000 字/月
- 超出后：~0.01 元/字

**项目成本参考**:
- Project 001 (25 秒): ~5 元
- Project 002 (2 分 10 秒): ~20 元
- Project 003 (55 秒): ~18 元

详细计费标准：https://www.volcengine.com/docs/82379/1399008

---

## 📁 项目结构

```
ai-long-video/
├── volc_video_sdk.py         # 核心 SDK
├── volc_image_sdk.py         # 图片生成 SDK
├── volc_tts_sdk.py           # TTS 配音 SDK
├── SKILL.md                  # 完整文档
├── README.md                 # 使用说明
├── TROUBLESHOOTING.md        # 踩坑指南（20+ 条）
├── MAINTENANCE_GUIDE.md      # 维护指南
├── LICENSE                   # MIT 许可证
├── requirements.txt          # Python 依赖
└── examples/                 # 示例项目
    ├── project_001/          # AI 做视频介绍（25 秒）
    │   ├── README.md
    │   ├── generate_keyframes.py
    │   ├── generate_videos.py
    │   ├── generate_tts.py
    │   └── video_final.mp4
    ├── project_002/          # 一拳超人 vs 鸣人（2 分 10 秒）
    │   ├── README.md
    │   ├── 脚本_一拳超人 vs 鸣人.md
    │   ├── generate_srt.py
    │   ├── generate_tts_correct.py
    │   └── video_final.mp4
    └── project_003/          # 木屋烧烤宣传片（55 秒）
        ├── README.md
        ├── 脚本_木屋烧烤.md
        ├── generate_srt.py
        ├── generate_tts.py
        └── video_final.mp4
```

---

## 🎓 示例代码

### 示例 1：企业宣传片

```python
from volc_video_sdk import VolcVideoSDK

sdk = VolcVideoSDK(api_key="your-api-key")

# 生成企业宣传片
video = sdk.generate_from_first_last_frames(
    first_frame_path="company_logo.png",
    last_frame_path="contact_qrcode.png",
    prompt="科技感蓝色粒子特效，光线流动，专业大气",
    duration=10,
    watermark=False
)

print(f"企业宣传片生成成功：{video['video_url']}")
```

### 示例 2：多段拼接长视频

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

# 使用 FFmpeg 拼接
# ffmpeg -i video1.mp4 -i video2.mp4 -i video3.mp4 \
#   -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0" output.mp4
```

---

## 🤝 作为 Agent 技能使用

本工具已封装为 CoPaw Skill，可直接集成到 AI Agent 中：

```python
# 在 Agent 中调用
from volc_video_sdk import VolcVideo

video = VolcVideo()
result = video.generate_from_first_last_frames(
    first_frame_path="logo.png",
    last_frame_path="qrcode.png",
    prompt="科技感粒子特效过渡",
    duration=10
)
```

详细 Skill 文档：[SKILL.md](SKILL.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **火山引擎** - 提供强大的视频生成 API
- **CoPaw** - Agent 框架支持
- **社区贡献者** - 感谢所有提 Issue 和 PR 的朋友

---

## 📮 问题反馈

如有问题或建议，欢迎提 [Issue](https://github.com/jcs130/ai-long-video/issues)

---

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star！🌟

[![Star History Chart](https://api.star-history.com/svg?repos=jcs130/ai-long-video&type=Date)](https://star-history.com/#jcs130/ai-long-video&Date)

---

*最后更新：2026-03-28*
