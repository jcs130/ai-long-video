# 🚧 AI Long Video - 踩坑指南

**创建时间**: 2026-03-23  
**基于项目**: 项目 001 - AI 做视频介绍视频  
**目的**: 记录所有踩过的坑，避免重复犯错

---

## 📋 目录

1. [API 调用相关](#api-调用相关)
2. [图片生成相关](#图片生成相关)
3. [视频生成相关](#视频生成相关)
4. [TTS 配音相关](#tts-配音相关)
5. [视频拼接相关](#视频拼接相关)
6. [文件管理相关](#文件管理相关)
7. [音频处理相关](#音频处理相关)

---

## API 调用相关

### 坑 1：模型 ID 错误导致 404

**问题**: 使用 `doubao-seedance-1-5-pro-250528` 返回 404 错误

```python
# ❌ 错误用法
result = client.content_generation.tasks.create(
    model="doubao-seedance-1-5-pro-250528",  # 404 错误
    content=content
)
```

**解决方案**: 使用用户端点 ID

```python
# ✅ 正确用法
result = client.content_generation.tasks.create(
    model="ep-20260227022253-b67vh",  # 用户端点
    content=content
)
```

**原因**: 公共模型 ID 和用户端点 ID 不同，需要使用控制台分配的端点 ID

**教训**: 始终使用用户端点 ID，不要直接使用公共模型 ID

---

### 坑 2：首尾帧参数格式错误

**问题**: 首尾帧同时传递时 API 报错

**错误尝试 1**: 使用 `control_type` 参数

```python
# ❌ 错误格式
content = [
    {"type": "text", "text": "prompt --dur 5"},
    {"type": "image_url", "image_url": "data:image;base64,...", "control_type": "first_frame"},
    {"type": "image_url", "image_url": "data:image;base64,...", "control_type": "last_frame"}
]
```

**错误尝试 2**: `image_url` 不是嵌套对象

```python
# ❌ 错误格式
content = [
    {"type": "image_url", "image_url": "data:image;base64,...", "role": "first_frame"},
    {"type": "image_url", "image_url": "data:image;base64,...", "role": "last_frame"},
    {"type": "text", "text": "prompt"}
]
```

**解决方案**: 正确的嵌套格式

```python
# ✅ 正确格式
content = [
    {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{first_b64}"
        },
        "role": "first_frame"  # 注意是 role 不是 control_type
    },
    {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{last_b64}"
        },
        "role": "last_frame"
    },
    {
        "type": "text",
        "text": f"{prompt} --wm false --dur 5"  # 参数放在最后
    }
]
```

**关键点**:
- `image_url` 必须是对象 `{"url": "data:..."}`，不是字符串
- 使用 `role: "first_frame"` 和 `role: "last_frame"` 区分
- 文本参数放在最后，包含 `--wm` 和 `--dur`

**教训**: 严格按照 SDK 的 `_build_content_with_first_last_frames` 方法格式

---

### 坑 3：API Key 格式问题

**问题**: 某些 API 需要完整的认证信息，不仅仅是 API Key

**TTS API 需要**:
- APP_ID
- ACCESS_TOKEN  
- RESOURCE_ID

**视频/图片 API 需要**:
- API_KEY (ARK_API_KEY)

**解决方案**: 区分不同服务的认证方式

```python
# 视频/图片 API
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="8d27bf88-53b0-4656-9946-f21934f4f24b"
)

# TTS API (WebSocket)
headers = {
    "X-Api-App-Key": "3019120872",
    "X-Api-Access-Key": "qcdGrSiKz8_8qTkHo1whQREW48QPWT6I",
    "X-Api-Resource-Id": "volc.service_type.10029",
    "X-Api-Connect-Id": connection_id
}
```

**教训**: 不同服务认证方式不同，需要查看对应文档

---

## 图片生成相关

### 坑 4：图片 URL 过期

**问题**: 生成的图片 URL 有有效期（约 24 小时），过期后无法访问

**现象**:
```python
# 第一次下载成功
curl -o frame1.jpeg "https://..."

# 几小时后下载失败（返回 217 字节的错误信息）
curl -o frame4.jpeg "https://..."  # 文件只有 217 字节
```

**解决方案**: 生成后立即下载到本地

```python
import requests

# 生成图片
result = generator.generate(prompt=prompt, ...)
url = result['urls'][0]

# 立即下载
img_data = requests.get(url).content
with open('local_frame.jpeg', 'wb') as f:
    f.write(img_data)
```

**教训**: 不要依赖临时 URL，立即保存为本地文件

---

### 坑 5：图片尺寸要求

**问题**: 火山引擎要求图片尺寸至少 3686400 像素

**解决方案**: 使用 2K 尺寸（约 2048x2048）

```python
result = generator.generate(
    prompt=prompt,
    size='2K',  # 使用 2K 尺寸
    ...
)
```

**教训**: 始终使用 2K 尺寸，避免尺寸错误

---

## 视频生成相关

### 坑 6：视频生成需要等待

**问题**: 视频生成不是实时的，需要 1-3 分钟

**解决方案**: 轮询检查状态

```python
import time

# 提交任务
task_id = client.content_generation.tasks.create(...).id

# 轮询检查
while True:
    result = client.content_generation.tasks.get(task_id=task_id)
    if result.status == 'succeeded':
        video_url = result.content.video_url
        break
    elif result.status == 'failed':
        print(f"生成失败：{result.error}")
        break
    else:
        print(f"处理中：{result.status}")
        time.sleep(10)  # 每 10 秒检查一次
```

**教训**: 异步任务需要轮询，设置合理超时时间

---

### 坑 7：视频自带音频轨道

**问题**: 生成的视频已经包含背景音乐，不需要额外添加

**发现**: 
```bash
ffprobe video.mp4
# 显示有 video 和 audio 两个轨道
codec_type=video
codec_type=audio
```

**解决方案**: 如果需要人声配音，需要：
1. 生成 TTS 音频
2. 混合原视频背景音乐和人声（调整音量比例）

**教训**: 先检查视频是否有音频，再决定是否需要添加

---

## TTS 配音相关

### 坑 8：TTS API 认证复杂

**问题**: TTS API 需要 APP_ID、ACCESS_TOKEN、RESOURCE_ID 三个参数

**错误**: 只传 API Key 会报错 `get resource id empty`

**解决方案**: 使用正确的认证参数

```python
# ❌ 错误
payload = {
    "app": {
        "appid": APP_ID,
        "token": ACCESS_TOKEN
    }
}

# ✅ 正确
payload = {
    "app": {
        "appid": APP_ID,
        "token": ACCESS_TOKEN,
        "cluster": "volcano_tts",
        "resource_id": "volc.service_type.10029"  # 必须有
    }
}
```

**教训**: TTS API 认证复杂，建议使用 SDK 封装

---

### 坑 9：TTS WebSocket 连接问题

**问题**: WebSocket 连接需要正确的 header 和帧格式，websockets 库版本兼容性问题

**现象**:
```
BaseEventLoop.create_connection() got an unexpected keyword argument 'extra_headers'
```

**解决方案 A**: 使用微软 Edge TTS（推荐⭐）

```bash
# 安装
pip install edge-tts --break-system-packages

# 生成配音
edge-tts --text "你的文案" --voice zh-CN-XiaoxiaoNeural --write-media narration.mp3
```

**优势**:
- ✅ 免费
- ✅ 高质量（微软 Azure 语音）
- ✅ 简单易用
- ✅ 无需认证

**常用音色**:
- `zh-CN-XiaoxiaoNeural` - 甜美女声（最常用）
- `zh-CN-YunxiNeural` - 成熟男声
- `zh-CN-XiaoyiNeural` - 活泼女声

**解决方案 B**: 使用火山引擎 HTTP SSE 端点

```python
url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"
params = {
    "access_token": ACCESS_TOKEN,
    "app_id": APP_ID,
    "resource_id": "seed-tts-1.0",
    "voice_type": "zh_female_uranus_bigtts",
    "text": text
}
```

**教训**: 优先使用 Edge TTS，简单可靠

---

### 坑 10：视频自带 BGM，需要替换为人声

**问题**: 生成的视频已有背景音乐，需要去掉并替换为 TTS 配音

**解决方案**: 使用 FFmpeg 替换音频轨道

```bash
# 1. 生成 TTS 配音
edge-tts --text "文案" --voice zh-CN-XiaoxiaoNeural --write-media narration.mp3

# 2. 替换视频音频（去掉原 BGM，添加人声）
ffmpeg -i video.mp4 -i narration.mp3 \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 \
  -shortest \
  video_with_narration.mp4
```

**参数说明**:
- `-c:v copy`: 视频流直接复制（不重新编码）
- `-c:a aac`: 音频重新编码为 AAC
- `-map 0:v:0`: 使用第一个文件的视频
- `-map 1:a:0`: 使用第二个文件的音频
- `-shortest`: 以较短的流为准（避免音画不同步）

**如需保留 BGM + 添加人声**:
```bash
# 混合原音频和 TTS（调整音量比例）
ffmpeg -i video.mp4 -i narration.mp3 \
  -filter_complex "[0:a]volume=0.3[a];[a][1:a]amix=inputs=2:duration=first" \
  -c:v copy -c:a aac \
  video_mixed.mp4
```

**教训**: 先用 FFmpeg 检查视频是否有音频轨道，再决定处理方式

---

## 视频拼接相关

### 坑 11：FFmpeg 拼接需要文件列表

**问题**: 直接拼接多个视频文件会报错

**解决方案**: 创建文件列表

```bash
# 创建 concat_list.txt
file 'scene_1.mp4'
file 'scene_2.mp4'
file 'scene_3.mp4'
file 'scene_4.mp4'
file 'scene_5.mp4'

# 使用 FFmpeg 拼接
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy output.mp4
```

**关键点**:
- `-f concat`: 指定拼接模式
- `-safe 0`: 允许相对路径
- `-c copy`: 直接复制流（不重新编码）

**教训**: 使用 FFmpeg concat demuxer，不要用 concat 滤镜

---

### 坑 12：视频时间戳问题

**问题**: 拼接时出现 `Non-monotonic DTS` 警告

**现象**:
```
[mp4 @ 0x...] Non-monotonic DTS in output stream 0:1
```

**解决方案**: 忽略警告（不影响输出），或重新编码

```bash
# 方法 1: 直接复制（有警告但可用）
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# 方法 2: 重新编码（无警告但慢）
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

**教训**: 警告可以忽略，不影响最终视频

---

## 文件管理相关

### 坑 13：文件路径混乱

**问题**: 项目文件散落在不同目录

**解决方案**: 建立清晰的目录结构

```
project_001/
├── frame1-6.jpeg          # 关键帧
├── scene_v2_1-5.mp4       # 视频片段
├── video_final.mp4        # 最终输出
├── tasks.json             # 任务 ID 记录
├── concat_v2.txt          # FFmpeg 列表
└── 进度报告.md            # 项目文档
```

**教训**: 每个项目独立目录，避免文件混乱

---

### 坑 14：未保存任务 ID

**问题**: 生成过程中断后无法恢复

**解决方案**: 每次提交任务后立即保存

```python
import json

task_ids = []
for scene in scenes:
    task_id = submit_task(...)
    task_ids.append({'scene': i, 'task_id': task_id})
    
    # 立即保存
    with open('tasks.json', 'w') as f:
        json.dump(task_ids, f, indent=2)
```

**教训**: 重要信息及时持久化

---

## 音频处理相关

### 坑 15：视频自带 BGM 需要处理

**问题**: 火山引擎生成的视频自带背景音乐，需要决定是否保留

**解决方案**:

**方案 A: 完全替换为人声**（适合知识分享类）
```bash
ffmpeg -i video.mp4 -i narration.mp3 \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 \
  -shortest \
  output.mp4
```

**方案 B: 混合 BGM+ 人声**（保留氛围）
```bash
ffmpeg -i video.mp4 -i narration.mp3 \
  -filter_complex "[0:a]volume=0.3[a];[a][1:a]amix=inputs=2" \
  -c:v copy -c:a aac \
  output.mp4
```

**教训**: 先检查视频是否有音频轨道，根据视频类型决定处理方式

---

### 最佳实践总结

### 1. API 调用

```python
# ✅ 标准流程
1. 使用用户端点 ID（ep-xxx）
2. 首尾帧格式：image_url 嵌套对象 + role 参数
3. 文本参数放最后：prompt + --wm + --dur
4. 提交后立即保存 task_id
5. 轮询检查状态（10 秒间隔）
6. 成功后立即下载视频
```

### 2. 图片生成

```python
# ✅ 标准流程
1. 使用 2K 尺寸
2. 生成后立即下载
3. 检查文件大小（>100KB 为正常）
4. 保存 URL 到 JSON 记录
```

### 3. 视频拼接

```python
# ✅ 标准流程
1. 创建 FFmpeg 列表文件
2. 使用 -f concat -safe 0 -c copy
3. 忽略 Non-monotonic DTS 警告
4. 检查输出文件大小和时长
```

### 4. 错误处理

```python
# ✅ 标准流程
try:
    result = api_call()
except Exception as e:
    error_msg = str(e)[:150]  # 限制长度
    log_error(error_msg)
    # 记录到 tasks.json
    task['error'] = error_msg
```

---

## 📚 相关文档

- [项目完整档案](项目完整档案.md)
- [README](README.md)
- [SKILL](SKILL.md)
- [MAINTENANCE_GUIDE](MAINTENANCE_GUIDE.md)

---

**最后更新**: 2026-03-23  
**维护者**: 扛枪 / 小咪
