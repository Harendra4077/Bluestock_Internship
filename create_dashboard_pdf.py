
"""
Create Dashboard.pdf from the 4 dashboard preview images
"""
from pathlib import Path
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def create_dashboard_pdf():
    dashboard_dir = Path(__file__).parent / "reports" / "dashboard_preview"
    image_files = [
        "page1_industry_overview.png",
        "page2_fund_performance.png",
        "page3_investor_analytics.png",
        "page4_sip_market_trends.png"
    ]

    # Create PDF in landscape mode to fit the wide dashboard pages
    pdf_path = Path(__file__).parent / "Dashboard.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=landscape(A4))
    page_width, page_height = landscape(A4)

    for img_file in image_files:
        img_path = dashboard_dir / img_file
        if not img_path.exists():
            print(f"Warning: {img_file} not found, skipping")
            continue

        # Open image and get dimensions
        img = Image.open(img_path)
        img_width, img_height = img.size

        # Calculate scaling to fit on A4 landscape page, maintaining aspect ratio
        width_ratio = page_width / img_width
        height_ratio = page_height / img_height
        scale = min(width_ratio, height_ratio) * 0.95  # 95% of page to leave margins
        scaled_width = img_width * scale
        scaled_height = img_height * scale

        # Center image on page
        x = (page_width - scaled_width) / 2
        y = (page_height - scaled_height) / 2

        # Draw image on PDF
        c.drawImage(
            ImageReader(img),
            x, y,
            width=scaled_width,
            height=scaled_height,
            preserveAspectRatio=True
        )

        c.showPage()

    c.save()
    print(f"✅ Dashboard.pdf created at {pdf_path}")


if __name__ == "__main__":
    create_dashboard_pdf()
