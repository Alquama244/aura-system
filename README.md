# AURA: Autonomous Unified Reasoning & Automation

AURA is an intelligent visual inventory management system combining real-time computer vision object detection with LLM reasoning.

## Tech Stack
- **Frontend & UI:** Streamlit
- **Computer Vision:** YOLOv8 (`ultralytics`)
- **Generative AI:** Google Gemini API (`google-genai` SDK with multi-model failover & retry logic)
- **Database:** SQLite (`aura_inventory.db`)
- **Export Formats:** Pandas (`openpyxl` Excel) & ReportLab (PDF)

## System Architecture
1. **Visual Processing**: Images are processed via YOLOv8 to identify and count visual items.
2. **AI Analysis**: Detected counts are sent to the Gemini API using dynamic retry and failover routing to generate structured operational insights.
3. **Storage & Reporting**: Scan metrics and narratives are logged to SQLite, with one-click PDF and Excel report exports.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aura-system