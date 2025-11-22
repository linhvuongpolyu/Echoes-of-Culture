# frontend/utils/star_manager.py
"""Simple star management using JSON file storage - no API needed"""
import json
from pathlib import Path
import streamlit as st

class StarManager:
    """Manages star data using JSON file storage"""
    
    def __init__(self):
        # Data file in project root
        self.project_root = Path(__file__).parent.parent.parent
        self.data_file = self.project_root / "data" / "stars.json"
        self.data_file.parent.mkdir(exist_ok=True)
        self._ensure_default_data()
    
    def _ensure_default_data(self):
        """Ensure data file exists with default structure"""
        if not self.data_file.exists():
            default_data = {
                'Hong Kong': {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
                'China': {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
                'Vietnam': {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
            }
            self._save_data(default_data)
    
    def _load_data(self):
        """Load star data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Failed to load star data: {e}")
            return self._get_default_data()
    
    def _save_data(self, data):
        """Save star data to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            st.error(f"Failed to save star data: {e}")
            return False
    
    def _get_default_data(self):
        """Get default data structure"""
        return {
            'Hong Kong': {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
            'China': {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
            'Vietnam': {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
        }
    
    def update_stars(self, region, activity, stars):
        """Update star count for a specific region and activity"""
        data = self._load_data()
        
        # Ensure region exists
        if region not in data:
            data[region] = {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
        
        # Update star count
        data[region][activity] = min(max(0, stars), 3)  # Clamp between 0-3
        
        success = self._save_data(data)
        return success
    
    def get_stars(self, region=None):
        """Get star data for a specific region or all regions"""
        data = self._load_data()
        
        if region:
            return data.get(region, {'Language': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0})
        else:
            return data
    
    def get_total_stars(self, region=None):
        """Get total star count for a region or all regions"""
        data = self._load_data()
        
        if region:
            region_data = data.get(region, {})
            return sum(region_data.values())
        else:
            total = 0
            for region_data in data.values():
                total += sum(region_data.values())
            return total
    
    def get_overall_stats(self):
        """Get overall statistics"""
        data = self._load_data()
        total_stars = sum(sum(region.values()) for region in data.values())
        max_total_stars = 36  # 3 regions * 4 activities * 3 stars each
        
        return {
            'all_stars': data,
            'total_stars': total_stars,
            'max_total_stars': max_total_stars
        }
    
    def display_stars(self, count, max_stars=3):
        """Display star visualization"""
        return "⭐" * count + "☆" * (max_stars - count)


# Create global instance
star_manager = StarManager()

