# SITCON Camp 2021 Discord Bot

## Commands

機器人會給按了詢問組別訊息的使用者對應的組別身分。
一個使用者只可以獲得一個身分組，如果不小心按錯了需要請管理員幫忙移除。

- `/gen <point> <amount>` 產生 amount 組 point 分的序號
- `/use <code>` 使用該序號
- `/delete <code>` 刪除該序號
- `/rank` 取得當前小組排名

## Deploy

Put your token in either `docker-compose.yml` or `setting-sample.json`

- `docker-compose.yml`:
  ```
  environment:
    TOKEN: <your token here>
  ```

- `setting-sample.json`:
  ```
  "TOKEN": "<your token here>",
  ```

