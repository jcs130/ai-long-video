#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 TTS 配音 - 简化版（完全按照 SKILL.md）
"""

import requests
import json
import base64

# 配置
APP_ID = "3019120872"
ACCESS_TOKEN = "qcdGrSiKz8_8qTkHo1whQREW48QPWT6I"
RESOURCE_ID = "seed-tts-2.0"

# 脚本
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
    url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"
    
    headers = {
        "X-Api-App-Id": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Content-Type": "application/json"
    }
    
    # 简化版 payload（完全按照 SKILL.md）
    payload = {
        "user": {"uid": "user_001"},
        "req_params": {
            "speaker": "zh_female_xiaohe_uranus_bigtts",
            "text": text,
            "audio_params": {"format": "mp3", "sample_rate": 24000}
        }
    }
    
    print(f"📝 脚本字数：{len(text)}")
    print(f"🎤 音色：zh_female_xiaohe_uranus_bigtts")
    print(f"📤 发送请求...")
    
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
    
    print(f"📥 响应状态码：{response.status_code}")
    
    audio_data = b""
    count = 0
    
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8', errors='ignore')
            count += 1
            if count <= 5:
                print(f"   行{count}: {line_str[:100]}...")
            
            if line_str.startswith('data:'):
                try:
                    event = json.loads(line_str[5:])
                    if 'data' in event and event['data']:
                        audio_data += base64.b64decode(event['data'])
                    elif 'code' in event:
                        print(f"⚠️ 错误码：{event.get('code')} - {event.get('message')}")
                except Exception as e:
                    print(f"⚠️ 解析错误：{e}")
    
    print(f"\n📊 处理行数：{count}")
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
    generate_tts(SCRIPT, "narration.mp3")
