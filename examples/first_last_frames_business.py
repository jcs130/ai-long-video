#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
首尾帧生成示例 - 商业级应用

演示如何使用首尾帧功能生成企业宣传片、产品广告等商业视频
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from volc_video_sdk import VolcVideoSDK

API_KEY = os.getenv("VOLC_API_KEY", "8d27bf88-53b0-4656-9946-f21934f4f24b")

def create_company_promo():
    """
    企业宣传片
    首帧：公司 Logo
    尾帧：联系方式 + 二维码
    """
    sdk = VolcVideoSDK(api_key=API_KEY)
    
    print("🎬 生成企业宣传片...")
    
    video = sdk.generate_from_first_last_frames(
        first_frame_path="examples/assets/company_logo.png",
        last_frame_path="examples/assets/contact_qrcode.png",
        prompt="科技感蓝色粒子特效，光线流动，专业大气，商业级质感",
        duration=10,
        watermark=False
    )
    
    print(f"✅ 企业宣传片生成成功")
    print(f"   视频 URL: {video['video_url']}")
    print(f"   建议售价：500-2000 元")
    return video

def create_product_ad():
    """
    产品广告
    首帧：产品特写
    尾帧：购买链接 + 优惠信息
    """
    sdk = VolcVideoSDK(api_key=API_KEY)
    
    print("\n🎬 生成产品广告...")
    
    video = sdk.generate_from_first_last_frames(
        first_frame_path="examples/assets/product.jpg",
        last_frame_path="examples/assets/buy_link.png",
        prompt="产品展示，360 度旋转，光影效果，高端质感",
        duration=10,
        watermark=False
    )
    
    print(f"✅ 产品广告生成成功")
    print(f"   视频 URL: {video['video_url']}")
    print(f"   建议售价：300-1000 元")
    return video

def create_course_promo():
    """
    课程推广
    首帧：讲师照片 + 课程标题
    尾帧：报名二维码
    """
    sdk = VolcVideoSDK(api_key=API_KEY)
    
    print("\n🎬 生成课程推广视频...")
    
    video = sdk.generate_from_first_last_frames(
        first_frame_path="examples/assets/instructor.jpg",
        last_frame_path="examples/assets/enroll_qrcode.png",
        prompt="教育风格，温暖光线，知识传播感",
        duration=10,
        watermark=False
    )
    
    print(f"✅ 课程推广视频生成成功")
    print(f"   视频 URL: {video['video_url']}")
    print(f"   建议售价：200-800 元")
    return video

if __name__ == "__main__":
    print("=" * 60)
    print("首尾帧生成 - 商业应用示例")
    print("=" * 60)
    
    # 注意：实际运行需要准备图片文件
    print("\n⚠️  运行前需要准备以下图片:")
    print("   - company_logo.png (公司 Logo)")
    print("   - contact_qrcode.png (联系方式二维码)")
    print("   - product.jpg (产品图片)")
    print("   - buy_link.png (购买链接)")
    print("   - instructor.jpg (讲师照片)")
    print("   - enroll_qrcode.png (报名二维码)")
    
    print("\n💡 提示:")
    print("   1. 可以先用示例图片测试")
    print("   2. 替换为客户真实图片即可商用")
    print("   3. 建议售价仅供参考，可根据市场调整")
    
    # 实际调用（需要准备图片）
    # create_company_promo()
    # create_product_ad()
    # create_course_promo()
