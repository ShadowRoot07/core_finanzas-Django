from django.shortcuts import render, redirect
from .services import calcular_resumen_financiero
from .models import Transaccion
from .forms import TransaccionForm

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
        'resumen': resumen,
        'transacciones': transacciones,
        'form': form, # Pasamos el formulario al template
    }
    return render(request, 'finanzas/dashboard.html', context)

