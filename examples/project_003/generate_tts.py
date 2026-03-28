#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 003: 木屋烧烤 - 生成 TTS 配音
使用火山引擎 TTS 2.0（小何 2.0 音色）
"""

import requests
import json
import base64

# 配置
APP_ID = "3019120872"
ACCESS_TOKEN = "qcdGrSiKz8_8qTkHo1whQREW48QPWT6I"
RESOURCE_ID = "seed-tts-2.0"

# 完整脚本（带停顿标记）
SCRIPT = """有人说，成年人的世界，没有容易二字。

但总有个地方，能让你卸下防备。

老张，这杯酒，敬咱们认识的第十年。

十年啊，还记得咱俩第一次来这儿吗？

怎么不记得，那时候咱俩兜里加起来不到 100 块。

哈哈，现在不也过来了？来，吃肉！

你说，啥叫日子？

日子啊，就是有人陪你吃肉，有人陪你扛事。

说得好！敬木屋，敬兄弟，敬这该死的生活！

木屋烧烤，有些话，有些肉，只和懂你的人分享。"""

def generate_tts(text, output_path="narration.mp3"):
    """使用正确的 API 格式生成 TTS"""
    
    url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"
    
    headers = {
        "X-Api-App-Id": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Content-Type": "application/json"
    }
    
    # 正确的 payload 格式（简化版）
    payload = {
        "user": {"uid": "user_001"},
        "req_params": {
            "speaker": "zh_female_xiaohe_uranus_bigtts",  # 小何 2.0
            "text": text,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000
            }
        }
    }
    
    print(f"📝 脚本字数：{len(text)}")
    print(f"🎤 音色：zh_female_xiaohe_uranus_bigtts (小何 2.0)")
    print(f"📤 发送请求...")
    
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
    
    print(f"📥 响应状态码：{response.status_code}")
    
    audio_data = b""
    
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8', errors='ignore')
            if line_str.startswith('data:'):
                try:
                    event = json.loads(line_str[5:])
                    if 'data' in event and event['data']:
                        audio_data += base64.b64decode(event['data'])
                except Exception as e:
                    pass
    
    print(f"📊 音频数据大小：{len(audio_data)} bytes")
    
    if len(audio_data) < 1000:
        print(f"❌ 音频数据过小，生成失败")
        return None
    
    with open(output_path, 'wb') as f:
        f.write(audio_data)
    
    print(f"✅ TTS 生成完成：{output_path} ({len(audio_data)/1024:.1f} KB)")
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("Project 003: 木屋烧烤 - 生成 TTS 配音")
    print("=" * 60)
    generate_tts(SCRIPT, "narration.mp3")
