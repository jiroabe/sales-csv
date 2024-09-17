import streamlit as st
import pandas as pd

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

    # 必要な列のみを抽出（存在する列のみ）
    existing_columns = [col for col in header_mapping.keys() if col in df.columns]
    df = df[existing_columns]

    # ヘッダー名を変更
    df = df.rename(columns=header_mapping)

    # facility_idが重複している場合、最初の行を残して重複行を削除
    df = df.drop_duplicates(subset='facility_id', keep='first')

    # 処理後のデータを表示
    st.write("処理後のデータ:")
    st.dataframe(df)

    # データフレームをCSVに変換
    csv = df.to_csv(index=False)

    # CSVファイルのダウンロードボタンを作成
    st.download_button(
        label="CSVファイルをダウンロード",
        data=csv,
        file_name="partners_care.csv",
        mime='text/csv'
    )
