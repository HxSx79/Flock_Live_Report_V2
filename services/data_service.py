"""Production data handling service"""
import pandas as pd
from datetime import datetime
from models.production_line import ProductionLine

class DataService:
    def __init__(self):
        self.line1 = ProductionLine('line1')
        self.line2 = ProductionLine('line2')
        self.history = []
        
    def update_production(self, line_id, detections):
        """Update production based on detections"""
        line = self.line1 if line_id == 'line1' else self.line2
        # Process detections and update line data
        for detection in detections:
            if self._is_valid_part(detection['class']):
                line.add_production()
                
    def get_production_data(self):
        """Get current production data for all lines"""
        return {
            'line1': self._get_line_data(self.line1),
            'line2': self._get_line_data(self.line2),
            'totals': self._get_totals()
        }
        
    def _get_line_data(self, line):
        """Get data for a specific line"""
        return {
            'quantity': line.total_quantity,
            'scrap': line.scrap_count,
            'pph': round(line.parts_per_hour, 2),
            'current_part': line.current_part
        }
        
    def _get_totals(self):
        """Calculate totals across all lines"""
        total_quantity = self.line1.total_quantity + self.line2.total_quantity
        total_scrap = self.line1.scrap_count + self.line2.scrap_count
        return {
            'quantity': total_quantity,
            'scrap': total_scrap,
            'scrap_rate': round(total_scrap / total_quantity * 100 if total_quantity > 0 else 0, 2)
        }