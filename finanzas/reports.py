from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

def generar_pdf_finanzas(context):
    # Renderizamos un template HTML específico para el PDF
    html_string = render_to_string('finanzas/reporte_pdf.html', context)
    
    # Creamos la respuesta con WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_financiero.pdf"'
    
    HTML(string=html_string).write_pdf(response)
    return response

