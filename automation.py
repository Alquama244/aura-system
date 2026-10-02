from detector import ObjectDetector
from database import DatabaseManager
from ai_engine import AIEngine
from report_generator import ReportGenerator
import os

class AuraAutomationWorkflow:
    def __init__(self):
        self.detector = ObjectDetector()
        self.db = DatabaseManager()
        self.ai = AIEngine()
        self.reporter = ReportGenerator()

    def run_pipeline(self, image_path):
        # Step 1: Detect objects & count using YOLO
        annotated_image, object_counts = self.detector.detect_objects(image_path)
        
        # Step 2: Generate AI analysis text
        ai_analysis = self.ai.generate_analysis(object_counts)
        
        # Step 3: Save results to SQLite database
        image_name = os.path.basename(image_path)
        self.db.save_record(image_name, object_counts, ai_analysis)
        
        # Step 4: Generate Excel spreadsheet report
        excel_path = self.reporter.create_excel_report(object_counts)
        
        return annotated_image, object_counts, ai_analysis, excel_path