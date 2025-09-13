from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import os

class HealthReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF report"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2563eb')
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#1f2937')
        )
        
        # Risk level styles
        self.risk_styles = {
            'Low': colors.HexColor('#10b981'),
            'Moderate': colors.HexColor('#f59e0b'),
            'High': colors.HexColor('#ef4444'),
            'Very High': colors.HexColor('#dc2626')
        }
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT
        )
    
    def generate_report(self, prediction_data, user_data=None):
        """Generate a comprehensive health assessment PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build the story (content)
        story = []
        
        # Header
        story.extend(self._build_header())
        
        # Patient Information (if provided)
        if user_data:
            story.extend(self._build_patient_info(user_data))
        
        # Assessment Results
        story.extend(self._build_assessment_results(prediction_data))
        
        # Risk Analysis
        story.extend(self._build_risk_analysis(prediction_data))
        
        # Recommendations
        story.extend(self._build_recommendations(prediction_data))
        
        # Footer
        story.extend(self._build_footer())
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _build_header(self):
        """Build the report header"""
        story = []
        
        # Title
        title = Paragraph("Health Assessment Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_para = Paragraph(f"<b>Report Generated:</b> {date_str}", self.body_style)
        story.append(date_para)
        story.append(Spacer(1, 30))
        
        return story
    
    def _build_patient_info(self, user_data):
        """Build patient information section"""
        story = []
        
        story.append(Paragraph("Patient Information", self.subtitle_style))
        
        # Create patient info table
        patient_data = []
        if 'age' in user_data:
            patient_data.append(['Age:', f"{user_data['age']} years"])
        if 'gender' in user_data:
            gender_text = 'Male' if user_data['gender'] == 1 else 'Female'
            patient_data.append(['Gender:', gender_text])
        if 'bmi' in user_data:
            patient_data.append(['BMI:', f"{user_data['bmi']:.1f}"])
        
        if patient_data:
            table = Table(patient_data, colWidths=[2*inch, 3*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(table)
        
        story.append(Spacer(1, 30))
        return story
    
    def _build_assessment_results(self, prediction_data):
        """Build assessment results section"""
        story = []
        
        story.append(Paragraph("Assessment Results", self.subtitle_style))
        
        # Predictor type
        predictor_name = prediction_data.get('predictor_type', 'Unknown').replace('_', ' ').title()
        story.append(Paragraph(f"<b>Assessment Type:</b> {predictor_name}", self.body_style))
        
        # Risk score and level
        risk_score = prediction_data.get('risk_score', 0)
        risk_level = prediction_data.get('risk_level', 'Unknown')
        confidence = prediction_data.get('confidence', 0)
        
        # Create results table
        results_data = [
            ['Risk Score:', f"{risk_score:.2%}"],
            ['Risk Level:', risk_level],
            ['Confidence:', f"{confidence:.1%}"]
        ]
        
        table = Table(results_data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (1, 1), (1, 1), self.risk_styles.get(risk_level, colors.black)),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
        ]))
        story.append(table)
        story.append(Spacer(1, 30))
        
        return story
    
    def _build_risk_analysis(self, prediction_data):
        """Build risk analysis section"""
        story = []
        
        story.append(Paragraph("Risk Analysis", self.subtitle_style))
        
        risk_level = prediction_data.get('risk_level', 'Unknown')
        risk_score = prediction_data.get('risk_score', 0)
        
        # Risk interpretation
        risk_interpretation = self._get_risk_interpretation(risk_level, risk_score)
        story.append(Paragraph(risk_interpretation, self.body_style))
        
        story.append(Spacer(1, 20))
        return story
    
    def _build_recommendations(self, prediction_data):
        """Build recommendations section"""
        story = []
        
        story.append(Paragraph("Recommendations", self.subtitle_style))
        
        recommendations = prediction_data.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                rec_para = Paragraph(f"{i}. {rec}", self.body_style)
                story.append(rec_para)
        else:
            story.append(Paragraph("No specific recommendations available.", self.body_style))
        
        story.append(Spacer(1, 30))
        return story
    
    def _build_footer(self):
        """Build report footer"""
        story = []
        
        # Disclaimer
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        disclaimer_text = (
            "<b>IMPORTANT DISCLAIMER:</b> This report is for informational purposes only and should not "
            "replace professional medical advice, diagnosis, or treatment. Always consult with a qualified "
            "healthcare provider regarding any health concerns or before making any decisions related to your health."
        )
        
        story.append(Spacer(1, 40))
        story.append(Paragraph(disclaimer_text, disclaimer_style))
        
        return story
    
    def _get_risk_interpretation(self, risk_level, risk_score):
        """Get risk level interpretation text"""
        interpretations = {
            'Low': f"Your risk score of {risk_score:.1%} indicates a low risk level. This suggests that based on the assessed factors, you have a relatively low likelihood of developing the condition. Continue maintaining healthy lifestyle habits.",
            'Moderate': f"Your risk score of {risk_score:.1%} indicates a moderate risk level. While not immediately concerning, this suggests you should pay attention to risk factors and consider preventive measures.",
            'High': f"Your risk score of {risk_score:.1%} indicates a high risk level. This suggests you should take proactive steps to address risk factors and consult with healthcare professionals for proper evaluation and management.",
            'Very High': f"Your risk score of {risk_score:.1%} indicates a very high risk level. This requires immediate attention and professional medical consultation for proper assessment and intervention."
        }
        
        return interpretations.get(risk_level, f"Your risk score is {risk_score:.1%}. Please consult with a healthcare professional for proper interpretation.")