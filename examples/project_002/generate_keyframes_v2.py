#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成关键帧 - 一拳超人 vs 鸣人
使用火山引擎 SDK
"""

import sys
sys.path.insert(0, '/home/jcs130/.copaw/active_skills')

from volc_multimedia_sdk import VolcImage
import os
import time

# 配置
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"
MODEL = "ep-20260227121917-j9vll"  # Seedream-5.0-lite

OUTPUT_DIR = "/home/jcs130/.copaw/workspaces/64cKss/media/project_002/keyframes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 20 个关键帧提示词（剪影风格，避免版权）
PROMPTS = [
    # 场景 0: 开场
    ("00_start", "Anime title screen, bold Chinese text '一拳超人 VS 火影', dark background with orange and yellow energy explosion effects, cinematic dramatic lighting, high quality anime art, 960x960"),
    ("00_end", "Two warrior silhouettes facing each other on cliff, one wearing yellow cape flowing in wind, one in orange outfit with headband, dramatic sunset background, energy aura surrounding both, anime confrontation scene, 960x960"),
    
    # 场景 1: 力量对比
    ("01_power_start", "Close-up of anime fist clenching, glowing with intense orange energy, power gathering, sparks and lightning around fist, dramatic shadows, 960x960"),
    ("01_power_end", "Massive energy explosion from fist collision, huge shockwave spreading outward, ground cracking and debris flying, epic anime battle impact scene, 960x960"),
    
    # 场景 2: 速度对比
    ("02_speed_start", "Anime silhouette in sprinting stance, motion blur lines, wind swirling around, leaves flying, showing extreme speed, dynamic angle, 960x960"),
    ("02_speed_end", "Multiple afterimages of running figure creating trail across screen, speed lines everywhere, showing teleportation-level velocity, anime action scene, 960x960"),
    
    # 场景 3: 防御能力
    ("03_defense_start", "Glowing energy barrier shield surrounding silhouette, orange hexagonal pattern barrier, protective aura, anime defensive stance, 960x960"),
    ("03_defense_end", "Powerful energy beam hitting barrier shield, massive impact explosion, shield holding strong with cracks of light, sparks flying everywhere, anime defense scene, 960x960"),
    
    # 场景 4: 特殊能力
    ("04_ability_start", "Blue spiraling energy ball forming in hand, swirling chakra-like energy, glowing orb with lightning, anime jutsu technique, 960x960"),
    ("04_ability_end", "Serious punch with massive yellow energy beam trail, devastating attack, air splitting from power, epic anime strike scene, 960x960"),
    
    # 场景 5: 战斗经验
    ("05_exp_start", "Young ninja silhouette training alone at sunset, practicing basic moves, determination posture, anime flashback style, warm lighting, 960x960"),
    ("05_exp_end", "Mature warrior silhouette standing confidently, battle-worn appearance, experienced fighter aura, night sky with stars, anime veteran scene, 960x960"),
    
    # 场景 6: 耐力对比
    ("06_stamina_start", "Two fighters facing each other at beginning of battle, energy auras visible, sunset golden hour, anime tournament scene, 960x960"),
    ("06_stamina_end", "Same two fighters still standing after long battle, night sky with full moon, both exhausted but determined, anime endurance battle, 960x960"),
    
    # 场景 7: 成长潜力
    ("07_growth_start", "Timeline infographic, small silhouette at left starting point, arrow pointing right showing growth path, anime style chart, 960x960"),
    ("07_growth_end", "Silhouette at peak form glowing with maximum golden power, radiant aura, reached ultimate level, anime powerup transformation, 960x960"),
    
    # 场景 8: 综合评估
    ("08_analysis_start", "Radar chart comparison graphic showing five stats, two colored areas in orange and yellow, overlapping comparison, anime infographic, 960x960"),
    ("08_analysis_end", "Large question mark in center, two fighter silhouettes on left and right sides, thinking atmosphere, question marks floating, anime analysis scene, 960x960"),
    
    # 场景 9: 结尾
    ("09_end_start", "Two fighters standing respectfully after battle, fists touching in mutual respect, sunset background, anime rivalry respect scene, 960x960"),
    ("09_end_end", "End screen with large Chinese text '你支持谁？', comment bubble icon, thumbs up icon, anime outro style, call to action, 960x960"),
]

def main():
    print("=" * 60)
    print("生成关键帧 - 一拳超人 vs 鸣人")
    print("=" * 60)
    
    img = VolcImage(api_key=API_KEY)
    
    total = len(PROMPTS)
    success = 0
    
    for i, (name, prompt) in enumerate(PROMPTS):
        output_path = f"{OUTPUT_DIR}/{name}.png"
        
        print(f"\n[{i+1}/{total}] 生成：{name}")
        print(f"  提示词：{prompt[:80]}...")
        
        try:
            result = img.generate(
                prompt=prompt,
                size="1920x1920",
                model=MODEL,
                watermark=False
            )
            
            if result and 'urls' in result and len(result['urls']) > 0:
                # 下载图片
                img_url = result['urls'][0]
                import requests
                img_data = requests.get(img_url, timeout=60).content
                
                with open(output_path, "wb") as f:
                    f.write(img_data)
                
                print(f"  ✅ 成功：{output_path}")
                success += 1
            else:
                print(f"  ❌ 失败：{result}")
            
        except Exception as e:
            print(f"  ❌ 错误：{e}")
        
        # 避免限流
        if i < total - 1:
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"完成！成功：{success}/{total}")
    print("=" * 60)

if __name__ == "__main__":
    main()
