# 🎬 AI Long Video Generator

> **First-Last Frame Control + Unlimited Duration + Character Consistency** - Open Source AI Video Generation Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Volcengine](https://img.shields.io/badge/Powered%20by-Volcengine-orange)](https://www.volcengine.com/)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/jcs130/ai-long-video)

**Language**: **🇬🇧 English** | [🇨🇳 中文](README_zh.md)

**Production Ready** - Tested with 3 complete projects (001/002/003)

---

## 🎯 Project Showcase

### Project 001: AI Video Introduction (25 seconds)
- **Content**: Introduction to AI video generation tool
- **Duration**: 25.22 seconds
- **Scenes**: 5 shots
- **Cost**: ~¥5 CNY
- **Features**: First complete case, workflow validation

### Project 002: One Punch Man vs Naruto (2 min 10 sec)
- **Content**: Anime character battle analysis
- **Duration**: 130 seconds
- **Scenes**: 10 shots
- **Cost**: ~¥20 CNY
- **Features**: Long video test, character consistency validation

### Project 003: Muwu BBQ Promotional Video (38 seconds) ✅ Latest
- **Content**: Middle-aged men's friendship story
- **Duration**: 38 seconds
- **Scenes**: 10 shots
- **Cost**: ~¥18 CNY
- **Features**:
  - ✅ Character design document (Lao Zhang / Lao Li)
  - ✅ Keyframe consistency (20 images)
  - ✅ Multi-role voiceover (Narrator + Lao Zhang + Lao Li)
  - ✅ Audio-video sync (video clipped to match audio)
  - ✅ Hard subtitle embedding
- **Lessons**:
  - ⚠️ Fully utilize video duration (supports 4-12s, don't fix at 5s)
  - ⚠️ Design characters before generating keyframes (avoid inconsistent appearance)

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/jcs130/ai-long-video.git
cd ai-long-video

# Install dependencies
pip install volcenginesdkarkruntime requests pillow
```

### 2. Get API Key

**Step 1**: Visit Volcengine ARK Console  
👉 https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

**Step 2**: Create or select your API Key
- Click "Create API Key" if you don't have one
- Copy the generated key (starts with UUID format)

**Step 3**: Set environment variable
```bash
# Linux/Mac
export ARK_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:ARK_API_KEY="your-api-key-here"

# Windows (CMD)
set ARK_API_KEY=your-api-key-here
```

**Note**: 
- Free tier available for testing
- Pricing: ~¥0.05 CNY per 5-second video
- See [official pricing](https://www.volcengine.com/docs/82379/1399008) for details

### 3. Basic Usage

```python
from volc_video_sdk import VolcVideo

# Initialize with API key
video = VolcVideo(api_key="your-api-key")

# Generate video with first-last frame control
task_id = video.create_task_with_first_last_frames(
    first_frame_path="frame1.jpeg",
    last_frame_path="frame2.jpeg",
    prompt="Person transitions from smile to wave, natural motion",
    duration=5,
    watermark=False
)
```

---

## ✨ Core Features

### 🎯 First-Last Frame Precision Control

**Industry-leading first-last frame generation** with keyframe interpolation:

- ✅ **First Frame Control** - Specify video opening (logo/product/person)
- ✅ **Last Frame Control** - Specify video ending (QR code/contact/CTA)
- ✅ **Smooth Transition** - AI generates intermediate frames naturally
- ✅ **Seamless Stitching** - Multiple segments connect without hard cuts

```python
# First-last frame generation example
video = sdk.generate_from_first_last_frames(
    first_frame_path="logo.png",      # First: Company logo
    last_frame_path="qrcode.png",     # Last: QR code
    prompt="Tech particle effects transition",
    duration=10                        # 10 seconds smooth transition
)
```

### ♾️ Unlimited Duration Video

**Theoretically supports any duration** - achieved through first-last frame chaining:

- ✅ **Single Segment**: 4-12 seconds (Volcengine limitation)
- ✅ **Chaining Method**: Previous segment's last frame = Next segment's first frame
- ✅ **Seamless Connection**: AI auto-transitions, no hard cut marks
- ✅ **Unlimited Extension**: 1 min, 5 min, 10 min... theoretically unlimited

```python
# Generate 60-second video example (5 segments × 12 seconds)
frames = []
for i in range(6):
    # Generate keyframes
    frame = sdk.generate_frame(f"Scene {i}, progressive change")
    frames.append(frame)

# Chain into complete video
videos = []
for i in range(len(frames) - 1):
    video = sdk.generate_from_first_last_frames(
        first_frame_path=frames[i],
        last_frame_path=frames[i+1],
        prompt="Smooth transition",
        duration=12  # 12 seconds per segment
    )
    videos.append(video)

# Merge all segments (using FFmpeg)
# Total duration: 5 segments × 12 seconds = 60 seconds
```

**Real-world Applications**:
- 📺 **Micro-films**: 3-5 minutes (15-25 segments chained)
- 🎓 **Educational Videos**: 10-30 minutes (50-150 segments chained)
- 🎬 **Promotional Videos**: 1-3 minutes (5-15 segments chained)
- 📖 **Audiobook Illustrations**: Any duration (chained by chapters)

### 🎭 Character Consistency

**Solving AI video's biggest pain point** - inconsistent characters/scenes:

- ✅ **Character Lock** - Fixed character description template
- ✅ **Reference Image** - Use reference images for consistency
- ✅ **Multi-frame Fusion** - Up to 4 reference images fused
- ✅ **Professional Terminology** - Supports dance, sports, and other professional action descriptions

### ⏱️ 12-Second Long Videos

**Breaking the 5-second limit**, fully utilizing API capabilities:

- ✅ **4-12 Second Support** - Single video up to 12 seconds
- ✅ **Duration Advantage** - Supports 4-12 seconds (most AI video tools only 5 seconds)
- ✅ **Multi-segment Chaining** - Chain multiple segments for longer videos

---

## 💼 Use Cases

### Corporate Promotional Videos
- First frame: Company logo + name
- Middle: AI-generated product showcase / team highlights
- Last frame: Contact info + QR code

### Product Advertisements
- First frame: Product close-up
- Middle: Usage scenario demonstration
- Last frame: Purchase link + discount info

### Course Promotion
- First frame: Instructor photo + course title
- Middle: Course content highlights
- Last frame: Registration QR code

### Event Previews
- First frame: Event theme poster
- Middle: Event highlights / guest introduction
- Last frame: Time/location + registration entrance

---

## 📊 Technical Comparison

| Feature | Standard AI Video | This Tool |
|---------|------------------|-----------|
| **First Frame Control** | ❌ Not supported | ✅ Precision control |
| **Last Frame Control** | ❌ Not supported | ✅ Precision control |
| **Middle Transition** | ❌ Hard cut/jump | ✅ AI smooth interpolation |
| **Character Consistency** | ⚠️ Easy to deform | ✅ Reference image lock |
| **Single Segment Duration** | 5 seconds | 4-12 seconds |
| **Total Duration** | 5 seconds | ♾️ Unlimited (via chaining) |
| **Seamless Stitching** | ❌ Not supported | ✅ First-last frame connection |
| **Use Cases** | Short videos | Micro-films/Education/Promos |

---

## 📁 Project Structure

```
ai-long-video/
├── volc_video_sdk.py       # Core SDK
├── volc_image_sdk.py       # Image generation SDK
├── SKILL.md                # Complete documentation
├── README.md               # This file
├── CONFIG.md               # Configuration guide
├── TROUBLESHOOTING.md      # ⭐ Pitfall guide - Must read!
├── LICENSE                 # MIT License
├── examples/
│   ├── project_001/        # Project 001 examples
│   ├── project_002/        # Project 002 examples
│   └── project_003_v2/     # Project 003 V2 automation scripts
└── docs/
    ├── API_REFERENCE.md    # API reference
    └── BEST_PRACTICES.md   # Best practices
```

---

## 🔧 API Parameters

### generate_from_first_last_frames

```python
def generate_from_first_last_frames(
    first_frame_path: str,    # Path to first frame image
    last_frame_path: str,     # Path to last frame image
    prompt: str = "",         # Video description (optional)
    model: str = "ep-20260227022253-b67vh",  # Model ID
    watermark: bool = True,   # Whether to add watermark
    duration: int = 5         # Duration (4-12 seconds)
) -> dict
```

**Return Value**:
```python
{
    "task_id": "cgt-20260322123456-xxxxx",
    "video_url": "https://...",
    "status": "success",
    "duration": 5
}
```

---

## 💰 Pricing

**Volcengine Seedance 1.5 Pro**:

- 5-second video: ~¥0.05 CNY
- 10-second video: ~¥0.10 CNY
- First-last frame feature: **Free** (included in base API)

For detailed pricing, see: https://www.volcengine.com/docs/82379/1399008

---

## 🎓 Code Examples

### Example 1: Corporate Promotional Video

```python
from volc_video_sdk import VolcVideoSDK

sdk = VolcVideoSDK(api_key="your-api-key")

# Generate corporate promo
video = sdk.generate_from_first_last_frames(
    first_frame_path="company_logo.png",
    last_frame_path="contact_qrcode.png",
    prompt="Tech blue particle effects, light flow, professional atmosphere",
    duration=10,
    watermark=False
)

print(f"Corporate promo generated: {video['video_url']}")
```

### Example 2: Product Advertisement

```python
# Generate product ad
video = sdk.generate(
    prompt="Smartphone showcase, 360-degree rotation, screen lights up showing features",
    duration=5,
    watermark=False
)
```

### Example 3: Multi-segment Long Video

```python
# Generate 3 segments
video1 = sdk.generate(prompt="Opening animation", duration=5)
video2 = sdk.generate_from_first_last_frames(
    first_frame="product.jpg",
    last_frame="price.png",
    prompt="Product showcase transition",
    duration=10
)
video3 = sdk.generate(prompt="Ending animation", duration=5)

# Merge with FFmpeg
# ffmpeg -i video1.mp4 -i video2.mp4 -i video3.mp4 -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0" output.mp4
```

---

## 🤝 Use as Agent Skill

This tool is packaged as a CoPaw Skill for AI Agent integration:

```python
# Call in Agent
from volc_video_sdk import VolcVideo

video = VolcVideo()
result = video.generate_from_first_last_frames(
    first_frame_path="logo.png",
    last_frame_path="qrcode.png",
    prompt="Tech particle effects transition",
    duration=10
)
```

For detailed Skill documentation, see: [SKILL.md](SKILL.md)

---

## 📚 Important Documentation

| Document | Description |
|----------|-------------|
| [SKILL.md](SKILL.md) | Skill usage guide |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | ⭐ **Pitfall Guide** - Must read! |
| [CONFIG.md](CONFIG.md) | Configuration & path setup |
| [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md) | Maintenance guide |
| [SECURITY_CHECK.md](SECURITY_CHECK.md) | Security audit report |

**Strongly recommend reading [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first** to avoid common pitfalls!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **Volcengine** - For powerful video generation API
- **CoPaw** - For Agent framework support
- **Community Contributors** - Thanks to everyone who filed Issues and PRs

---

## 📮 Issue Reporting

For questions or suggestions, please file an [Issue](https://github.com/jcs130/ai-long-video/issues)

---

## ⭐ Star History

If this project helps you, please give it a Star! 🌟

[![Star History Chart](https://api.star-history.com/svg?repos=jcs130/ai-long-video&type=Date)](https://star-history.com/#jcs130/ai-long-video&Date)

---

*Last updated: 2026-03-29*

---

## 📝 Changelog

### 2026-03-29
- ✅ Project 003 completed (Muwu BBQ promotional video)
- ✅ Added character design workflow
- ✅ Added video duration optimization tips (4-12 seconds)
- ✅ Updated SKILL.md pitfalls #12/#14/#15
- ✅ Added complete automation workflow scripts

### 2026-03-28
- ✅ Project 002 completed (One Punch Man vs Naruto)
- ✅ Added multi-role voiceover support
- ✅ Added audio-video sync workflow

### 2026-03-27
- ✅ Project 001 completed (AI video introduction)
- ✅ First-last frame workflow validated
