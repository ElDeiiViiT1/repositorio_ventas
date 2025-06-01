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
app.config['MAIL_PASSWORD'] = 'Zaragoza.1914.1914'        # CAMBIA ESTO
app.config['MAIL_DEFAULT_SENDER'] = 'congregacion.ventas1@gmail.com'

mail = Mail(app)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
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

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    msg = Message(subject=f"Informe de Predicación - {data['nombre']} ({data['mes']})",
                  recipients=["david.carrera2001@gmail.com"])
    msg.body = "Se adjunta el informe de predicación."
    msg.attach("Informe.pdf", "application/pdf", pdf_output.read())

    mail.send(msg)
    return {'message': 'Informe enviado con éxito'}, 200

if __name__ == '__main__':
    app.run(debug=True)