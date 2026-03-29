# ⚙️ Configuration Guide

## Modifying Local Paths

Paths in example code need to be adjusted for your environment:

### 1. Modify sys.path
```python
# ❌ Don't use (my local path)
sys.path.insert(0, '/home/jcs130/.copaw/active_skills')

# ✅ Use your path instead
sys.path.insert(0, '/your/path/to/active_skills')

# Or use relative path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### 2. Modify Working Directory
```python
# ❌ Don't use (my local path)
WORK_DIR = Path("/home/jcs130/.copaw/workspaces/64cKss/media/project_003")

# ✅ Use your path
WORK_DIR = Path("./media/project_003")  # Relative path
# or
WORK_DIR = Path("/your/work/dir/media/project_003")  # Absolute path
```

### 3. Modify API Key
```python
# ❌ Don't hardcode (my API key is revoked)
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"

# ✅ Use environment variable
import os
API_KEY = os.getenv("ARK_API_KEY")
```

### 4. Quick Modification Commands
```bash
# Batch replace paths (Linux/Mac)
find . -name "*.py" -type f -exec sed -i '' 's|/home/jcs130|/your/path|g' {} \;

# Or manually edit config file
cp config.example.py config.py
# Then edit config.py with your paths
```

## Recommended Directory Structure

```
your_project/
├── active_skills/          # Skills directory
│   ├── volc_video_sdk.py
│   ├── volc_image_sdk.py
│   └── short_video_production/
├── media/                  # Media files
│   ├── project_001/
│   ├── project_002/
│   └── project_003/
├── examples/               # Example code
│   └── project_003_v2/
└── config.py              # Config file (fill in your paths)
```

## Configuration File Example

```python
# config.py
import os
from pathlib import Path

# API Configuration
ARK_API_KEY = os.getenv("ARK_API_KEY", "your-api-key-here")

# TTS Configuration
TTS_APP_ID = "3019120872"
TTS_ACCESS_KEY = "your-access-key"
TTS_RESOURCE_ID = "seed-tts-2.0"

# Path Configuration
BASE_DIR = Path(__file__).parent
ACTIVE_SKILLS_DIR = BASE_DIR / "active_skills"
MEDIA_DIR = BASE_DIR / "media"

# Project Paths
PROJECT_003_DIR = MEDIA_DIR / "project_003"
```

---

*Note: Paths in example code are for reference only. Please modify according to your actual environment.*
