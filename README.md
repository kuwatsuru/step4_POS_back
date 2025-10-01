# POS API (FastAPI)

## セットアップ
1. `.env.example` を `.env` にコピーして値を設定
2. 依存インストール
   ```bash
   pip install -r requirements.txt
   ```
3. 起動
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

## エンドポイント
- GET `/products/{code}`
- POST `/orders`
