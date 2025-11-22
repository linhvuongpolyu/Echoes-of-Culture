import json
import os
from pathlib import Path

class StarModel:
    def __init__(self):
        # Place data file in data folder at project root
        self.project_root = Path(__file__).parent.parent.parent
        self.data_file = self.project_root / "data" / "stars.json"
        self.data_file.parent.mkdir(exist_ok=True)
        self._ensure_default_data()
    
    def _ensure_default_data(self):
        """Ensure the data file exists with a default structure"""
        if not self.data_file.exists():
            default_data = {
                'Hong Kong': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
                'China': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
                'Vietnam': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
            }
            self._save_data(default_data)
    
    def _load_data(self):
        """Load data"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load data: {e}")
            return {}
    
    def _save_data(self, data):
        """Save data"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save data: {e}")
            return False
    
    def update_stars(self, region, activity, stars):
        """Update star count"""
        data = self._load_data()
        
        # Ensure region exists
        if region not in data:
            data[region] = {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
        
        # Update star count
        data[region][activity] = stars
        
        success = self._save_data(data)
        return success
    
    def get_stars(self, region=None):
        """Get star data"""
        data = self._load_data()
        
        if region:
            return data.get(region, {})
        else:
            return data
    
    def get_total_stars(self, region=None):
        """Get total star count"""
        data = self._load_data()
        
        if region:
            region_data = data.get(region, {})
            return sum(region_data.values())
        else:
            total = 0
            for region_data in data.values():
                total += sum(region_data.values())
            return total
    
    def reset_stars(self):
        """Reset all star data"""
        default_data = {
            'Hong Kong': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
            'China': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
            'Vietnam': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
        }
        return self._save_data(default_data)