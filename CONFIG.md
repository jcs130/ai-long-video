# 📝 配置说明

## 修改本地路径

示例代码中的路径需要根据你的实际环境修改：

### 1. 修改 sys.path
```python
# ❌ 不要使用（我的本地路径）
sys.path.insert(0, '/home/jcs130/.copaw/active_skills')

# ✅ 改为你的路径
sys.path.insert(0, '/your/path/to/active_skills')

# 或者使用相对路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### 2. 修改工作目录
```python
# ❌ 不要使用（我的本地路径）
WORK_DIR = Path("/home/jcs130/.copaw/workspaces/64cKss/media/project_003")

# ✅ 改为你的路径
WORK_DIR = Path("./media/project_003")  # 相对路径
# 或
WORK_DIR = Path("/your/work/dir/media/project_003")  # 绝对路径
```

### 3. 修改 API Key
```python
# ❌ 不要硬编码（我的 API Key 已失效）
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"

# ✅ 使用环境变量
import os
API_KEY = os.getenv("ARK_API_KEY")
```

### 4. 快速修改命令
```bash
# 批量替换路径（Linux/Mac）
find . -name "*.py" -type f -exec sed -i '' 's|/home/jcs130|/your/path|g' {} \;

# 或者手动编辑配置文件
cp config.example.py config.py
# 然后编辑 config.py 填入你的路径
```

## 推荐目录结构

```
your_project/
├── active_skills/          # 技能目录
│   ├── volc_video_sdk.py
│   ├── volc_image_sdk.py
│   └── short_video_production/
├── media/                  # 媒体文件
│   ├── project_001/
│   ├── project_002/
│   └── project_003/
├── examples/               # 示例代码
│   └── project_003_v2/
└── config.py              # 配置文件（填入你的路径）
```

## 配置文件示例

```python
# config.py
import os
from pathlib import Path

# API 配置
ARK_API_KEY = os.getenv("ARK_API_KEY", "your-api-key-here")

# TTS 配置
TTS_APP_ID = "3019120872"
TTS_ACCESS_KEY = "your-access-key"
TTS_RESOURCE_ID = "seed-tts-2.0"

# 路径配置
BASE_DIR = Path(__file__).parent
ACTIVE_SKILLS_DIR = BASE_DIR / "active_skills"
MEDIA_DIR = BASE_DIR / "media"

# 项目路径
PROJECT_003_DIR = MEDIA_DIR / "project_003"
```

---

*提示：示例代码中的路径仅供参考，请根据你的实际环境修改*
