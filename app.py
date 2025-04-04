from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            img_b64 = base64.b64encode(buf.getvalue()).decode('ascii')
            return render_template('generator.html', qr_code=img_b64, text=text)

    return render_template('generator.html', qr_code=None)


if __name__ == '__main__':
    app.run(debug=True)