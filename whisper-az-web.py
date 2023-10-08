################################################################################
# Name:
#   Simple whisper web user interface for Azure OpenAI Service
# Description:
#   This is sample program for learning Open API whisper for inexperienced
#   programmers.
# Requirement:
#   streamlit-1.27.2
#     Streamlit is a Python library that makes it easy to create interactive
#     web apps for data science and machine learning.
#   openai-0.28.1
#     The OpenAI Python package is an open-source Python library that provides
#     advanced tools and algorithms for artificial intelligence and machine 
#     learning.
#   python-dotenv-1.0.0
#     The python-dotenv package is a Python library that allows you to easily
#     load environment variables from a .env file in your Python project.
# Auther:
#   potofo
# Revision:
#   2023/10/09 01-00 potofo   Initial Creation.
# Disclaimer:
#   Please be aware that we are not responsible for any problems caused by this 
#   program.
# Specifications:
#   - Supported file types.
#     - wav,mp3,mpga, m4a,WebM,mpeg,mp4
#       - 
# Restriction:
#   - Uploaded file size is up to 25MB according to the Whisper API.
#     reffer to https://openai.com/blog/introducing-chatgpt-and-whisper-apis
#     for specifications
# License:
#   MIT License
# Copyright:
#   Copyright (c) 2023 potofo. All rihtts reserved.
# Note:
#   -
################################################################################

################################################################################
# Import sections
import streamlit as st            # must be 1.24.0 or higher
import openai
import os
from os.path import join, dirname # for establish path
from dotenv import  load_dotenv   # for Loading .env file

################################################################################
# Get Environment Variables sections
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

################################################################################
# main routine
def main():
    st.set_page_config(
        # Page title for browser
        page_title="Simple Whisper web application",
        # Favorite icon for browser
        page_icon="🧊",
        # Layout type ,centered or wide
        layout="wide",
        # Initial state of sidebar display method, expanded or collapsed
        initial_sidebar_state="collapsed",
    )

    ############################################################################
    # screen layout definitions for whisper azure web
    wsp_sb     = st.sidebar.empty()
    
    # Page title for Display web page
    wsp_title          = st.empty()
    # Lead Paragraph and restriction
    wsp_leadparagraph  = st.empty()
    wsp_upload         = st.empty()
    wsp_audio          = st.empty()
    wsp_transcriptions = st.empty()
    wsp_result         = st.empty()
    wsp_download       = st.empty()

    wsp_sb.button('Reload')
    wsp_title.title('Simple Whisper web application')
    wsp_leadparagraph.markdown("""
                      This web application can perform text recognition from video and audio files.
                      ### Restrictions
                      - Uploaded file size is up to 25MB according to the Whisper API.
                      - Supported file types.
                        - wav,mp3,mpga, m4a,WebM,mpeg,mp4
                      > Whisper API is available through our transcriptions (transcribes in source language) or translations (transcribes into English) endpoints, and accepts a variety of formats (m4a, mp3, mp4, mpeg, mpga, wav, webm):
                      > reffer to https://openai.com/blog/introducing-chatgpt-and-whisper-apis
                      
                      """,unsafe_allow_html=True)
    
    uploaded_file = wsp_upload.file_uploader("ファイルを選択してください", type=['m4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'wav', 'webm'])
    wsp_audio.audio(uploaded_file)
    btn_transcriptions_css = f"""
    <style>
      div.stButton > button:first-child  {{
        color: white;
        background: green;
        width: 600px;
        height: 50px;
        font-weight    : bold;
        //font-weight  : bold                ;/* bold text                    */
        //border       : 5px solid #f36      ;/* 枠線：ピンク色で5ピクセルの実線 */
        //border-radius: 10px 10px 10px 10px ;/* 枠線：半径10ピクセルの角丸     */
        //background   : #ddd                ;/* 背景色：薄いグレー            */
        //font-size:50px;
        /*
        padding-left: {1}rem;
        padding-right: {1}rem;
        */
        //padding-legt: 30%;
        /*
        width: 30em;
        font-size:50px;
        */
        //margin: 10px;
      }}
      div.stButton > button{{
        font-size:30px;
      }}
    </style>
    """
    # Cascading Style Sheets for  transcriptions button
    st.markdown(btn_transcriptions_css, unsafe_allow_html=True)

    # transcriptions button
    wsp_event = wsp_transcriptions.button('transcriptions')

    

################################################################################
# Event Dispatchers
################################################################################

    ############################################################################
    # In case of the transcription button is pressed
    if(wsp_event):
        print("Do transcriptions!!")
        openai.api_type    = os.getenv("OPENAI_API_TYPE")
        openai.api_base    = os.getenv("OPENAI_API_HOST")
        openai.api_key     = os.getenv("OPENAI_API_KEY")
        openai.api_version = os.getenv("OPENAI_API_VERSION") 
        language           = os.getenv("LANGUAGE")
        deployment_id      = os.getenv("AZURE_DEPLOYMENT_ID") # Deployment in Azure AI Studio

        # Confirm Parameter of Azure openAI Service
        print(f'api_type      :{openai.api_type}')
        print(f'api_base      :{openai.api_base}')
        print(f'api_key       :{openai.api_key}')
        print(f'api_version   :{openai.api_version}')
        print(f'language      :{language}')
        print(f'deployment_id :{deployment_id}')

        model_engine = 'whisper-1'

        transcript = openai.Audio.transcribe(model=model_engine,
                                    file=uploaded_file,
                                    deployment_id=deployment_id,
                                    language=language)
        
        print(str(transcript["text"]))
        #wsp_result.write(transcript["text"])
        wsp_result.markdown(transcript["text"],unsafe_allow_html=True)

        wsp_download.download_button(label='Download',data=transcript["text"], file_name='')

    ############################################################################
    # In case of the transcription button is pressed



if __name__ == '__main__':
    main()