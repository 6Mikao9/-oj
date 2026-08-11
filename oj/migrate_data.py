#!/usr/bin/env python3
"""迁移题目数据，添加收藏和批注字段"""

import json
import os
from pathlib import Path

def migrate_problems():
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    data_dir = base_dir / "data" / "years"
    
    if not data_dir.exists():
        print("No data directory found!")
        return
    
    updated_count = 0
    
    for year_dir in data_dir.iterdir():
        if not year_dir.is_dir():
            continue
        
        for prob_file in year_dir.glob("*.json"):
            with open(prob_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 添加新字段（如果不存在）
            modified = False
            if 'is_favorite' not in data:
                data['is_favorite'] = False
                modified = True
            if 'annotation' not in data:
                data['annotation'] = ""
                modified = True
            
            if modified:
                with open(prob_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                updated_count += 1
                print(f"Updated: {prob_file}")
    
    print(f"\nMigration complete! Updated {updated_count} problem(s).")

if __name__ == "__main__":
    migrate_problems()
