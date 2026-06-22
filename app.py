import os
import flet as ft
from google import genai

# 1. Configuración de las instrucciones del "Gem" (El sistema)
INSTRUCCIONES_GEM = """
Eres un asistente escolar dividido estrictamente en dos funciones:
1. Si piden ayuda con imágenes o videos, redacta un prompt detallado listo para copiar en otra IA.
2. Si piden ayuda con tareas, NO des la respuesta. Da pistas y explica el concepto para que el alumno aprenda.
"""

# 2. Conexión con la API de Google
client = genai.Client(api_key="AQ.Ab8RN6LRCXp-ztniSsSbs93WCqiiKW5XoLuFDdE8tDvKq5jTGQ")

def main(page: ft.Page):
    page.title = "EduPrompt App - Proyecto Escolar"
    page.window_width = 450
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Componentes visuales
    chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    user_input = ft.TextField(hint_text="Pregúntame algo de clase o pide un prompt...", expand=True)

    def enviar_mensaje(e):
        if not user_input.value: return
        
        # Mostrar lo que escribió el usuario
        chat_history.controls.append(ft.Text(f"Tú: {user_input.value}", weight=ft.FontWeight.BOLD))
        page.update()
        
        try:
            # Llamada a Gemini usando el nuevo SDK estándar de Google
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input.value,
                config={'system_instruction': INSTRUCCIONES_GEM}
            )
            # Mostrar la respuesta condicionada de la IA
            chat_history.controls.append(ft.Text(f"IA: {response.text}"))
        except Exception as ex:
            chat_history.controls.append(ft.Text(f"Error de conexión: {ex}", color="red"))
            
        user_input.value = ""
        page.update()

    # Botón clásico sin incompatibilidades de íconos
    boton_enviar = ft.ElevatedButton("Enviar", on_click=enviar_mensaje)
    
    # Construcción de la interfaz de usuario
    page.add(
        ft.Text('Asistente Valeria')
