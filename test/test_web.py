from flask import Flask

# Создаем экземпляр приложения
app = Flask(__name__)

@app.route('/')
def index():
    return 'Привет! Это мой второй веб-сайт.'

if __name__ == '__main__':
    # Запускаем приложение на всех интерфейсах сети
    app.run(host='0.0.0.0', port=5000)