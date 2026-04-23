"""Escribe 3 variantes GENERICAS (A/B/C) en el Google Doc.

Sin personalizacion, sin lista de leads. Solo las 3 plantillas una vez cada una.
"""

from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT_FILE = ROOT / "recursos-ia" / "api-keys" / "google-sheets-service-account.json"

DOC_ID = "14vDGAzNyAlCtOwvBKNxk6-ZLjU2IwNWMUtzIS1DHZiY"

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


CONTENIDO = """OUTREACH MM AGENCY — 3 VARIANTES GENERICAS PARA TESTEAR

Objetivo: mandar A, B o C a cada lead (rotando) y ver cual convierte mas.
Flujo: IG DM + Email (dia 1) -> Llamada (dia 2).

============================================================

VARIANTE A — CASE STUDY DIRECTO

--- IG DM ---

Saludos,

Vi tu cuenta aqui en IG y me llamo la atencion tu trabajo.

Trabajo con MM Agency y hace poco armamos un embudo completo para una clinica medica aqui en RD (landing + trafico + seguimiento por WhatsApp) y en los ultimos 60 dias genero 85 pacientes interesados.

Si quieres que te muestre como funciona el sistema, podemos hablar 20 min sin costo.

¿Te mando el link para agendar?

Martin

--- EMAIL ---

Asunto: Sistema de captacion de pacientes

Hola,

Soy Martin Mercedes de MM Agency, especializados en captacion de pacientes para clinicas medicas en RD.

Te escribo porque hace poco armamos un embudo completo para una clinica medica aqui en el pais: landing, trafico pagado, CRM y seguimiento por WhatsApp.

En los ultimos 60 dias ese sistema genero 85 pacientes interesados reales.

Si te interesa ver como podriamos replicar algo asi para ti, te propongo una llamada de diagnostico de 20 min sin costo.

¿Te mando el link para agendar?

Martin Mercedes
MM Agency
WhatsApp +1 849-577-2978
mmagency.com.do

--- LLAMADA (DIA 2) ---

[Saludo]
Hola, ¿hablo con [nombre]? Soy Martin Mercedes, de MM Agency.

[Razon]
Te escribi ayer por IG/email, no se si lo viste. Te llamo 30 segundos para explicarte rapido por que te busque.

[Hook]
Armamos un embudo completo para una clinica medica aqui en RD y en 60 dias genero 85 pacientes interesados. Estoy hablando con clinicas para mostrarles como funciona.

[CTA]
¿Tienes 20 min esta semana para que te muestre? Sin costo.

[Si dice NO]
Entiendo. ¿Te mando info por WhatsApp?

[Si dice QUIZAS]
¿Jueves 3pm o viernes 10am te funciona?

============================================================

VARIANTE B — PREGUNTA DIRECTA

--- IG DM ---

Pregunta rapida: ¿como estas captando pacientes nuevos hoy?

Trabajo con clinicas medicas en RD montando sistemas automatizados (landing + ads + seguimiento WhatsApp) y llevo varios meses obteniendo resultados interesantes.

Si quieres te cuento en 20 min como lo hacemos. Sin costo, sin compromiso.

¿Te interesa?

Martin

--- EMAIL ---

Asunto: ¿Como captas pacientes hoy?

Hola,

Pregunta rapida: ¿como estas captando pacientes nuevos hoy?

Soy Martin Mercedes, de MM Agency. Trabajo con clinicas medicas en RD armando sistemas de captacion: landing optimizada, anuncios en Meta, CRM y seguimiento automatizado por WhatsApp.

El embudo que montamos para una clinica medica aqui genero 85 pacientes interesados en 60 dias.

Si quieres conocer como funciona y si tiene sentido para tu practica, te propongo una llamada de 20 min sin costo.

¿Te va?

Martin Mercedes
MM Agency
WhatsApp +1 849-577-2978
mmagency.com.do

--- LLAMADA (DIA 2) ---

[Saludo]
Hola, ¿hablo con [nombre]? Soy Martin de MM Agency.

[Pregunta]
Te llamo rapido para hacerte una pregunta: ¿como estas captando pacientes nuevos hoy? ¿Referidos, redes, anuncios?

[Escuchar — dejar que responda]

[Bridge]
Te pregunto porque armamos un sistema completo para una clinica medica aqui en RD y genero 85 pacientes interesados en 60 dias.

[CTA]
¿Tienes 20 min esta semana? Sin costo.

[Si dice NO] ¿Te mando info por WhatsApp?
[Si dice QUIZAS] ¿Jueves 3pm o viernes 10am?

============================================================

VARIANTE C — AUDITORIA GRATIS

--- IG DM ---

Breve.

Hago auditorias gratuitas de embudo de adquisicion para clinicas medicas en RD. Reviso landing, anuncios y seguimiento — y te digo que mejoraria, sin compromiso.

Toma 20 min. Si te sirve, trabajamos juntos. Si no, igual te llevas el analisis.

¿Te mando el link para agendar?

Martin
MM Agency

--- EMAIL ---

Asunto: Auditoria gratis para tu clinica

Hola,

Soy Martin de MM Agency. Estamos haciendo auditorias gratuitas de embudo de adquisicion de pacientes para clinicas medicas en RD.

Que incluye:
- Revision de tu presencia digital actual (web, redes, proceso de contacto)
- Diagnostico de donde se pierden pacientes
- Recomendaciones especificas para mejorar captacion
- Caso real: como una clinica medica genero 85 pacientes interesados en 60 dias

Toma 20 min por Zoom. Sin compromiso. Si no te sirve, igual te llevas el analisis.

¿Te mando el link para agendar?

Martin Mercedes
MM Agency
WhatsApp +1 849-577-2978
mmagency.com.do

--- LLAMADA (DIA 2) ---

[Saludo]
Hola, ¿hablo con [nombre]? Soy Martin de MM Agency.

[Oferta]
Te llamo 30 segundos. Estoy ofreciendo auditorias gratis de embudo de adquisicion de pacientes a clinicas medicas.

[Que incluye]
Reviso como estas captando pacientes hoy, donde se estan perdiendo y que cambiaria. Toma 20 min por Zoom y te llevas el analisis tengamos trato o no.

[CTA]
¿Te agendo esta semana? Tengo jueves 3pm o viernes 10am.

[Si dice NO AHORA] ¿Proxima semana?
[Si pregunta CUANTO CUESTA] La auditoria es gratis. Si trabajamos juntos despues, paquete inicial US$2,000 setup + US$600/mes.

============================================================

COMO USAR:

1. Abre el Google Sheet de prospectos
2. Toma los primeros 20 leads 🔥 ALTA -> Variante A
3. Siguientes 20 -> Variante B
4. Siguientes 20 -> Variante C
5. Marca en cada fila: fecha_contacto, canales_usados, que variante usaste
6. Al dia 2 llama a todos con el guion correspondiente
7. A las 48h compara tasas de respuesta
"""


def main():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    docs = build("docs", "v1", credentials=creds)

    doc = docs.documents().get(documentId=DOC_ID).execute()
    end_idx = doc["body"]["content"][-1]["endIndex"]

    requests = []
    if end_idx > 2:
        requests.append({
            "deleteContentRange": {
                "range": {"startIndex": 1, "endIndex": end_idx - 1}
            }
        })
    requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": CONTENIDO,
        }
    })

    print(f"Escribiendo {len(CONTENIDO)} chars...")
    docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
    print(f"Listo: https://docs.google.com/document/d/{DOC_ID}/edit")


if __name__ == "__main__":
    main()
