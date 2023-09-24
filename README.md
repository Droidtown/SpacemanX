# SpacemanX (失傳的空格)

很久以前，當人類仍然知道全形與半形字集的區別時，一個受過教育的打字者會注意把全型字符和半型字符之間加一個「空格」。後來，隨著文明的崩解與人類集體智力表現的衰退，這個古老的技能漸漸被遺忘了。

SpacemanX 脫胎自 Python2 時代的 Spaceman，在 Python3.6+ 的版本可以運作。它的功能就是確保「半型符號」和「全型符號」之間至少有一個空格。例如 `用English寫2次` 經過 SpacemanX 處理後，會成為 `用 English 寫 2 次` (注意到 English 這個半型字串和前後的全型字符之間多了空格，且 2 這個半型字符也和前後的全型字符之間多了空格)。

### 主要功能：
- 加空格！(不然你期待什麼？發射火箭嗎？)

### 功能：
- 輸入字串 => 輸出字串
- 輸入檔案 => 輸出檔案
- 模式 (mode) 可選為 **"modest"(預設值)** 或 **"strong"**
    - modest 模式 (預設值)
    ```python
    import SpacemanX
    inputSTR = "這是一個(English)測試"
    resultSTR = SpacemanX.makeroom(inputSTR)
    print(resultSTR)
    # "這是一個 (English) 測試" 括號前後的半型字符不加空格。
    # 適合閱讀使用
    ```
    - strong 模式
    ```python
    import SpacemanX
    inputSTR = "這是一個(English)測試"
    resultSTR = SpacemanX.makeroom(inputSTR, mode="strong")
    print(resultSTR)
    # "這是一個 ( English ) 測試" 括號前後也加上空格。
    # 適合 NLP 前處理使用
    ```