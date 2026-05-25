from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ユーザー情報を保存する一時的なメモ帳（初期ユーザーとしてstudent01を登録済み）
users = {
    "student01": "password123"
}

# ログイン画面（最初の画面）
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        # メモ帳（users）にIDが存在し、パスワードが一致するか確認
        if user_id in users and users[user_id] == password:
            return redirect(url_for('id_card'))
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

        # 既に同じIDが登録されていないかチェック
        if new_id in users:
            error = 'そのIDはすでに使われています。別のIDにしてください。'
        else:
            # 新しいIDとパスワードをメモ帳（users）に追加
            users[new_id] = new_password
            # 登録成功したらログイン画面へ戻す
            return redirect(url_for('login'))
            
    return render_template('signup.html', error=error)

# 学生証表示画面
@app.route('/id_card')
def id_card():
    return render_template('id_card.html')

if __name__ == '__main__':
    # 外部からアクセスできるようにhost='0.0.0.0'を設定
    app.run(host='0.0.0.0', debug=True)