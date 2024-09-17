import streamlit as st
import pandas as pd
import base64

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# CSVファイルのアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")

if uploaded_file is not None:
    # CSVファイルを文字列として読み込み
    df = pd.read_csv(uploaded_file, dtype=str)

    # ヘッダー名のマッピング
    header_mapping = {
        "事業所番号": "facility_id",
        "都道府県コード又は市町村コード": "pref_code",
        "都道府県名": "pref",
        "市区町村名": "city",
        "事業所名": "facility_name",
        "事業所名カナ": "facility_name_kana",
        "サービスの種類": "service",
        "住所": "address",
        "緯度": "latitude",
        "経度": "longitude",
        "電話番号": "phone_number",
        "FAX番号": "fax_number",
        "法人番号": "company_number",
        "法人の名称": "company_name",
        "定員": "capacity",
        "URL": "url"
    }

    # 必要な列のみを抽出
    df = df[list(header_mapping.keys())]

    # ヘッダー名を変更
    df = df.rename(columns=header_mapping)

    # SQL文を生成
    sql_statements = []

    for index, row in df.iterrows():
        columns = ', '.join(row.index)
        values_list = []
        for value in row.values:
            if pd.isnull(value):
                values_list.append('NULL')
            else:
                # シングルクオートをエスケープ
                escaped_value = str(value).replace("'", "''")
                values_list.append(f"'{escaped_value}'")
        values = ', '.join(values_list)

        # 更新する列（facility_id以外）
        update_columns = [col for col in row.index if col != 'facility_id']
        update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_columns])

        sql = f"INSERT INTO partners ({columns}) VALUES ({values}) ON CONFLICT (facility_id) DO UPDATE SET {update_set};"

        sql_statements.append(sql)

    # SQL文を表示
    st.write("生成されたSQL文:")

    for sql in sql_statements:
        st.code(sql, language='sql')
        # コピー機能を追加
        b64_sql = base64.b64encode(sql.encode()).decode()
        button_id = f"copy-button-{hash(sql)}"
        custom_css = f"""
        <style>
            #{button_id} {{
                background-color: #e1e1e1;
                border: none;
                padding: 5px 10px;
                font-size: 14px;
                cursor: pointer;
                margin-bottom: 20px;
            }}
            #{button_id}:hover {{
                background-color: #d1d1d1;
            }}
        </style>
        """
        copy_button = f"""
        {custom_css}
        <button id="{button_id}" onclick="copyToClipboard('{b64_sql}')">コピー</button>
        <script>
        function copyToClipboard(text) {{
            const decodedText = atob(text);
            navigator.clipboard.writeText(decodedText);
            alert('SQL文をクリップボードにコピーしました。');
        }}
        </script>
        """
        st.markdown(copy_button, unsafe_allow_html=True)

    # SQLスクリプトをダウンロード
    sql_script = '\n'.join(sql_statements)
    st.download_button(
        label="SQLスクリプトをダウンロード",
        data=sql_script,
        file_name="update_partners.sql",
        mime='text/plain'
    )
