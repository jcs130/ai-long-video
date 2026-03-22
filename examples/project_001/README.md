# 项目 001 - AI 做视频介绍视频

**完整示例** - 展示从脚本到成片的完整 AI 视频生成流程

## 📋 项目信息

- **主题**: AI 视频制作工具介绍
- **时长**: 25.22 秒
- **场景数**: 5 个
- **文件大小**: 
  - 原始输出：26MB
  - 压缩后：3.3MB（适合微信/飞书传播）
  - 带字幕版：6.4MB

## 🎬 脚本

```
做视频还在写脚本、拍素材、剪半天？OUT 了！
现在 AI 做视频，只要一句话。
输入主题，AI 自动写文案、生成分镜、生成视频、配好音。
30 秒视频，30 秒搞定。
成本？不到 1 块钱。
我是小咪，AI 视频专家。
关注我，教你用 AI 做爆款。
```

**字数**: 124 字符  
**TTS 语音**: 小何 2.0 (`zh_female_xiaohe_uranus_bigtts`)

## 📁 文件结构

```
project_001/
├── source/              # 源文件
│   ├── frame1.jpeg      # 关键帧 1 - 开场
│   ├── frame2.jpeg      # 关键帧 2 - 痛点场景
│   ├── frame3.jpeg      # 关键帧 3 - AI 工作流
│   ├── frame4.jpeg      # 关键帧 4 - 效率对比
│   ├── frame5.jpeg      # 关键帧 5 - 成本优势
│   ├── frame6.jpeg      # 关键帧 6 - 结尾号召
│   ├── scene_1.mp4      # 视频片段 1 (4.68s)
│   ├── scene_2.mp4      # 视频片段 2 (4.42s)
│   ├── scene_3.mp4      # 视频片段 3 (5.36s)
│   ├── scene_4.mp4      # 视频片段 4 (5.18s)
│   ├── scene_5.mp4      # 视频片段 5 (5.58s)
│   ├── narration_volc_official.mp3  # TTS 配音
│   └── subtitles.srt    # 字幕文件
├── output/              # 最终输出
│   ├── video_volc_final.mp4         # 原始合并版 (26MB)
│   ├── video_volc_compressed.mp4    # 压缩版 (3.3MB)
│   └── video_with_subtitles.mp4     # 带字幕版 (6.4MB)
└── README.md            # 本文件
```

## 🛠️ 生成命令

### 1. 合并视频片段

```bash
# 创建合并列表
cat > concat_list.txt << EOF
file 'scene_1.mp4'
file 'scene_2.mp4'
file 'scene_3.mp4'
file 'scene_4.mp4'
file 'scene_5.mp4'
EOF

# 合并视频
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy video_merged.mp4
```

### 2. 添加 TTS 配音（移除原背景音乐）

```bash
ffmpeg -i video_merged.mp4 -i narration_volc_official.mp3 \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest \
  video_with_narration.mp4
```

### 3. 压缩视频（适合社交媒体传播）

```bash
ffmpeg -i video_with_narration.mp4 \
  -c:v libx264 -crf 28 -preset medium \
  -c:a aac -b:a 128k -movflags +faststart \
  video_compressed.mp4
```

### 4. 添加硬字幕

```bash
ffmpeg -i video_compressed.mp4 \
  -vf "subtitles=subtitles.srt:force_style='Fontsize=24,PrimaryColour=&H00FFFF,BackColour=&H80000000,BorderStyle=4,MarginV=25'" \
  -c:a copy video_with_subtitles.mp4
```

## 📊 关键参数

### 首尾帧控制 API 调用

```python
from volc_video_sdk import VolcVideo

video = VolcVideo(api_key="YOUR_API_KEY")

# 示例：生成片段 1（开场→痛点）
segments = video.generate_with_consistency(
    prompt="镜头推进，展现传统视频制作的复杂流程",
    first_frame_path="frame1.jpeg",
    last_frame_path="frame2.jpeg",
    duration=12,
    model_id="ep-20260227022253-b67vh"  # 用户端点 ID
)
```

### TTS 配置

- **端点**: `https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse`
- **Voice**: `zh_female_xiaohe_uranus_bigtts`
- **模型**: `seed-tts-2.0`
- **速度**: 1.0
- **情感**: 中性

## 💡 使用建议

1. **关键帧设计**: 每个场景的首尾帧要有明确的视觉联系，确保过渡流畅
2. **时长控制**: 单个片段建议 4-6 秒，总时长控制在 30 秒内
3. **字幕样式**: 使用蓝色 (`&H00FFFF`) 配黑色半透明背景，确保可读性
4. **压缩参数**: CRF 28 在画质和文件大小间取得良好平衡

## 📈 成本明细

| 项目 | 用量 | 单价 | 费用 |
|------|------|------|------|
| 图像生成 (6 张) | 6 tokens | ¥0.00125/token | ¥0.0075 |
| 视频生成 (5 段) | 5 × 12s | ¥0.12/s | ¥7.20 |
| TTS (124 字) | 124 tokens | ¥0.0005/token | ¥0.062 |
| **总计** | | | **¥7.33** |

*实际成本可能因 API 定价调整而变化*

## 🔗 相关文档

- [主项目 README](../../README.md)
- [故障排查指南](../../TROUBLESHOOTING.md)
- [维护指南](../../MAINTENANCE_GUIDE.md)
- [字幕制作指南](../../../media/project_001/字幕制作指南.md)

---

**生成时间**: 2026-03-23  
**GitHub**: https://github.com/jcs130/ai-long-video
