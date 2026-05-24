from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 仮のユーザーデータ (プロトタイプ用のハードコード)
USER_ID = "student01"
PASSWORD = "password123"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # フォームから入力されたIDとパスワードを取得
        input_id = request.form['user_id']
        input_pass = request.form['password']

        # 認証チェック
        if input_id == USER_ID and input_pass == PASSWORD:
            # 認証成功：学生証ページへリダイレクト
            return redirect(url_for('show_id'))
        else:
            # 認証失敗：エラーメッセージを設定
            error = 'ユーザーIDまたはパスワードが間違っています。'

    # GETメソッド時、または認証失敗時はログイン画面を表示
    return render_template('login.html', error=error)

@app.route('/student_id')
def show_id():
    # 認証成功後に表示されるQRコード画面
    return render_template('id_card.html')

if __name__ == '__main__':
    # アプリケーションの起動
    app.run(debug=True, host='0.0.0.0')
    
    