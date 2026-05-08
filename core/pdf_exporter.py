"""PDF Export Module - Converts notes to PDF format"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import os


class PDFExporter:
    """Handles exporting notes to PDF format"""
    
    @staticmethod
    def export_note_to_pdf(content: str, title: str, output_path: str = None) -> str:
        """
        Export note content to PDF
        
        Args:
            content: Note content (plain text)
            title: Note title
            output_path: Optional output path (auto-generated if None)
            
        Returns:
            Path to created PDF file
        """
        if output_path is None:
            # Generate filename from title
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            output_path = f"{safe_title}.pdf"
        
        # Ensure .pdf extension
        if not output_path.lower().endswith('.pdf'):
            output_path += '.pdf'
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Get base styles
        styles = getSampleStyleSheet()
        
        # Custom title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#244235'),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold'
        )
        
        # Date style
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#8A9A95'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        # Body style
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        )
        
        # Add title
        story.append(Paragraph(title, title_style))
        
        # Add date
        current_date = datetime.now().strftime("%B %d, %Y at %H:%M")
        story.append(Paragraph(f"Exported on {current_date}", date_style))
        
        story.append(Spacer(1, 12))
        
        # Process content - handle line breaks and paragraphs
        lines = content.split('\n')
        paragraph_buffer = []
        
        for line in lines:
            line = line.rstrip()
            if line == "":
                # Empty line - flush paragraph buffer
                if paragraph_buffer:
                    paragraph_text = ' '.join(paragraph_buffer)
                    if paragraph_text:
                        story.append(Paragraph(paragraph_text, body_style))
                    paragraph_buffer = []
                story.append(Spacer(1, 6))
            else:
                # Add line to buffer
                paragraph_buffer.append(line)
        
        # Flush remaining paragraph
        if paragraph_buffer:
            paragraph_text = ' '.join(paragraph_buffer)
            if paragraph_text:
                story.append(Paragraph(paragraph_text, body_style))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    @staticmethod
    def export_to_desktop(content: str, title: str) -> str:
        """Export PDF to desktop with default name"""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        output_path = os.path.join(desktop, f"{safe_title}.pdf")
        
        return PDFExporter.export_note_to_pdf(content, title, output_path)
    
    @staticmethod
    def export_to_user_documents(content: str, title: str) -> str:
        """Export PDF to user Documents folder"""
        documents = os.path.join(os.path.expanduser("~"), "Documents")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        output_path = os.path.join(documents, f"Kairus_{safe_title}.pdf")
        
        return PDFExporter.export_note_to_pdf(content, title, output_path)