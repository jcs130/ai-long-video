# Project 002: 一拳超人 vs 鸣人 战力分析

**时长**: 2 分 10 秒  
**场景数**: 10  
**成本**: ~20 元  
**状态**: ✅ 完成

---

## 📋 项目信息

| 指标 | 数值 |
|------|------|
| 视频时长 | 2 分 10 秒 (130 秒) |
| 场景数量 | 10 |
| 关键帧 | 20 张 (1920x1920) |
| 视频片段 | 10 段 × 12 秒 |
| 字幕数量 | 11 条 |
| TTS 字数 | 537 字 |
| 文件大小 | 15MB |
| API 成本 | ~20 元 |

---

## 📁 文件说明

- `脚本_一拳超人 vs 鸣人.md`: 完整脚本（10 场景，537 字）
- `generate_srt.py`: SRT 字幕生成脚本
- `generate_tts_correct.py`: TTS 配音生成（**正确 API 格式**）
- `subtitles.srt`: 字幕文件（11 条）
- `narration.mp3`: TTS 配音（749KB，小何 2.0）
- `video_final.mp4`: 最终视频（15MB）

---

## 🚀 使用方法

### 1. 生成字幕

```bash
python3 generate_srt.py
```

输出：`subtitles.srt` (11 条字幕)

### 2. 生成 TTS 配音

```bash
python3 generate_tts_correct.py
```

输出：`narration.mp3` (749KB, 36 秒)

**注意**: 使用正确的 API 格式：
```python
payload = {
    "user": {"uid": "user_001"},
    "req_params": {
        "speaker": "zh_female_xiaohe_uranus_bigtts",
        "text": text,
        "audio_params": {"format": "mp3", "sample_rate": 24000}
    }
}
```

### 3. 合并视频

```bash
# 假设有 video_merged.mp4（10 段视频已合并）
ffmpeg -i video_merged.mp4 -i narration.mp3 \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest \
  video_final.mp4
```

### 4. 添加字幕（可选）

```bash
ffmpeg -i video_merged.mp4 \
  -vf "subtitles=subtitles.srt:force_style='Fontsize=28,PrimaryColour=&H00FFFF,BackColour=&H80000000'" \
  -c:a copy video_with_subs.mp4
```

---

## 📜 脚本概览

| 场景 | 时长 | 内容 | 台词 |
|------|------|------|------|
| 0. 开场 | 10s | 标题 + 剪影对峙 | "如果一拳超人埼玉遇到火影忍者鸣人，谁会赢？" |
| 1. 力量 | 12s | 拳头碰撞特效 | "埼玉老师能一拳打爆地球，力量没有上限" |
| 2. 速度 | 12s | 残影移动效果 | "埼玉能从月球跳回地球只需几秒" |
| 3. 防御 | 12s | 能量护盾对比 | "埼玉承受过波罗斯的崩星咆哮炮" |
| 4. 技能 | 12s | 技能展示 | "鸣人有影分身、螺旋丸、尾兽玉" |
| 5. 经验 | 12s | 战斗回忆 | "鸣人从小战斗到大，经验丰富" |
| 6. 耐力 | 12s | 持久战示意 | "鸣人能连续战斗几天几夜" |
| 7. 成长 | 12s | 成长时间线 | "鸣人从吊车尾到火影，成长惊人" |
| 8. 评估 | 12s | 数据对比图表 | "埼玉在硬实力上全面领先" |
| 9. 结论 | 12s | 结论 + 结尾 | "如果纯战力对决，埼玉胜" |

---

## ⚠️ 踩坑记录

### #21: TTS API 格式错误导致 resource ID mismatch

**问题**: TTS 生成一直返回错误：`resource ID is mismatched with speaker related resource`

**原因**: 使用了复杂的 API 格式：
```python
# ❌ 错误
payload = {
    "audio": {"voice_type": "..."},
    "request": {"text": "...", "service_instance": "..."}
}
```

**解决**: 改用简化格式：
```python
# ✅ 正确
payload = {
    "user": {"uid": "user_001"},
    "req_params": {
        "speaker": "zh_female_xiaohe_uranus_bigtts",
        "text": text,
        "audio_params": {"format": "mp3", "sample_rate": 24000}
    }
}
```

### #22: 关键帧角色描述太抽象导致生成错误角色

**问题**: 生成的关键帧不是埼玉和鸣人，是其他动漫角色

**原因**: prompt 太抽象：`"两人剪影对峙，拳头碰撞特效"`

**解决**: 具体描述：
```
"左侧：光头黄色战衣的埼玉（一拳超人），
右侧：金色头发橙色服装的鸣人（火影忍者），
两人拳头碰撞，能量爆炸特效"
```

**关键**: 包含角色名 + 作品名 + 外观特征（发型、服装颜色）

### #23: 阿里云盘上传 API 返回 201 也是成功

**问题**: 上传脚本检查 `status_code == 200`，但 API 返回 201

**解决**: 检查 `status_code in [200, 201]`

---

## 📊 成本分析

| 项目 | 数量 | 单价 | 小计 |
|------|------|------|------|
| 图片生成 | 20 张 | 0.15 元/张 | 3 元 |
| 视频生成 | 10 段×12 秒 | 1.5 元/秒 | 18 元 |
| TTS 配音 | 537 字 | 免费额度内 | 0 元 |
| **合计** | | | **21 元** |

---

## 🎯 技术要点

### 首尾帧控制
```python
video.generate_from_first_last_frames(
    first_frame_path="frame1.jpg",
    last_frame_path="frame2.jpg",
    prompt="流畅的动作过渡，能量爆炸特效",
    model="ep-20260227022253-b67vh",  # 视频端点 ID
    duration=12
)
```

### 角色一致性技巧
- 包含角色名 + 作品名：`埼玉（一拳超人）`
- 描述外观特征：`光头黄色战衣`
- 可以加英文名：`Saitama (One-Punch Man)`

### TTS 推荐音色
- `zh_female_xiaohe_uranus_bigtts` - 小何 2.0（知性女声，知识分享）
- `zh_female_linjianvhai_uranus_bigtts` - 邻家女孩 2.0（亲切女声）
- `zh_female_liuchangnv_uranus_bigtts` - 流畅女声 2.0（流畅解说）

---

## 📹 输出文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `video_merged.mp4` | 69MB | 合并原版（无字幕无配音） |
| `video_with_subs.mp4` | 18MB | 加字幕版 |
| `video_final.mp4` | 15MB | 最终版（字幕 + 配音） |

---

## 🔗 相关链接

- [主项目 README](../../README.md)
- [踩坑指南](../../TROUBLESHOOTING.md)
- [技能文档](../../SKILL.md)

---

*最后更新：2026-03-26*
