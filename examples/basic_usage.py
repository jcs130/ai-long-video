#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础使用示例 - AI 一致性视频生成

演示：
1. 文生视频
2. 首帧生视频
3. 首尾帧生视频（核心功能）
"""

import sys
import os

# 添加 SDK 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from volc_video_sdk import VolcVideoSDK

# 配置 API Key（从环境变量读取）
# 使用前请设置：export VOLC_API_KEY="your-api-key-here"
API_KEY = os.getenv("VOLC_API_KEY")
if not API_KEY:
    raise ValueError("请设置 VOLC_API_KEY 环境变量")

def main():
    # 初始化 SDK
    sdk = VolcVideoSDK(api_key=API_KEY)
    
    print("=" * 60)
    print("AI 一致性视频生成 - 基础示例")
    print("=" * 60)
    
    # 示例 1: 文生视频
    print("\n📹 示例 1: 文生视频")
    print("-" * 60)
    try:
        video1 = sdk.generate(
            prompt="一只小猫在草地上奔跑，阳光明媚，4K 画质",
            duration=5,
            watermark=False
        )
        print(f"✅ 文生视频成功")
        print(f"   视频 URL: {video1.get('video_url', 'N/A')}")
        print(f"   时长：{video1.get('duration', 'N/A')}秒")
    except Exception as e:
        print(f"❌ 失败：{e}")
    
    # 示例 2: 首帧生视频
    print("\n📹 示例 2: 首帧生视频")
    print("-" * 60)
    print("⚠️  需要准备首帧图片：first_frame.jpg")
    # 实际使用时取消注释
    # video2 = sdk.generate_from_first_frame(
    #     first_frame_path="first_frame.jpg",
    #     prompt="图片中的场景开始动态变化",
    #     duration=5
    # )
    
    # 示例 3: 首尾帧生视频（核心功能！）
    print("\n📹 示例 3: 首尾帧生视频 ⭐ 核心功能")
    print("-" * 60)
    print("⚠️  需要准备首帧和尾帧图片")
    print("   first_frame.jpg - 首帧（如公司 Logo）")
    print("   last_frame.jpg - 尾帧（如二维码）")
    print()
    print("代码示例:")
    print("""
    video3 = sdk.generate_from_first_last_frames(
        first_frame_path="logo.png",
        last_frame_path="qrcode.png",
        prompt="科技感粒子特效过渡，蓝色光效",
        duration=10,
        watermark=False
    )
    """)
    
    print("\n" + "=" * 60)
    print("💡 提示：")
    print("1. 首次使用需要开通火山引擎视频生成服务")
    print("2. API Key 在火山引擎控制台获取")
    print("3. 首尾帧功能适合企业宣传片、产品广告等场景")
    print("=" * 60)

if __name__ == "__main__":
    main()
