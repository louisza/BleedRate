"""PDF Export Service for tax calculation reports"""
from io import BytesIO
from datetime import datetime
from typing import Dict
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.pdfgen import canvas


class PDFExporter:
    """Generate professional PDF reports of tax calculations"""
    
    # Constants
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]
    LEFT_MARGIN = 1.5 * cm
    RIGHT_MARGIN = 1.5 * cm
    TOP_MARGIN = 1.5 * cm
    BOTTOM_MARGIN = 1.5 * cm
    
    # Colors
    BLEEDRATE_BLUE = HexColor("#003D7A")
    BLEEDRATE_LIGHT = HexColor("#E8EFF5")
    ACCENT_COLOR = HexColor("#F39C12")
    TEXT_DARK = HexColor("#2C3E50")
    TABLE_HEADER_BG = BLEEDRATE_BLUE
    TABLE_HEADER_TEXT = white
    TABLE_ALT_ROW = HexColor("#F8F9FA")
    
    def __init__(self):
        """Initialize PDF exporter"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom Paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.BLEEDRATE_BLUE,
            spaceAfter=10,
            alignment=1,  # Center
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.TEXT_DARK,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=white,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Normal text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=self.TEXT_DARK,
            spaceAfter=4,
            leading=12
        ))
        
        # Small disclaimer
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['BodyText'],
            fontSize=8,
            textColor=HexColor("#7F8C8D"),
            spaceAfter=2,
            leading=10,
            alignment=0  # Left
        ))
    
    def generate_pdf(self, calculation_data: dict) -> bytes:
        """Generate PDF report from calculation data
        
        Args:
            calculation_data: Dictionary containing:
                - personal: PersonalProfile data
                - breakdown: Tax breakdown dict
                - total: Total tax amount
                - effective_rate_vs_gross: Effective tax rate %
                - timestamp: Optional datetime (defaults to now)
        
        Returns:
            PDF as bytes
        """
        # Extract data
        personal = calculation_data.get('personal', {})
        breakdown = calculation_data.get('breakdown', {})
        total = calculation_data.get('total', 0.0)
        effective_rate = calculation_data.get('effective_rate_vs_gross', 0.0)
        timestamp = calculation_data.get('timestamp', datetime.now())
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=self.LEFT_MARGIN,
            rightMargin=self.RIGHT_MARGIN,
            topMargin=self.TOP_MARGIN,
            bottomMargin=self.BOTTOM_MARGIN,
            title="BleedRate - Tax Calculation Report"
        )
        
        # Build story (content)
        story = []
        
        # Header
        story.append(Paragraph("BleedRate", self.styles['CustomTitle']))
        story.append(Paragraph("South African Tax Footprint Calculator", self.styles['CustomBody']))
        story.append(Spacer(1, 0.5 * cm))
        
        # Timestamp and reference
        if isinstance(timestamp, datetime):
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_str = str(timestamp)
        
        story.append(Paragraph(
            f"<b>Report Generated:</b> {timestamp_str}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.8 * cm))
        
        # Section 1: Your Profile
        story.append(self._build_profile_section(personal))
        story.append(Spacer(1, 0.5 * cm))
        
        # Section 2: Tax Summary
        story.append(self._build_summary_section(total, effective_rate, personal))
        story.append(Spacer(1, 0.5 * cm))
        
        # Section 3: Tax Breakdown
        story.append(self._build_breakdown_section(breakdown))
        story.append(Spacer(1, 0.8 * cm))
        
        # Footer: Disclaimer
        story.append(self._build_disclaimer_section())
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        buffer.seek(0)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _build_profile_section(self, personal: dict) -> Table:
        """Build the profile/input section"""
        annual_salary = personal.get('annual_salary', 0)
        annual_bonus = personal.get('annual_bonus', 0)
        age = personal.get('age', 0)
        medical_members = personal.get('medical_members', 0)
        
        gross_income = annual_salary + annual_bonus
        
        data = [
            [
                Paragraph("<b>Your Profile</b>", self.styles['SectionHeader']),
                "",
                ""
            ],
            [
                Paragraph("Annual Salary:", self.styles['CustomBody']),
                Paragraph(self._format_currency(annual_salary), self.styles['CustomBody']),
                ""
            ],
            [
                Paragraph("Annual Bonus:", self.styles['CustomBody']),
                Paragraph(self._format_currency(annual_bonus), self.styles['CustomBody']),
                ""
            ],
            [
                Paragraph("<b>Gross Income:</b>", self.styles['CustomBody']),
                Paragraph(f"<b>{self._format_currency(gross_income)}</b>", self.styles['CustomBody']),
                ""
            ],
            [
                Paragraph("Age:", self.styles['CustomBody']),
                Paragraph(str(age), self.styles['CustomBody']),
                ""
            ],
            [
                Paragraph("Medical Aid Members:", self.styles['CustomBody']),
                Paragraph(str(medical_members), self.styles['CustomBody']),
                ""
            ],
        ]
        
        table = Table(data, colWidths=[4 * cm, 3 * cm, 2 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (2, 0), self.TABLE_HEADER_BG),
            ('TEXTCOLOR', (0, 0), (2, 0), self.TABLE_HEADER_TEXT),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (2, 0), 10),
            ('BOTTOMPADDING', (0, 0), (2, 0), 8),
            ('TOPPADDING', (0, 0), (2, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#DDDDDD")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, self.TABLE_ALT_ROW]),
            ('PADDING', (0, 1), (-1, -1), 5),
        ]))
        
        return table
    
    def _build_summary_section(self, total: float, effective_rate: float, personal: dict) -> Table:
        """Build the summary section"""
        gross_income = personal.get('annual_salary', 0) + personal.get('annual_bonus', 0)
        monthly_total = total / 12 if total else 0
        
        # Format effective rate
        effective_rate_str = f"{effective_rate:.2f}%" if effective_rate else "0.00%"
        
        data = [
            [
                Paragraph("<b>Tax Summary</b>", self.styles['SectionHeader']),
                "",
                ""
            ],
            [
                Paragraph("<b>Total Tax to Government (Annual):</b>", self.styles['CustomBody']),
                Paragraph(f"<b>{self._format_currency(total)}</b>", self.styles['CustomBody']),
                ""
            ],
            [
                Paragraph("Total Tax to Government (Monthly):", self.styles['CustomBody']),
                Paragraph(self._format_currency(monthly_total), self.styles['CustomBody']),
                ""
            ],
            [
                Paragraph("<b>Effective Tax Rate:</b>", self.styles['CustomBody']),
                Paragraph(f"<b>{effective_rate_str}</b>", self.styles['CustomBody']),
                ""
            ],
            [
                Paragraph("Percentage of Gross Income:", self.styles['CustomBody']),
                Paragraph(f"{(total/gross_income*100):.1f}% of {self._format_currency(gross_income)}", self.styles['CustomBody']),
                ""
            ],
        ]
        
        table = Table(data, colWidths=[4 * cm, 3 * cm, 2 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (2, 0), self.ACCENT_COLOR),
            ('TEXTCOLOR', (0, 0), (2, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (2, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (2, 0), 10),
            ('BOTTOMPADDING', (0, 0), (2, 0), 8),
            ('TOPPADDING', (0, 0), (2, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#DDDDDD")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, self.TABLE_ALT_ROW]),
            ('PADDING', (0, 1), (-1, -1), 5),
        ]))
        
        return table
    
    def _build_breakdown_section(self, breakdown: dict) -> Table:
        """Build the detailed tax breakdown section"""
        # Sort breakdown by amount (descending)
        sorted_items = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
        
        # Header row
        data = [
            [
                Paragraph("<b>Tax Category</b>", self.styles['SectionHeader']),
                Paragraph("<b>Annual Amount</b>", self.styles['SectionHeader']),
                Paragraph("<b>Monthly Amount</b>", self.styles['SectionHeader']),
                Paragraph("<b>% of Total</b>", self.styles['SectionHeader']),
            ]
        ]
        
        total = sum(breakdown.values())
        
        # Data rows
        for category, amount in sorted_items:
            monthly = amount / 12
            percentage = (amount / total * 100) if total > 0 else 0
            
            data.append([
                Paragraph(category, self.styles['CustomBody']),
                Paragraph(self._format_currency(amount), self.styles['CustomBody']),
                Paragraph(self._format_currency(monthly), self.styles['CustomBody']),
                Paragraph(f"{percentage:.1f}%", self.styles['CustomBody']),
            ])
        
        # Total row
        data.append([
            Paragraph("<b>TOTAL</b>", self.styles['CustomBody']),
            Paragraph(f"<b>{self._format_currency(total)}</b>", self.styles['CustomBody']),
            Paragraph(f"<b>{self._format_currency(total/12)}</b>", self.styles['CustomBody']),
            Paragraph("<b>100.0%</b>", self.styles['CustomBody']),
        ])
        
        table = Table(data, colWidths=[5.5 * cm, 3 * cm, 3 * cm, 2 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.TABLE_HEADER_BG),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.TABLE_HEADER_TEXT),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#DDDDDD")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [white, self.TABLE_ALT_ROW]),
            ('BACKGROUND', (0, -1), (-1, -1), self.BLEEDRATE_LIGHT),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('TOPPADDING', (0, -1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 6),
            ('PADDING', (0, 1), (-1, -1), 5),
        ]))
        
        return table
    
    def _build_disclaimer_section(self) -> Paragraph:
        """Build the disclaimer section"""
        disclaimer_text = (
            "<b>IMPORTANT DISCLAIMER:</b> This report is provided for information purposes only and does not constitute "
            "professional tax advice. The calculations in this report are based on the tax rates and regulations as of the "
            "calculation date. Tax laws change frequently, and individual circumstances may affect your actual tax liability. "
            "<br/><br/>"
            "You should consult with a qualified tax professional, chartered accountant, or tax advisor to understand your "
            "specific tax obligations and to receive personalized tax planning advice. BleedRate does not provide licensed "
            "tax advisory services and cannot be held responsible for any decisions made based on this report."
            "<br/><br/>"
            "<i>BleedRate - Understand your tax footprint. Always consult a qualified tax professional.</i>"
        )
        
        return Paragraph(disclaimer_text, self.styles['Disclaimer'])
    
    def _format_currency(self, amount: float) -> str:
        """Format amount as South African Rand"""
        # Handle negative numbers
        if amount < 0:
            sign = "-"
            amount = abs(amount)
        else:
            sign = ""
        
        # Format with thousands separator and 2 decimal places
        formatted = f"{amount:,.2f}"
        
        return f"{sign}R {formatted}"
