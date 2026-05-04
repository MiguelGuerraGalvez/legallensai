from django.contrib import admin, messages
from app.models import Auditoria
from django.utils import timezone
from collections import Counter
from django.utils.html import format_html

# Register your models here.
@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo', 'riesgo_total', 'fecha')

    list_filter = ('tipo', 'riesgo_total', 'fecha')

    search_fields = ('cliente', 'nombre_archivo')

    ordering = ('-fecha',)

    readonly_fields = ('puntos_clave', 'banderas_rojas', 'riesgo_total', 'fecha', 'creador')

    def changelist_view(self, request, extra_context = None):
        hoy = timezone.now().date()
        analizados_hoy = Auditoria.objects.filter(fecha__date=hoy).count()

        listas_todas = Auditoria.objects.values_list('banderas_rojas', flat=True)
        
        trampas_todas = []
        for lista in listas_todas:
            if lista:
                trampas_todas.extend(lista)
        
        conteo = Counter(trampas_todas).most_common(3)
        trampas_comunes = " | ".join([f"{t}\n" for t, c in conteo]) if conteo else "Ninguna trampa es cómún."

        vista_html = format_html (
            "<b>Hoy se han analizado {} contratos. </b> <br>"
            "<b>TRAMPAS MÁS COMUNES:</b> <br> <span style='color: #d9534f;'> {}",
            analizados_hoy,
            trampas_comunes
        )
        
        self.message_user(request, vista_html, messages.INFO)

        return super().changelist_view(request, extra_context)
