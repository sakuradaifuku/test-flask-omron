# Heroku+Flask+MySQLの使い方（Windows・Ubuntu）
## ①Heroku導入
1. Heroku CLIをインストール．
-  Heroku用のコマンドを入れるため．  
    - Windowsの場合はネットからインストーラをダウンロード．
    - Ubuntuの場合はコマンドでインストール．
2. GitHub登録．
- Herokuデプロイ時にgitコマンドで動かす必要があるため．
3. Gitのインストール
4. Gitの設定
- 2．で登録したメアドとユーザ名を設定
```
$ ~[プロジェクトまでのPath]/git init
$ ~[プロジェクトまでのPath]/git config --global user.email [メアド]
$ ~[プロジェクトまでのPath]/git config --global user.name [ユーザ名]
$ ~[プロジェクトまでのPath]/git config -l # 確認の仕方
```
5. Herokuへのログイン
```
$ ~[プロジェクトまでのPath]/heroku login
（途中でHerokuにの登録情報であるメアドとパスワードを入力）
```
6. gitとHerokuの連携  
以下コマンドの後で「git config -l」をして「remote.heroku.url」がちゃんと登録できているか確認．
```
$ ~[プロジェクトまでのPath]/heroku git:remote -a [Herokuのapp名]
```

## ②FlaskをHerokuで動かすための準備
1. Procfile：以下で固定．
```
web: gunicorn run:app ==log-file=-
```
2. runtime.txt：以下で固定．
```
python-3.6.6
```
3. requirements.txt：必要なPythonパッケージだけ記入．  
ただしflaskとgunicornは必ずインストール．
```
flask==1.0.2
gunicorn==19.9.0
[パッケージ名]==[バージョン]
```
4. pythonコード  
※分かりやすくするため，実行するメインのpythonコードのファイル名を「**run.py**」とする．  
例↓↓↓
```python:run.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/python")
def hello_python():
    return "Hello Python!"

if __name__ == "__main__": # サーバ起動のため必ず記入．
    app.run()
```

## ③FlaskをHerokuにデプロイして動かす
1. まずはgitでステージ．
```
$ ~[プロジェクトまでのPath]/git add .
```
2. 次にコミット．
```
$ ~[プロジェクトまでのPath]/git commit -am "変更点などのコメント"
```
3. 最後にデプロイ
```
$ ~[プロジェクトまでのPath]/git push heroku master
```
4. Herokuのマイページの「Resources」でサーバをONにする．
5. 「https://[app名].herokuapp.com」でサイト確認．
6. HTML等テンプレートはtemplatesフォルダ下に置いてデプロイするように！

## ④-1：HerokuへのMySQL導入
1. 

## ④-2：HerokuへのPostgleSQL導入
1. 