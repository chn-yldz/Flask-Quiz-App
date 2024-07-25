from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'

def get_db_connection():
    conn = sqlite3.connect('database/users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        
        if not name or not surname or not email:
            flash('Lütfen tüm alanları doldurunuz.')
            return redirect(url_for('test'))
        
        return redirect(url_for('quiz', name=name, surname=surname, email=email))
    
    return render_template('test.html')

@app.route('/quiz')
def quiz():
    name = request.args.get('name')
    surname = request.args.get('surname')
    email = request.args.get('email')
    
    questions = [
    {'id': 'q1', 'question': 'Python’da makine öğrenmesi modelleri oluşturmak için en popüler kütüphane hangisidir?', 'options': ['a) NumPy', 'b) SciPy', 'c) Scikit-learn']},
    {'id': 'q2', 'question': 'Python’da derin öğrenme modelleri oluşturmak için en sık kullanılan framework hangisidir?', 'options': ['a) TensorFlow', 'b) Flask', 'c) Django']},
    {'id': 'q3', 'question': 'Python’da yapay zeka projelerinde veri manipülasyonu ve analizi için en uygun kütüphane hangisidir?', 'options': ['a) Pandas', 'b) Matplotlib', 'c) Seaborn']},
    {'id': 'q4', 'question': 'Bilgisayar görüşünde nesneleri tespit etmek ve sınıflandırmak için kullanılan popüler bir algoritma hangisidir?', 'options': ['a) YOLO', 'b) SVM', 'c) Naive Bayes']},
    {'id': 'q5', 'question': 'Python’da görüntü işleme için kullanılan temel kütüphane hangisidir?', 'options': ['a) OpenCV', 'b) PIL', 'c) Scikit-image']},
    {'id': 'q6', 'question': 'Metin verilerindeki kelimeleri sayısal vektörlere dönüştürmek için kullanılan popüler bir yöntem hangisidir?', 'options': ['a) Word2Vec', 'b) TF-IDF', 'c) One-Hot Encoding']},
    {'id': 'q7', 'question': 'Duygu analizi gibi NLP görevlerinde kullanılan yaygın bir derin öğrenme modeli hangisidir?', 'options': ['a) RNN (Recurrent Neural Network)', 'b) CNN (Convolutional Neural Network)', 'c) GAN (Generative Adversarial Network)']},
    {'id': 'q8', 'question': 'Python’da eğitilmiş bir makine öğrenmesi modelini web uygulamasına entegre etmek için hangi framework kullanılabilir?', 'options': ['a) Flask', 'b) TensorFlow', 'c) Keras']},
    {'id': 'q9', 'question': 'Python’da bir görüntü sınıflandırma modelini mobil uygulamaya entegre etmek için hangi platform kullanılabilir?', 'options': ['a) TensorFlow Lite', 'b) PyTorch Mobile', 'c) Core ML']},
    {'id': 'q10', 'question': 'Python’da bir metin oluşturma modelini (örneğin GPT-3) kullanarak bir sohbet botu oluşturmak için hangi kütüphane kullanılabilir?', 'options': ['a) Transformers', 'b) NLTK', 'c) SpaCy']}
]

    
    return render_template('quiz.html', name=name, surname=surname, email=email, questions=questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    
    correct_answers = {'q1': 'c', 'q2': 'a', 'q3': 'a', 'q4': 'a', 'q5': 'a', 'q6': 'a', 'q7': 'a', 'q8': 'a', 'q9': 'a', 'q10': 'a'}
    correct_count = 0
    total_questions = len(correct_answers)
    
    for question_id, correct_answer in correct_answers.items():
        if request.form.get(question_id) == correct_answer:
            correct_count += 1
    
    incorrect_count = total_questions - correct_count
    accuracy = (correct_count / total_questions) * 100
    
    conn = get_db_connection()
    conn.execute('INSERT INTO users (name, surname, email, correct, incorrect, accuracy) VALUES (?, ?, ?, ?, ?, ?)', (name, surname, email, correct_count, incorrect_count, accuracy))
    conn.commit()
    conn.close()
    
    return render_template('result.html', correct=correct_count, incorrect=incorrect_count, accuracy=accuracy)

@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
