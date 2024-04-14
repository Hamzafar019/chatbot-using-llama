# chatbot-using-llama
1. Install libraries using pip install -r requirements.txt
2. download model from https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q8_0.bin and place it in the chatbot-using-llama directory/folder
3. create data directory in chatbot-using-llama directory and place pdf files from which you want to ask questions
4. first command "python ingest.py"
5. then run "chainlit run model.py -w"
