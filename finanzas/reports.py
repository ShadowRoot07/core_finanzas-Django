from django.template.loader import render_to_string
from django.http import HttpResponse

def generar_pdf_finanzas(context):
    try:
        # IMPORTACIÓN LOCAL: Solo ocurre cuando se llama a esta función
        from weasyprint import HTML
        
        # Renderizamos el template
        html_string = render_to_string('finanzas/reporte_pdf.html', context)

        # Creamos la respuesta
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_financiero.pdf"'

        # Intentamos generar el PDF
        HTML(string=html_string).write_pdf(response)
        return response

    except (OSError, ImportError):
        # Si Vercel no tiene las librerías de C (Pango/Cairo), 
        # devolvemos un mensaje amigable en lugar de romper toda la app.
        return HttpResponse(
            "La generación de PDF no está disponible en este servidor (Faltan librerías de sistema). "
            "Por favor, usa la versión local con Docker para esta función.",
            status=503
        )

