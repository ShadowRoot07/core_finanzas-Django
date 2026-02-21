from django.shortcuts import render, redirect
from .services import calcular_resumen_financiero
from .models import Transaccion
from .forms import TransaccionForm
from .services import calcular_resumen_financiero, get_gastos_por_categoria

def dashboard(request):
    resumen = calcular_resumen_financiero()
    transacciones = Transaccion.objects.all()[:10]
    
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigimos para evitar que el formulario se envíe dos veces al refrescar
            return redirect('dashboard') 
    else:
        form = TransaccionForm() 
    
    context = {
        'resumen': calcular_resumen_financiero(),
        'transacciones': Transaccion.objects.all().order_by('-fecha')[:10],
        'gastos_por_categoria': get_gastos_por_categoria(),
        'form': form,
    }
    return render(request, 'finanzas/dashboard.html', context)
