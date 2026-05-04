from abc import ABC,abstractmethod
from pydantic import BaseModel

# 1. El "molde" para los datos que devuelve la IA
class AnalisisResultados(BaseModel):
    puntos_clave: list[str]
    banderas_rojas: list[str]
    riesgo_total: str # "Bajo", "Medio", "Crítico"

# 2. La Clase Abstracta (POO Pura)
class Contrato(ABC):
    def __init__(self, texto: str):
        self.texto = texto

    @abstractmethod
    def obtener_prompt_especifico(self) -> str:
        """Cada hijo dirá qué trampas buscar"""
        pass

    def ejecutar_auditoria(self, agente_ia) -> AnalisisResultados:
        # Lógica común: Se le pasa el prompt del hijo al Agente
        prompt = self.obtener_prompt_especifico()
        resultado = agente_ia.analizar(self.texto, prompt)
        return resultado
    
# 3. Implementaciones concretas
class ContratoAlquiler(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return "Busca si la fianza es legal (1 mes) y si el inquilino " \
        "paga averías estructurales"
    
class ContratoNDA(Contrato):
    def obtener_prompt_especifico(self) -> str:
        return "Busca si la duración es infinita y si la multa supera " \
        "los 100.000€."

def ContratoFactory(tipo: str, texto:str):
    tipos_contrato = {"alquiler": ContratoAlquiler, "nda": ContratoNDA}
    if tipo.lower() in tipos_contrato:
        contrato = tipos_contrato[tipo](texto)
    else:
        raise AttributeError("No existe ese tipo de contrato.")

    return contrato
