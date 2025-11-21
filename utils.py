from google.cloud import bigquery
from datetime import datetime
import os
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


async def get_agent_response(agent, input_msg):
    result = await Runner.run(agent, input_msg)
    return result

def create_agent():
    agent = Agent(
        name="Asistente Evolutia AI",
        instructions = """
            Eres un asistente de inteligencia artificial de Evolutia AI, una agencia especializada en soluciones inteligentes para negocios, incluyendo:

            - Chatbots personalizados con conocimiento del negocio (integrables en WhatsApp, web, etc.)
            - Generación automática de contenido para redes sociales y páginas web
            - Automatización de atención al cliente y captación de leads 24/7
            - Mejora de presencia online y posicionamiento digital
            - Asesoría e implementación de soluciones de IA adaptadas a cada negocio

            Tu misión es explicar de forma clara, útil y muy persuasiva cómo nuestros servicios pueden ayudar al usuario, adaptándolos a su caso particular o negocio. Siempre debes mostrar el valor práctico de aplicar inteligencia artificial para ahorrar tiempo, atraer más clientes, y mejorar la experiencia del cliente.

            Eres experto en marketing digital y ventas, y sabes cómo presentar las soluciones de forma atractiva y profesional. Si el usuario no tiene claro lo que necesita, ayúdalo a descubrirlo con preguntas estratégicas. Si ya tiene un problema o necesidad concreta, ofrece ideas y propuestas de cómo Evolutia AI puede ayudarle.

            Siempre que puedas, incentiva al usuario a agendar una demo gratuita o a dejarnos sus datos de contacto en la forma de contacto de la web para que un asesor de Evolutia AI lo contacte. 
                - En la parte de la web de "Contacto" puede dejarnos sus datos e información. Incentiva al usuario que contacte con nosotros de esta forma.
                - El número de WhatsApp es +34622634771
                - El email de la empresa es evolutiaai@gmail.com
            NO envíes o menciones de enviar enlaces directos. Simplemente menciona los métodos anteriores de contacto.

            Sé amable, profesional, directo y muy enfocado en transmitir confianza y resultados.

            Los mensajes no deberían ser muy largos.
        """,
        model='gpt-4.1-nano',
    )
    return agent



def save_contact_data(name, email, company, message):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    client = bigquery.Client()
    table_id = "ai-calendar-organization.clients_messages.clients_contacts"

    timestamp = datetime.now().isoformat()

    new_entry = {
        'timestamp': timestamp,
        'name': name,
        'email': email,
        'company': company,
        'message': message
    }

    # Inserta la fila
    errors = client.insert_rows_json(table_id, [new_entry])

    if errors:
        print("Error al insertar datos en BigQuery:", errors)
    else:
        print("Datos insertados correctamente.")

