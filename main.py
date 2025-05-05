import gradio as gr
from ai_utils import generar_pregunta_y_respuestas, validar_respuesta_con_modelo

puntaje = 0
pregunta_actual = ""
respuestas_actuales = []
presentador_actual = "openai"

def nueva_ronda(presentador):
    global pregunta_actual, respuestas_actuales, presentador_actual
    presentador_actual = presentador
    pregunta_actual, respuestas_actuales = generar_pregunta_y_respuestas(presentador_actual)
    return f"Puntaje: {puntaje}", f"Pregunta: {pregunta_actual}"

def jugar(respuesta_usuario):
    global puntaje, pregunta_actual, respuestas_actuales, presentador_actual

    acierto, posicion = validar_respuesta_con_modelo(pregunta_actual, respuestas_actuales, respuesta_usuario, presentador_actual)

    resultado = f"Respuestas del presentador IA: {respuestas_actuales}\n\n"
    if acierto:
        resultado += f"✅ ¡Correcto! Tu respuesta está en la posición #{posicion}."
        puntaje += 1
    else:
        resultado += "❌ Fallaste. Tu respuesta no estaba en la lista (o fue demasiado diferente)."

    return f"Puntaje: {puntaje}", resultado, *nueva_ronda(presentador_actual)

with gr.Blocks() as demo:
    gr.Markdown("# 🎤 100 IAs Dijeron (modo presentador)")
    gr.Markdown("Elige tu modelo presentador. Él hará las preguntas y validará tus respuestas.")

    proveedor_radio = gr.Radio(["openai", "anthropic"], label="Modelo presentador", value="openai")
    puntaje_text = gr.Textbox(label="Puntaje", value="Puntaje: 0", interactive=False)
    pregunta_text = gr.Textbox(label="Pregunta", value="Haz clic en 'Nueva Ronda' para comenzar", interactive=False)
    respuesta_input = gr.Textbox(label="Tu respuesta")
    salida = gr.Textbox(label="Resultado", lines=4)

    nueva_btn = gr.Button("Nueva Ronda")
    enviar_btn = gr.Button("Enviar")

    nueva_btn.click(nueva_ronda, inputs=[proveedor_radio], outputs=[puntaje_text, pregunta_text])
    enviar_btn.click(jugar, inputs=[respuesta_input], outputs=[puntaje_text, salida, puntaje_text, pregunta_text])

if __name__ == "__main__":
    demo.launch()
