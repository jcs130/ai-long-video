#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成 TTS 配音 - 修复资源 ID 问题
"""

import requests
import json

# 配置 - 使用正确的资源 ID
APP_ID = "3019120872"
ACCESS_TOKEN = "qcdGrSiKz8_8qTkHo1whQREW48QPWT6I"
# 小何 2.0 对应的资源 ID 应该是 seed-tts 而不是 seed-tts-2.0
RESOURCE_ID = "seed-tts"  # 改用普通资源 ID
SERVICE_INSTANCE = "BigTTS2000000634074326722"

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

def generate_tts():
    print("=" * 60)
    print("重新生成 TTS 配音")
    print("=" * 60)
    
    char_count = len(SCRIPT)
    print(f"\n📝 脚本字数：{char_count} 字符")
    print(f"⏱️ 预计时长：{char_count / 4:.1f} 秒")
    
    # API 端点
    url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"
    
    headers = {
        "X-Api-App-Id": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Content-Type": "application/json"
    }
    
    # 使用小何语音（非 2.0 版本）
    payload = {
        "app": {
            "appid": APP_ID,
            "token": "access_token",
            "cluster": "volcano_tts"
        },
        "user": {
            "uid": "user_123"
        },
        "audio": {
            "voice_type": "zh_female_xiaohe_uranus_bigtts",
            "encoding": "mp3",
            "compression_rate": 1,
            "rate": 24000,
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0
        },
        "request": {
            "reqid": "req_002",
            "text": SCRIPT,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"
        }
    }
    
    print(f"\n🔊 使用资源 ID: {RESOURCE_ID}")
    print(f"🔊 使用语音：zh_female_xiaohe_uranus_bigtts")
    print("\n正在生成 TTS...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        print(f"\nHTTP 状态码：{response.status_code}")
        
        if response.status_code == 200:
            output_path = "/home/jcs130/.copaw/workspaces/64cKss/media/project_002/narration_new.mp3"
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ TTS 生成成功！")
            print(f"📁 保存位置：{output_path}")
            print(f"📊 文件大小：{file_size / 1024:.1f} KB")
            
            # 检查是否是有效 MP3
            if response.content[:3] == b'\xff\xfb' or response.content[:3] == b'\xff\xf3':
                print("✅ 验证：有效的 MP3 文件")
            else:
                print(f"⚠️ 警告：文件头不是标准 MP3 格式")
                print(f"   前 100 字节：{response.content[:100]}")
            
            return output_path
        else:
            print(f"❌ 生成失败：{response.status_code}")
            print(f"响应内容：{response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None

if __name__ == "__main__":
    generate_tts()
