# afterthought

## install dependencies
pip3 install pandas transformers streamlit
if pytorch not installed: pip3 install torch torchvision torchaudio

## download chats
enable security / perms for "all file access" for terminal
create copy of imessage history: cp ~/Library/Messages/chat.db ~/Desktop/chat_copy.db
run download_chats.py

## run
streamlit run afterthought.py