import streamlit as st
import sys
import json
import os
import pandas as pd
from io import BytesIO
# import streamlit_toggle as tog

# url = "https://tonton.amaneku.com/sp/list.php?id=20230612011710_zmxBic"
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from GetData import setdata

# st.session_state.read_prob_bool = False

def df_to_xlsx(df, name):
    byte_xlsx = BytesIO()
    writer_xlsx = pd.ExcelWriter(byte_xlsx, engine="xlsxwriter")
    df.to_excel(writer_xlsx, index=False, sheet_name=name)
    ##-----必要に応じてexcelのフォーマット等を設定-----##
    workbook = writer_xlsx.book
    worksheet = writer_xlsx.sheets[name]
    format1 = workbook.add_format({"num_format": "0.00"})
    worksheet.set_column("A:A", None, format1)
    writer_xlsx.save()
    ##---------------------------------------------##
    workbook = writer_xlsx.book
    out_xlsx = byte_xlsx.getvalue()
    return out_xlsx

def convert_url(url):
    if 'sp/' in url:
        return url.replace('/sp/', '/')
    else:
        return url

def result_page():
    st.session_state.read_data_bool = True
    # ページ2の内容
    st.title('特定の人の予定を抽出')
    input_value = st.session_state.get('input_value')
    st.write('取得したURL:', input_value)
    try:
        st.session_state.setdata = setdata.SetData(input_value)
    except:
        st.warning("URLが間違っています。")
        st.stop()
    for name in list(st.session_state.setdata.data_user_frame.keys()):
        st.session_state.setdata.data_user_frame[name]=st.session_state.setdata.data_user_frame[name].replace("", pd.NA).dropna(how='all', axis=0)
    stock_list = list(st.session_state.setdata.data_user_frame.keys())
    # stock_list.insert(0, "全員")
    stock = st.selectbox(label="絞り込みする人を選んでください",
            options=stock_list)
    st.header(stock)
    # st.session_state.setdata.data_user_frame[stock]=st.session_state.setdata.data_user_frame[stock].replace("", pd.NA).dropna(how='all', axis=0)
    # key1 = tog.st_toggle_switch(label="転置",
    #                 key="Key1",
    #                 default_value=False,
    #                 label_after = True,
    #                 inactive_color = '#D3D3D3',
    #                 active_color="#11567f",
    #                 track_color="#29B5E8"
    #                 )
    key1 = st.checkbox("転値")
    if key1 == False:
        st.dataframe(st.session_state.setdata.data_user_frame[stock])
        selected_dataframe = st.session_state.setdata.data_user_frame[stock]
    elif key1 == True:
        st.dataframe(st.session_state.setdata.data_user_frame[stock].T)
        selected_dataframe = st.session_state.setdata.data_user_frame[stock].T
    #for name in st.session_state.setdata.data_user_frame.keys():
    #    st.header(name)
    #    st.session_state.setdata.data_user_frame[name]=st.session_state.setdata.data_user_frame[name].replace("", pd.NA).dropna(how='all', axis=0)
    #    st.write(st.session_state.setdata.data_user_frame[name])

    # col1, col2 = st.columns(2)
    # with col1:
    selected_dataframe.to_excel(buf := BytesIO(), index=False)
    st.download_button(label="「"+stock+"」の予定をエクセル形式で保存", data=buf.getvalue(), file_name=stock+"-schedule.xlsx")

    #with col2:
    #    if st.button("全員の予定をエクセル形式で保存"):
    #       pass

    if st.button('URL入力画面に戻る'):
        # ページ2に遷移する際に入力値を渡す
        st.session_state.read_data_bool = False
        del st.session_state['input_value']
        st.experimental_rerun()


def main_page():
    # ページ1の内容
    st.title('URL入力画面')
    text_input = st.text_input('とんとんスケジュールのURLを入力してください')
    # text_input = convert_url(text_input)
    if st.button('結果の取得'):
        # ページ2に遷移する際に入力値を渡す
        st.session_state['input_value'] = text_input
        st.experimental_rerun()  # ページ2に遷移するために再描画

    st.write('Input value:', text_input)

def prob_get():
    # URL取得ページの内容
    st.session_state.read_prob_bool = False
    st.title('URL入力画面')
    text_input = st.text_input('とんとんスケジュールのURLを入力してください')
    # text_input = convert_url(text_input)
    if st.button('結果の取得'):
        # ページ2に遷移する際に入力値を渡す
        st.session_state['input_value'] = text_input
        st.session_state.read_prob_bool = True
        st.experimental_rerun()  # ページ2に遷移するために再描画

    st.write('Input value:', text_input)

def prob_result():
    st.text(st.session_state['input_value'])
    pass

def read_main():
    # ページの切り替え
    if 'input_value' not in st.session_state:
        main_page()  # ページ1を表示
    else:
        result_page()  # ページ2を表示

def prob_main():
    # ページの切り替え
    if 'read_prob_bool' not in st.session_state:
        st.session_state.read_prob_bool = False
    if 'input_value' not in st.session_state:
        prob_get()  # ページ1を表示
    else:
        prob_result()  # ページ2を表示

if __name__ == '__main__':

    # ページの切り替え
    pages = {
        "データ閲覧": read_main,
        "スケジューリング": prob_main
        # "データ可視化":out_page
    }

    offer_page = st.sidebar.selectbox('モードの選択', tuple(pages.keys()))
    if st.sidebar.button('リセットボタン'):
        try:
            del st.session_state.read_prob_bool
        except:
            pass
        try:
            del st.session_state.input_value
        except:
            pass
        try:
            del st.session_state.read_data_bool
        except:
            pass
        st.experimental_rerun()
    else:
        pass
    # st.sidebar.divider()
    try:
        st.sidebar.text("分析対象ページ")
        st.sidebar.code(st.session_state['input_value'])
    except:
        pass

    pages[offer_page]()