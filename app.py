from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Hesaplama geçmişi
calculation_history = []

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Hesaplama API endpoint'i"""
    try:
        data = request.get_json()
        num1 = float(data.get('num1', 0))
        num2 = float(data.get('num2', 0))
        operation = data.get('operation')
        
        result = None
        expression = ""
        
        if operation == 'add':
            result = num1 + num2
            expression = f"{num1} + {num2}"
        elif operation == 'subtract':
            result = num1 - num2
            expression = f"{num1} - {num2}"
        elif operation == 'multiply':
            result = num1 * num2
            expression = f"{num1} × {num2}"
        elif operation == 'divide':
            if num2 == 0:
                return jsonify({
                    'success': False,
                    'error': 'Sıfıra bölme hatası!'
                }), 400
            result = num1 / num2
            expression = f"{num1} ÷ {num2}"
        elif operation == 'power':
            result = num1 ** num2
            expression = f"{num1} ^ {num2}"
        elif operation == 'modulo':
            if num2 == 0:
                return jsonify({
                    'success': False,
                    'error': 'Sıfıra mod alma hatası!'
                }), 400
            result = num1 % num2
            expression = f"{num1} % {num2}"
        else:
            return jsonify({
                'success': False,
                'error': 'Geçersiz işlem!'
            }), 400
        
        # Geçmişe ekle
        calculation_entry = {
            'expression': expression,
            'result': result
        }
        calculation_history.append(calculation_entry)
        
        # Son 10 işlemi tut
        if len(calculation_history) > 10:
            calculation_history.pop(0)
        
        return jsonify({
            'success': True,
            'result': result,
            'expression': expression
        })
        
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Geçersiz sayı formatı!'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Hesaplama geçmişini getir"""
    return jsonify({
        'success': True,
        'history': calculation_history[::-1]  # Ters sırada (en yeni önce)
    })

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Geçmişi temizle"""
    calculation_history.clear()
    return jsonify({
        'success': True,
        'message': 'Geçmiş temizlendi'
    })

@app.route('/api/advanced', methods=['POST'])
def advanced_calculate():
    """Gelişmiş hesaplamalar (karekök, faktöriyel, vb.)"""
    import math
    
    try:
        data = request.get_json()
        num = float(data.get('num', 0))
        operation = data.get('operation')
        
        result = None
        expression = ""
        
        if operation == 'sqrt':
            if num < 0:
                return jsonify({
                    'success': False,
                    'error': 'Negatif sayının karekökü alınamaz!'
                }), 400
            result = math.sqrt(num)
            expression = f"√{num}"
        elif operation == 'square':
            result = num ** 2
            expression = f"{num}²"
        elif operation == 'factorial':
            if num < 0 or num != int(num):
                return jsonify({
                    'success': False,
                    'error': 'Faktöriyel sadece pozitif tam sayılar için geçerli!'
                }), 400
            result = math.factorial(int(num))
            expression = f"{int(num)}!"
        elif operation == 'log':
            if num <= 0:
                return jsonify({
                    'success': False,
                    'error': 'Logaritma sadece pozitif sayılar için geçerli!'
                }), 400
            result = math.log10(num)
            expression = f"log({num})"
        elif operation == 'ln':
            if num <= 0:
                return jsonify({
                    'success': False,
                    'error': 'Doğal logaritma sadece pozitif sayılar için geçerli!'
                }), 400
            result = math.log(num)
            expression = f"ln({num})"
        elif operation == 'sin':
            result = math.sin(math.radians(num))
            expression = f"sin({num}°)"
        elif operation == 'cos':
            result = math.cos(math.radians(num))
            expression = f"cos({num}°)"
        elif operation == 'tan':
            result = math.tan(math.radians(num))
            expression = f"tan({num}°)"
        else:
            return jsonify({
                'success': False,
                'error': 'Geçersiz işlem!'
            }), 400
        
        # Geçmişe ekle
        calculation_entry = {
            'expression': expression,
            'result': result
        }
        calculation_history.append(calculation_entry)
        
        if len(calculation_history) > 10:
            calculation_history.pop(0)
        
        return jsonify({
            'success': True,
            'result': result,
            'expression': expression
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)