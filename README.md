# sisakulint-doc
document page of sisakulint

# How To Build
以下のコマンドを順に打つ
1. `python -m venv .venv`
2. `. .venv/bin/activate`(linux or mac) or `.venv\Scripts\activate`(windows)
3. `pip install -r requirements.txt`
4. `python ogp_proxy.py &`
5. `hugo server`
  + 必要であれば`--disableFastRender --ignoreCache`(キャッシュの無効化など)オプションなどをつける
6. 表示されたアドレス(`Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)`など)にアクセスすれば確認可能

