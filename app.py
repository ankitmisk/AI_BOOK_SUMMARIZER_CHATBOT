import streamlit as st
import google.generativeai as genai
import streamlit as st
import pandas as pd
from io import StringIO
import time
import pickle
import numpy as np
# from llm_module import *
st.set_page_config(layout="wide")

# AIzaSyCxVEVXbzdDmizk1LMG_E8ScZnX6T0pUbc
# AIzaSyCkCfbMO-1mUhmZuqX7xNQYmNMFaxrZ0lk
# AIzaSyCROELUhDwdfeYcQNHyT3LyL5-BvfjqnnE

img_url = 'https://images.pexels.com/photos/942872/pexels-photo-942872.jpeg'

genai.configure(api_key="AIzaSyCROELUhDwdfeYcQNHyT3LyL5-BvfjqnnE")

google_model = genai.GenerativeModel("gemini-1.5-flash")


st.title("📚 AI Book Summarizer")

st.write('''This free AI book summary generator provides online access to comprehensive plot summaries of books, 
enabling you to read quickly and efficiently.''')
# 
# st.image('https://cdn.vdraw.ai/se/vdraw/web-pages/ai-book-summay/3in1-basic-plugins/images/ai-book-summarizer.webp',width = 500)

st.sidebar.title('📚AI Book Summarizer📚🔖🧾')
st.sidebar.image('https://cdn.zbaseglobal.com/saasbox/resources/png/step1-1__771a77af1df4e1e76d161d49e104d4d6.png')



writer_op = ['ANY','Munshi Premchand','Jaishankar Prasad']
writer_choice = st.sidebar.selectbox(f'Select your choice', writer_op)



if writer_choice == 'Munshi Premchand':
    books_op = ['Karmabhoomi','Godaan','Gaban','Nirmala','Rangbhoomi','Kaphan']

    books = st.sidebar.selectbox(f'Select your choice', books_op)
    books = books.lower()

    summary_type = ['short', 'bullet']
    choice_new = st.sidebar.radio(f'Select your choice', summary_type)

    try:
        model_name = books.lower() + 'model.pkl'
        with open(model_name, 'rb') as f:
            model = pickle.load(f)
    
        
        tokenizer_name = books + 'tokenizer.pkl'
        with open(tokenizer_name,'rb') as f:
            tokenizer = pickle.load(f)
    
        
        padding_name = books + 'padding_seq.pkl'
        with open(padding_name,'rb') as f:
            pad_sequences = pickle.load(f)
    
        # with open('predict_text.pkl','rb') as f:
        #     predict_text = pickle.load(f)
    
        
        # with open('summarize_text.pkl','rb') as f:
        #     summarize_text = pickle.load(f)
    
        
    
        bookfile_name = books.lower() + '.txt'
        with open(bookfile_name) as f:
            dummy_data = f.read(50)
    except Exception as err:
        st.warning('File handling Files Not Loaded Successfully')
        # st.warning(err)

    def predict_text(seed_text, next_words = 50):
        max_len = 183
        print('Predicte Func done')
        for i in range(next_words):
            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list],maxlen=max_len-1,padding='pre')
            predicted = np.argmax(model.predict(token_list,verbose = 0),axis = -1)[0]
            output_word = ''
            for word,index in tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            seed_text+= ' ' + output_word
        return seed_text


    def summarize_text(text, mode = choice_new):
        if choice_new == 'short':
            final_summary = predict_text(text,next_words=50).title() + '.'
            
        elif choice_new == 'bullet':
            generated = predict_text(text,next_words=50)
            words = generated.split()
            for i in range(1,len(words)+1):
                if i % 18 == 0:
                    words[i-1] = words[i-1]+'.\n\n👉'
                    
            final_summary = '👉' + ''' '''.join(words) + '.'.title()
            
        return final_summary
            
    try:
        story = summarize_text(dummy_data,mode=summary_type)
        summary = story
    except Exception as err:
        st.warning('Wrong Books Selected')
    # st.success('Your Summarized Story Using LSTM')

elif writer_choice == 'ANY':

    options_new = ['Chat', 'Book Summarizer']
    choice_new = st.sidebar.radio(f'Select your choice', options_new)
    
    if choice_new == 'Chat':
        st.subheader('🧑Chat here!!🤖')
        story = st.text_area('👇👇')
        prompt = 'You are an Intelligent AI, let\'s have a conversation'
        language_choice = 'English'
        
        
    else:
        prompt = 'You are an Intelligent AI BOOK Summarizer,Summarize story in '
        options = ['Text Input', 'Upload']
        choice = st.sidebar.selectbox(f'Select your choice', options)
    
        language_options = ['Hindi','English']
        
        language_choice = st.sidebar.radio(f'Select your Language for Final Summary', language_options,index=1)
            
        if choice == 'Text Input':
            # st.text_input('Paste your Story here!!')
            story = st.text_area("Paste your Story here!!")
            if story is None:
                story = None
            else:
                story = story
        else:
            uploaded_file = st.sidebar.file_uploader("Choose a file")
            if uploaded_file is not None:
                # To read file as bytes:
                # bytes_data = uploaded_file.getvalue()
                # # st.write(bytes_data)
                
                # To convert to a string based IO:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                # st.write(stringio)
            
                # To read file as string:
                string_data = stringio.read()
                st.write(string_data[:100] + '...')
                
                story = string_data
            else:
                story = None
    
    
    
    def summarize_story(text, mode="short",language = 'English', prompt = prompt):
        if text == '':
            welcome_text = 'Chat Here!! 🤖🤖'
            story = 'Enter Something, Waiting for response!!'
            return story
            
        elif text == None:
            welcome_text = 'Paste Story here!! 📚📚'
            story = 'Enter Story here, Waiting for Story response!!'
            return story
            
        else:
            prompt = prompt + language + '\n\n' + text
            response = google_model.generate_content(prompt)
            return response.text
    
    summary = summarize_story(story,mode="short",language = language_choice)

try:

    if (story == '') or (story == None):
        summary = 'Nothing here!!'
        sleep = 0.5 
    else:
        st.success('Your Summary📚')
        sleep = 1
    with st.spinner('Thinking...'):
     time.sleep(sleep)

except:
    pass

try:
    placeholder = st.empty()
    for i in range(len(summary.split(' '))):
        placeholder.write(' '.join(summary.split(' ')[0:i]))
        time.sleep(0.02)
    
    placeholder.empty()
    st.write(summary)
except:
    pass

# ---------------- FOOTER ----------------
st.markdown("---")

footer = """
<div style="position: fixed; left: 0; bottom: 0; width: 100%; 
            background-color: #f5f5f5; text-align: center; padding: 10px;">

  <p style="margin:5px;">📚 Made with ❤️ by Ankit Mishra</p>

  <a href="https://wa.me/8368061477" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/733/733585.png" width="30" style="margin:5px;">
  </a>

  <a href="https://www.linkedin.com/in/dsankitmishra/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" style="margin:5px;">
  </a>

  <a href="https://www.instagram.com/ankit____mishra/" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="30" style="margin:5px;">
  </a>

  <a href="https://www.youtube.com/@CodingAnalytics_withAnkit" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="35" style="margin:5px;">
  </a>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)





