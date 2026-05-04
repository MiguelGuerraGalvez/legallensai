import os
from fastapi import FastAPI, Depends, File, UploadFile
import fitz
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.models_legales import ContratoFactory
import json
app = FastAPI(root_path="/api")

@app.get("/")
async def root():
    return {"hello": "Hello World!"}

@app.post("/")
async def recibe_pdf(archivo: UploadFile = File(...)):
    contenido = await archivo.read()
    texto = ""

    documento = fitz.open(stream=contenido, filetype="pdf")

    for pagina in documento:
        texto += pagina.get_text()
    
    documento.close()

    return {
        "archivo": archivo.filename,
        "contenido": texto
    }

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

system_msg = "Eres un experto en contratos legales en España, tu misión es realizar auditorías exhaustivas de " \
"contratos. Debes detectar si hay cláusulas abusivas, errores de forma y riesgos potenciales." \
"Además, es MUY IMPORTANTE que tu respuesta sea EXCLUSIVAMENTE un objeto JSON válido para que el sistema" \
"pueda procesarlo. No añadas introducciones ni despedidas."

prompt = ChatPromptTemplate.from_messages([
    ("system", system_msg),
    ("human", "Debes seguir estas instrucciones al pie de la letra: {instrucciones} " \
    "en este contrato: {contrato}\n RESPONDE ÚNICAMENTE EN ESTE FORMATO JSON: \n" \
    "{{\n" \
    "   \"puntos_clave\": [\"Lista de strings\"],\n" \
    "   \"banderas_rojas\": [\"Lista de strings con cláusulas abusivas o ilegales, si no hay DÉJA ESTE CAMPO EN BLANCO\"],\n" \
    "   \"riesgo_total\": [\"Bajo/Medio/Crítico\"],\n"
    "}}\n")
])

chain = prompt | llm

@app.post("/ia")
async def consulta_ia(datos: dict):
    tipo = datos["tipo"]
    archivo = datos["archivo"]
    texto = archivo

    try:
        contrato = ContratoFactory(tipo, texto)

        respuesta = chain.invoke({
            "instrucciones": contrato.obtener_prompt_especifico(),
            "contrato": texto
        })

        respuesta_limpia = respuesta.content.replace("```json", "").replace("```", "").strip()
        
        try:
            respuesta_json = json.loads(respuesta_limpia)
            return respuesta_json
        except json.JSONDecodeError:
            return {"Error": "La IA no devolvión un JSON válido", "Contenido": respuesta_limpia}
    
    except Exception as e:
        return {"Error": str(e)}
