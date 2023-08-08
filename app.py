import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

txt = st.sidebar.file_uploader('Enter Whatsapp chat text file')
if(txt):
    data = txt.getvalue()
    data = data.decode('utf-8')
    df = preprocessor.preprocess(data)
    
    user_list = df['user'].unique().tolist()
    print(user_list)
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    
    selected_user = st.sidebar.selectbox("Show analysis wrt ", user_list)
    
    if st.sidebar.button("Show Analysis"):
        # st.dataframe(df)
        df = df[df['message'] != 'null\n']
        st.title("Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header('Total messages')
            st.title(num_messages)
            
        with col2:
            st.header('Total words')
            st.title(words)
            
        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)
            
        with col4:
            st.header('Links Shared')
            st.title(num_links)
            
        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.text_timeline(selected_user, df)
        
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #daily timeline
        st.title("Daily Timeline")
        fig, ax = plt.subplots()
        daily_timeline = helper.daily_stats(selected_user, df)
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color = 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            
        #busiest user in group
        
        if selected_user == "Overall":
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
            
        #create wordcloud
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        st.header("WordCloud")
        ax.imshow(df_wc)
        st.pyplot(fig)
            
        
        #most common texts
        most_common_df = helper.most_occur_texts(selected_user, df)
        
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        st.title("Most Common Words")
        st.pyplot(fig)
        
        #emoji analysis
        most_emoji = helper.most_used_emoji(selected_user, df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        
        with col1:
            st.dataframe(most_emoji)
            
        with col2:
            fig, ax = plt.subplots()
            ax.pie(most_emoji[1], labels=most_emoji[0], autopct='%0.2f')
            st.pyplot(fig)
            
        st.title('User weekly activity Heatmap')
        pivot_table = helper.heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(pivot_table)
        st.pyplot(fig)
            
        
        