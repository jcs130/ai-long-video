#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成 TTS 配音 - 使用正确的参数
"""

import requests
import json

# 配置 - 来自 MEMORY.md
APP_ID = "3019120872"
ACCESS_TOKEN = "qcdGrSiKz8_8qTkHo1whQREW48QPWT6I"
RESOURCE_ID = "seed-tts-2.0"  # 2.0 模型
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
    print("重新生成 TTS 配音 - 正确参数")
    print("=" * 60)
    
    char_count = len(SCRIPT)
    print(f"\n📝 脚本字数：{char_count} 字符")
    
    # API 端点
    url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"
    
    headers = {
        "X-Api-App-Id": APP_ID,
        "X-Api-Access-Key": ACCESS_TOKEN,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Content-Type": "application/json"
    }
    
    # 使用 SERVICE_INSTANCE 参数
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
            "reqid": "req_003",
            "text": SCRIPT,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson",
            "service_instance": SERVICE_INSTANCE
        }
    }
    
    print(f"\n🔊 Resource ID: {RESOURCE_ID}")
    print(f"🔊 Service Instance: {SERVICE_INSTANCE}")
    print(f"🔊 Voice: zh_female_xiaohe_uranus_bigtts")
    print("\n正在生成 TTS...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        print(f"\nHTTP 状态码：{response.status_code}")
        
        # 检查响应内容
        content = response.content
        print(f"响应大小：{len(content)} bytes")
        
        # 如果是 SSE 格式，解析
        if b'event:' in content:
            print("\n⚠️ 收到 SSE 格式响应，解析中...")
            lines = content.decode('utf-8', errors='ignore').split('\n')
            audio_data = b''
            for line in lines:
                if line.startswith('data:'):
                    try:
                        data = json.loads(line[5:].strip())
                        if 'data' in data and isinstance(data['data'], str):
                            # Base64 解码
                            import base64
                            audio_data += base64.b64decode(data['data'])
                    except:
                        pass
            
            if audio_data:
                output_path = "/home/jcs130/.copaw/workspaces/64cKss/media/project_002/narration_fixed.mp3"
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                
                print(f"✅ TTS 生成成功！")
                print(f"📁 保存位置：{output_path}")
                print(f"📊 文件大小：{len(audio_data) / 1024:.1f} KB")
                return output_path
            else:
                print("❌ 无法解析音频数据")
                print(f"原始响应前 500 字符：{content[:500]}")
                return None
        elif response.status_code == 200:
            # 直接是 MP3 数据
            output_path = "/home/jcs130/.copaw/workspaces/64cKss/media/project_002/narration_fixed.mp3"
            with open(output_path, "wb") as f:
                f.write(content)
            
            print(f"✅ TTS 生成成功！")
            print(f"📁 保存位置：{output_path}")
            print(f"📊 文件大小：{len(content) / 1024:.1f} KB")
            return output_path
        else:
            print(f"❌ 生成失败：{response.status_code}")
            print(f"响应内容：{content[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_tts()
