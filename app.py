import os
import flet as ft
from google import genai

# 1. Configuración de las instrucciones del "Gem" (El sistema)
INSTRUCCIONES_GEM = """
Eres un asistente escolar llamado sagIA dividido estrictamente en dos funciones:
1. Si piden ayuda con imágenes o videos, redacta un prompt detallado listo para copiar en otra IA.
2. Si piden ayuda con tareas, NO des la respuesta. Da pistas y explica el concepto para que el alumno aprenda.
"""

# 2. Conexión segura con la API de Google usando variables de entorno
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def main(page: ft.Page):
    page.title = "sagIA - Asistente Escolar"
    page.window_width = 450
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Aplicar un esquema de color morado global a la aplicación
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.PURPLE_700,
            secondary=ft.Colors.PURPLE_ACCENT_400,
            background=ft.Colors.WHITE,
        )
    )
    
    # Componentes visuales
    chat_history = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Cuadro de texto con borde morado cuando se selecciona
    user_input = ft.TextField(
        hint_text="Pregúntale algo de clase o pide un prompt a sagIA...", 
        expand=True,
        border_color=ft.Colors.PURPLE_200,
        focused_border_color=ft.Colors.PURPLE_600
    )

    def enviar_mensaje(e):
        if not user_input.value: return
        
        # Mostrar lo que escribió el usuario con estilo morado oscuro
        chat_history.controls.append(
            ft.Text(f"Tú: {user_input.value}", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)
        )
        page.update()
        
        try:
            # Llamada a Gemini usando el nuevo SDK estándar de Google
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input.value,
                config={'system_instruction': INSTRUCCIONES_GEM}
            )
            # Mostrar la respuesta condicionada de la IA en un tono morado más suave y legible
            chat_history.controls.append(
                ft.Text(f"sagIA: {response.text}", color=ft.Colors.DEEP_PURPLE_700)
            )
        except Exception as ex:
            chat_history.controls.append(
                ft.Text(f"Error de conexión: {ex}", color="red")
            )
            
        user_input.value = ""
        page.update()

    # Botón de enviar con estilo morado sólido y texto blanco
    boton_enviar = ft.ElevatedButton(
        "Enviar", 
        on_click=enviar_mensaje,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_600
        )
    )
    
    # Construcción de la interfaz de usuario con título morado vibrante
    page.add(
        ft.Text('sagIA', size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_ACCENT_700),
        chat_history,
        ft.Row([user_input, boton_enviar])
    )

# Indicarle a Flet que arranque la aplicación asignando el puerto correcto en Render
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port)
