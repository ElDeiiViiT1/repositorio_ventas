from flask import Flask, request, render_template, send_file
from flask_mail import Mail, Message
from io import BytesIO
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'congregacion.ventas1@gmail.com'  # CAMBIA ESTO
app.config['MAIL_PASSWORD'] = 'njynlrxfjqtwatld'        # CAMBIA ESTO
app.config['MAIL_DEFAULT_SENDER'] = 'congregacion.ventas1@gmail.com'

mail = Mail(app)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        data = request.json

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="INFORME DE PREDICACIÓN", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Nombre: {data['nombre']}", ln=True)
        pdf.cell(200, 10, txt=f"Mes: {data['mes']}", ln=True)
        pdf.cell(200, 10, txt=f"Participación: {'Sí' if data['participacion'] else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Cursos bíblicos dirigidos: {data['cursos']}", ln=True)
        pdf.cell(200, 10, txt=f"Horas: {data['horas']}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Comentarios: {data['comentarios']}")

        # ✅ Generar PDF como string y convertirlo a bytes
        pdf_bytes = bytes(pdf.output(dest='S').encode('latin-1'))

        msg = Message(subject=f"Informe de Predicación - {data['nombre']} ({data['mes']})",
                      recipients=["david.carrera2001@gmail.com"])
        msg.body = "Se adjunta el informe de predicación."
        msg.attach("Informe.pdf", "application/pdf", pdf_bytes)

        print("📤 Enviando correo...")
        mail.send(msg)
        print("✅ Correo enviado con éxito.")
        return {'message': 'Informe enviado con éxito'}, 200

    except Exception as e:
        print("🔴 ERROR DETECTADO:", e)
        return {'message': 'Error interno'}, 500
    
#if __name__ == '__main__':
 #   app.run(debug=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)