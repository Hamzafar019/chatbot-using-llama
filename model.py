from langchain import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit as cl

DB_FIASS_PATH='vectorestore/db_fiass'

custom_prompt_template="""Use the following pieces of information to 
answer the user's questions. If you don't know the answer, please just say that you don't know
the answer, don't try to make up an answer.

Context:{context}
Question:{question}
Only returns the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vector stores
    """

    prompt=PromptTemplate(template=custom_prompt_template,input_variables=['context','question'])

    return prompt

def load_llm():
    llm=CTransformers(
        model='llama-2-7b-chat.ggmlv3.q8_0.bin',
        model_type='llama',
        max_new_tokens=512,
        temperature=0.5
    )
    return llm

def retrieval_qa_chain(llm, prompt, db):
    
    print("shit\n\n\n\n\n\n\n")
    print(3)
    print(prompt)
    print("shit\n\n\n\n\n\n\n")
    qa_chain=RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_kwargs={'k':2}),
        return_source_documents=True,
        chain_type_kwargs={'prompt':prompt}
    )

    print("shit\n\n\n\n\n\n\n")
    print(4)
    print("shit\n\n\n\n\n\n\n")
    return qa_chain

def qa_bot():
    
    print("shit\n\n\n\n\n\n\n")
    print(1)
    print("shit\n\n\n\n\n\n\n")
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device':'cpu'})
    db=FAISS.load_local(DB_FIASS_PATH,embeddings, allow_dangerous_deserialization=True)
    llm=load_llm()
    qa_prompt=set_custom_prompt()

    print("shit\n\n\n\n\n\n\n")
    print(2)
    print("shit\n\n\n\n\n\n\n")
    qa=retrieval_qa_chain(llm,qa_prompt,db)

    return qa

def final_result(query):
    qa_result=qa_bot()
    response=qa_result({'query':query})
    return response


@cl.on_chat_start
async def start():
    chain=qa_bot()
    msg=cl.Message(content="Starting the bot....")
    await msg.send()
    msg.content="Hi, Welcome to the Medical Bot. What is your query?"
    await msg.update()
    cl.user_session.set("chain",chain)

@cl.on_message
async def main(message):
    chain=cl.user_session.get("chain")
    cb=cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,answer_prefix_tokens=["FINAL","ANSWER"]
    )
    cb.answer_reached=True
    print(message)
    res=await chain.acall(message.content,callbacks=[cb])
    answer=res["result"]
    sources=res["source_documents"]

    if sources:
        answer+=f"\nSources:"+str(sources)
    else:
        answer+=f"\nNo sources found"
    await cl.Message(content=answer).send()
