from ..models.star_model import StarModel

class StarService:
    def __init__(self):
        self.star_model = StarModel()
    
    def update_stars(self, region, activity, stars):
        """Renew star count service"""
        return self.star_model.update_stars(region, activity, stars)
    
    def get_stars(self, region=None):
        """Get star data service"""
        return self.star_model.get_stars(region)
    
    def get_total_stars(self, region=None):
        """Get total star count service"""
        return self.star_model.get_total_stars(region)
    
    def get_region_progress(self, region):
        """Get region progress service"""
        stars = self.get_stars(region)
        total = self.get_total_stars(region)
        max_stars = 12  # 4 activities × 3 stars
        
        return {
            'region': region,
            'stars': stars,
            'total': total,
            'max_stars': max_stars,
            'progress_percentage': (total / max_stars) * 100 if max_stars > 0 else 0
        }
    
    def get_overall_progress(self):
        """Get overall progress service"""
        all_stars = self.get_stars()
        total_stars = self.get_total_stars()
        max_total_stars = 36  # 3 regions × 12 stars
        
        return {
            'all_stars': all_stars,
            'total_stars': total_stars,
            'max_total_stars': max_total_stars,
            'progress_percentage': (total_stars / max_total_stars) * 100 if max_total_stars > 0 else 0
        }
    
    def reset_all_stars(self):
        """Reset all stars service"""
        return self.star_model.reset_stars()

# Create a global service instance
star_service = StarService()