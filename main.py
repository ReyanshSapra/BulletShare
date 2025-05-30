import streamlit as st
import string
import random
from minio import Minio
from minio.error import S3Error
from io import BytesIO

client = Minio(
    endpoint="play.min.io",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        secure=True
    )
st.set_page_config(page_title="BulletShare")
if 'currentScreen' not in st.session_state: 
    st.session_state.currentScreen = "home"

if "mainSendButton" not in st.session_state:
    st.session_state.mainSendButton = None

if "uploader" not in st.session_state:
    st.session_state.uploader = None

if "finalSendButton" not in st.session_state:
    st.session_state.finalSendButton = None

if "mainRecieveButton" not in st.session_state:
    st.session_state.mainRecieveButton = None

if "codeEntry" not in st.session_state:
    st.session_state.codeEntry = None

if "finalRecieveButton" not in st.session_state:
    st.session_state.finalReceiveButton = None

if "matchingFiles" not in st.session_state:
    st.session_state.matchingFiles = []

if "found_file" not in st.session_state:
    st.session_state.found_file = None

if "FileLink" not in st.session_state:
    st.session_state.FileLink = None

if "bucketName" not in st.session_state:
    st.session_state.bucketName = "bulletshare"

if "fileToDownload" not in st.session_state:
    st.session_state.fileToDownload = None

if "downloadButton" not in st.session_state:
    st.session_state.downloadButton = None

hide_st_style = """
    <style>
        .stApp {background-color: #C5DFF8;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

MainHeading = """
    <h1 style='text-align: center; color: black;'>
        Bullet
        <span style='color: #4A55A2; font-size: 1.3em'>
            Share  
        </span>
        <hr style='padding:0; margin:0; width: 50%; left:25%; position:absolute; border: none; border-top: 2px solid black;'>
    </h1>"""
st.markdown(MainHeading, unsafe_allow_html=True)
st.write("All data sent and recieved on this platform are hosted on a open-source cloud server so do not send anything that is private or confidential")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.session_state.mainSendButton = st.button("Send File")
    if st.session_state.mainSendButton:
        st.session_state.currentScreen = "send"
        st.rerun()

with col2:
    st.session_state.mainRecieveButton = st.button("Recieve Files")
    if st.session_state.mainRecieveButton:
        st.session_state.currentScreen = "recieve"
        st.rerun()

if st.session_state.currentScreen == "send":
    st.session_state.uploader = st.file_uploader("Upload File",
                type=['png', 'jpg', 'jpeg', 'mp4', 'mp3', 'pdf', 'docx', 'txt', 'xlsx', "pptx", "zip", "rar"],
                accept_multiple_files=False,
                label_visibility="collapsed",
                on_change=None)
    
    st.session_state.finalSendButton = st.button("Send")

    if st.session_state.finalSendButton:
        st.session_state.currentScreen = "final send"
        st.rerun()

elif st.session_state.currentScreen == "final send":
    if st.session_state.uploader is None:
        st.session_state.currentScreen = "send"
        print("select file")
        
    else:
        letters = string.ascii_uppercase
        code = ''.join(random.choices(letters, k=6))

        
        st.subheader("File Sent Successfully")
        if client.bucket_exists(st.session_state.bucketName):
            client.put_object(st.session_state.bucketName, f"{code}/{st.session_state.uploader.name}", data=st.session_state.uploader, length=st.session_state.uploader.size, content_type=st.session_state.uploader.type)

        else:
            client.make_bucket(st.session_state.bucketName)
            client.put_object(st.session_state.bucketName, f"{code}/{st.session_state.uploader.name}", data=st.session_state.uploader, length=st.session_state.uploader.size, content_type=st.session_state.uploader.type)


        st.subheader(code)
        
elif st.session_state.currentScreen == "recieve":
    st.subheader("Enter code to recieve file")
    st.session_state.codeEntry = st.text_input(label=" ", label_visibility="hidden")

    st.session_state.finalRecieveButton = st.button("Recieve")

    if st.session_state.finalRecieveButton:
        if len(st.session_state.codeEntry) == 6:
            try:
                objects = client.list_objects(st.session_state.bucketName, prefix=st.session_state.codeEntry + "/")
            
                for obj in objects:
                    if obj.object_name.startswith(st.session_state.codeEntry + "/"):
                        st.session_state.found_file = obj.object_name
                        break
                
                if st.session_state.found_file:
                    print(st.session_state.found_file.split("/")[1])
                    st.session_state.fileToDownload = client.get_object(st.session_state.bucketName, st.session_state.found_file)

                    fileData = BytesIO(st.session_state.fileToDownload.read())
    
                    st.session_state.downloadButton = st.download_button(label="Download File", data=fileData, file_name=st.session_state.found_file.split("/")[1])
                    
                    if st.session_state.downloadButton:
                        print("successfully downloaded")

                    else:
                        print("didnt work...")

                else:
                    print("no find")
            except S3Error as e:
                print(f"Error occurred: {e}")

        else:
            print("code is invalid")
