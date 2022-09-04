import streamlit as st
from get_pv import GetPV
import pandas as pd

st.title('ブログデータ取得ツール')
st.write('Seleniumでブログ情報を取得しStreamlitで分析できるwebサービス')

email = st.text_input('メールアドレス')
password = st.text_input('パスワード')
select_options = st.multiselect('取得するカラムを選択',['投稿者','カテゴリ','日付','PV','記事ID','文字数','アイキャッチ画像URL'],default=['カテゴリ','日付','PV'])
st.write('カラムは1つ以上選択してください。')
st.write('取得には1分以上かかる場合もあります。')
column_id_list = {'author-hide':'True','categories-hide':'True','tags-hide':'False','date-hide':'True','views-hide':'True','post-id-hide':'True','word-count-hide':'True','thumbnail-hide':'True'}
if st.button('取得'):    
    title_list,author_list,category_list,tags_list,date_list,views_list,post_id_list,word_count_list,thumbnail_list = GetPV(email,password,column_id_list)
    df = pd.DataFrame()
    df['タイトル'] = title_list
    for column_id in select_options:
        if column_id == '投稿者':
            df['投稿者'] = author_list
        if column_id == 'カテゴリ':
            df['カテゴリ'] = category_list
        if column_id == 'タグ':
            df['タグ'] = tags_list
        if column_id == '日付':
            df['日付'] = date_list
        if column_id == 'PV':
            df['PV'] = views_list
        if column_id == '記事ID':
            df['ID'] = post_id_list
        if column_id == '文字数':
            df['文字数'] = word_count_list
        if column_id == 'アイキャッチ画像URL':
            df['アイキャッチURL'] = thumbnail_list
    st.dataframe(df,width=1920,height=7000)