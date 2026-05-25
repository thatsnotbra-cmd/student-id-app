import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# メモ帳（IDごとにパスワードと学籍番号を保存）
users = {
    "student01": {
        "password": "password123",
        "student_number": "00000000"
    }
}

# ログイン画面
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if user_id in users and users[user_id]['password'] == password:
            return redirect(url_for('id_card', user_id=user_id))
        else:
            error = 'IDまたはパスワードが間違っています。'
    return render_template('login.html', error=error)

# サインアップ（会員登録）画面
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        new_id = request.form['user_id']
        new_password = request.form['password']

        if new_id in users:
            error = 'そのIDはすでに使われています。別のIDにしてください。'
        else:
            # ランダムな8桁の学籍番号を自動生成
            new_student_number = str(random.randint(2000000, 3000000))
            
            users[new_id] = {
                "password": new_password,
                "student_number": new_student_number
            }
            return redirect(url_for('login'))
            
    return render_template('signup.html', error=error)

# 【新規追加】パスワード変更画面
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    error = None
    success = None
    if request.method == 'POST':
        input_student_number = request.form['student_number']
        new_password = request.form['new_password']

        # usersの中から、入力された学籍番号を持っている人を探す
        user_found = False
        for user_id, user_data in users.items():
            if user_data['student_number'] == input_student_number:
                # 見つかったら、その人のパスワードを新しいもので上書きする
                users[user_id]['password'] = new_password
                user_found = True
                success = 'パスワードの変更が完了しました。新しいパスワードでログインしてください。'
                break # 見つかったので探すのをやめる

        # 全員探しても見つからなかった場合
        if not user_found:
            error = '入力された学籍番号は見つかりませんでした。'

    return render_template('reset_password.html', error=error, success=success)

# 学生証表示画面
@app.route('/id_card/<user_id>')
def id_card(user_id):
    if user_id not in users:
        return redirect(url_for('login'))
        
    student_number = users[user_id]['student_number']
    return render_template('id_card.html', user_id=user_id, student_number=student_number)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)