#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 TTS 配音 - 使用正确的 API 格式（来自 short_video_production SKILL.md）
"""

import requests
import json
import base64

# 配置 - 来自 MEMORY.md
APP_ID = "3019120872"
ACCESS_TOKEN = "qcdGrSiKz8_8qTkHo1whQREW48QPWT6I"
RESOURCE_ID = "seed-tts-2.0"  # 2.0 模型

# 完整脚本
SCRIPT = """如果一拳超人埼玉遇到火影忍者鸣人，谁会赢？今天我们从五个维度深度分析这场跨次元对决！

先看力量。埼玉老师能一拳打爆地球，力量没有上限。鸣人尾兽化后能撼动大地，但还在可测量范围。这一轮，埼玉完胜。

速度方面，埼玉能从月球跳回地球只需几秒，速度远超光速。鸣人虽然快，但还在音速级别。埼玉再次领先。

防御力，埼玉承受过波罗斯的崩星咆哮炮，毫发无伤。鸣人有九尾查克拉外衣，能挡普通攻击，但面对星球级攻击，难说。

特殊能力，鸣人有影分身、螺旋丸、尾兽玉，技能丰富。埼玉只有普通拳和认真系列。但问题是，他的普通拳已经够用了。

战斗经验，鸣人从小战斗到大，经验丰富。埼玉说自己是兴趣使然的英雄，但每次都是一拳结束，没什么技术含量。

耐力方面，鸣人能连续战斗几天几夜，查克拉量大。埼玉没人见过他累。可能这就是无敌的代价吧。

成长潜力，鸣人从吊车尾到火影，成长惊人。埼玉他已经没有成长空间了，因为已经是天花板。

综合来看，埼玉在硬实力上全面领先，但鸣人的战术和羁绊之力不可小觑。不过，这真的重要吗？

结论，如果纯战力对决，埼玉胜。但动漫的魅力不在于谁强谁弱，而在于角色的成长和故事。所以，这个问题没有标准答案。

你觉得谁能赢？评论区告诉我！关注我，下期分析更多跨次元对决！"""

def generate_tts(text, output_path="narration.mp3"):
    """使用正确的 API 格式生成 TTS"""
    
    url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"
    
    headers = {
        "X-Api-App-Id": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Content-Type": "application/json"
    }
    
    # 正确的 payload 格式（来自 SKILL.md）
    payload = {
        "app": {
            "appid": APP_ID,
            "token": "access_token",
            "cluster": "volcano_tts"
        },
        "user": {
            "uid": "user_001"
        },
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
    print(f"🔗 端点：{url}")
    print(f"📤 发送请求...")
    
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
    
    print(f"📥 响应状态码：{response.status_code}")
    
    audio_data = b""
    error_messages = []
    
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8', errors='ignore')
            if line_str.startswith('data:'):
                try:
                    event = json.loads(line_str[5:])
                    # 调试：打印事件结构
                    if 'data' in event and event['data'] is not None:
                        audio_data += base64.b64decode(event['data'])
                    elif 'error' in event or 'code' in event:
                        error_messages.append(event)
                        print(f"⚠️ 错误事件：{event}")
                    else:
                        print(f"⚠️ 未知事件格式：{event}")
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON 解析错误：{e}")
                    print(f"   原始数据：{line_str[:200]}")
    
    if error_messages:
        print(f"❌ 错误信息：{error_messages}")
        return None
    
    if len(audio_data) < 1000:  # 小于 1KB 肯定是错误
        print(f"❌ 音频数据过小：{len(audio_data)} bytes，可能是错误响应")
        return None
    
    with open(output_path, 'wb') as f:
        f.write(audio_data)
    
    print(f"✅ TTS 生成完成：{output_path}")
    print(f"📊 文件大小：{len(audio_data) / 1024:.1f} KB")
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("生成 TTS 配音 - 正确的 API 格式")
    print("=" * 60)
    generate_tts(SCRIPT, "narration.mp3")
