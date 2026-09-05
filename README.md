# PackCheck — Packaged Commodity Compliance & Consumer Awareness System

An AI-driven compliance verification and consumer awareness platform designed for the **Smart India Hackathon (SIH)**. The system enables consumers and regulatory officers to scan or upload product packaging labels, extracts text via OCR, parses mandatory legal declarations under Legal Metrology / Packaged Commodities rules, and provides an instant compliance audit score with actionable recommendations.

---

## 🚀 Key Features

- 📸 **Image Upload & Optical Character Recognition (OCR):**
  - Preprocesses label images using OpenCV (grayscale, adaptive thresholding, bilateral filtering).
  - High-accuracy text extraction powered by Tesseract OCR engine.
- ⚖️ **Packaged Commodity Compliance Engine:**
  - Automated rule-checking against statutory declarations (Product Name, Net Quantity, MRP, Manufacturing/Expiry Dates, Manufacturer/Packer Address, Customer Care, Country of Origin, Ingredients, etc.).
  - Calculates an overall compliance score (0–100%) with categorized status (`PASS`, `WARNING`, `FAIL`).
  - Highlights missing declarations and provides legal recommendations.
- 📋 **Manual Entry & Verification:**
  - Fallback manual form allowing users to input label details for instant compliance scoring.
- 🖨️ **Compliance Audit Dashboard & Reporting:**
  - Dynamic score ring visualization.
  - Full tabbed breakdown of compliance rules, extracted product attributes, and raw OCR output.
  - One-click print-ready audit reports for inspectors and consumers.
- 🎨 **Modern Responsive UI:**
  - Glassmorphic dark theme, responsive grid layouts, micro-animations, and clean typography.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask, REST API
- **Computer Vision & OCR:** OpenCV, Tesseract OCR (`pytesseract`), Pillow
- **Frontend:** HTML5, CSS3 (Modern Glassmorphism Design System), Vanilla JavaScript
- **Database:** MySQL (with connection pooling and graceful offline fallback)
- **Configuration:** python-dotenv

---

## 📁 Project Structure

```
├── backend/
│   ├── app.py                   # Flask Application entry point & blueprint registration
│   ├── config.py                # Environment and app configuration
│   ├── database/
│   │   ├── db.py                # MySQL connection pool with fallback
│   │   └── schema.sql           # Database schema definition
│   ├── modules/
│   │   ├── compliance_engine.py # Rules evaluation & scoring algorithm
│   │   ├── image_processing.py  # OpenCV preprocessing pipeline
│   │   ├── ocr.py               # Tesseract text extraction & path resolver
│   │   ├── product_parser.py    # Regex & NLP pattern matching for product fields
│   │   └── report_generator.py  # Report aggregation logic
│   ├── routes/
│   │   ├── main.py              # Landing page and static routes
│   │   └── scan.py              # API endpoints for image upload, OCR & compliance
│   ├── rules/
│   │   └── commodity_rules.json # Statutory compliance rules definition
│   └── uploads/                 # Temporary storage for uploaded product labels
├── frontend/
│   ├── static/
│   │   ├── css/style.css        # Custom CSS design system
│   │   └── js/app.js            # Client-side interactions
│   └── templates/
│       ├── base.html            # Common layout & navigation
│       ├── index.html           # Landing page
│       ├── scan.html            # Label upload & scanning interface
│       ├── result.html          # Compliance report dashboard
│       └── about.html           # Project background & legal framework
├── .env.example                 # Sample environment variables
├── .gitignore                   # Git ignore rules
└── requirements.txt             # Python dependencies
```

---

## ⚡ Quickstart & Setup

### 1. Prerequisites

- **Python 3.10+**
- **Tesseract OCR**:
  - macOS: `brew install tesseract`
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - Windows: Download installer from UB-Mannheim Tesseract repo

### 2. Clone and Setup Environment

```bash
# Clone the repository
git clone https://github.com/GunjanPatil-cloud/sih-packaged-commodity-compliance.git
cd sih-packaged-commodity-compliance

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` if you wish to configure MySQL credentials or port settings (default port is `5001`).

### 4. Run the Application

```bash
python backend/app.py
```

Open your browser and visit:
```
http://localhost:5001
```

---

## 📄 License
Open-source under the MIT License. Developed for Smart India Hackathon (SIH).
