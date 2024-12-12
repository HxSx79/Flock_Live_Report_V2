"""Production line data model"""
from datetime import datetime, timedelta
import pandas as pd

class ProductionLine:
    def __init__(self, line_id):
        self.line_id = line_id
        self.current_shift_start = None
        self.total_quantity = 0
        self.scrap_count = 0
        self.parts_per_hour = 0
        self.current_part = None
        
    def reset_shift(self):
        """Reset shift counters"""
        self.total_quantity = 0
        self.scrap_count = 0
        self.current_shift_start = datetime.now()
        
    def add_production(self, quantity=1):
        """Add produced parts"""
        self.total_quantity += quantity
        self._calculate_pph()
        
    def add_scrap(self, quantity=1):
        """Add scrapped parts"""
        self.scrap_count += quantity
        
    def _calculate_pph(self):
        """Calculate current parts per hour"""
        if self.current_shift_start:
            hours_elapsed = (datetime.now() - self.current_shift_start).total_seconds() / 3600
            self.parts_per_hour = self.total_quantity / hours_elapsed if hours_elapsed > 0 else 0