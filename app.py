from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# 创建知识库目录
if not os.path.exists('knowledge'):
    os.makedirs('knowledge')

@app.route('/')
def home():
    """首页"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """提问接口"""
    question = request.form.get('question', '').strip()
    if not question:
        return jsonify({'error': '请输入问题'}), 400
    
    try:
        file_path = f'knowledge/{question}.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                answer = f.read()
            return jsonify({
                'question': question, 
                'answer': answer,
                'status': 'success'
            })
        return jsonify({
            'question': question,
            'answer': '我暂时还不知道这个问题的答案，请教会我！',
            'status': 'not_found'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/teach', methods=['POST'])
def teach_ai():
    """教学接口"""
    question = request.form.get('question', '').strip()
    answer = request.form.get('answer', '').strip()
    
    if not question or not answer:
        return jsonify({'error': '问题和答案都不能为空'}), 400
    
    try:
        file_path = f'knowledge/{question}.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(answer)
        return jsonify({
            'question': question,
            'answer': answer,
            'status': 'success',
            'message': '教学成功！'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'message': '教学失败'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)