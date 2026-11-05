# victseng.com

Victor Tseng 曾浩瑜 的個人網站（作者中心），三語：繁中 `/`、English `/en/`、Français `/fr/`。

- 規則：網站上不寫目前的雇主；媒體文章只放索引（標題、日期、媒體、一句新寫的介紹、連結），不轉載、不翻譯投稿內文。

© 2026 Victor Tseng 曾浩瑜

## 怎麼更新

網站由 `_src/` 產生（GitHub Pages 不會公開以底線開頭的資料夾）。改了 `_src/` 裡的檔案並推上 main 之後，GitHub Actions 會自動重建網站。

- **新增媒體露出**：編輯 `_src/data/press.json`，複製一筆，填日期、媒體名（三語）、標題（三語）、原文語言、網址。只放索引，不放內文。
- **新增文章（現場筆記）**：在 `_src/notes/<網址代稱>/` 建立 `zh.md`（可再加 `en.md`、`fr.md`），開頭填 title、description、date、pillar、tags。想先存草稿不上線，就加一行 `draft: true`。
- **改首頁文字**：`_src/content.py`（三語都在這裡）。
- **本機重建**：`cd _src && pip install markdown && python3 build.py ..`
- **Podcast 區塊**：`_src/data/podcast.json`。開播時把 `live` 改成 `true`，三語首頁就會出現 Podcast 區塊和選單；新集數加在 `episodes` 最前面，`notes` 填對應文章的網址代稱，文章頁會自動出現「收聽這一集」。
