import os
import flask
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from service.message_service import EvolutionAPI

load_dotenv()
app = flask.Flask(__name__)
loader = CSVLoader(file_path=r'data\base_dados.csv')
documents = loader.load()
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=os.getenv("GOOGLE_API_KEY")
    )
vector_store = FAISS.from_documents(documents, embeddings)
retrieval = vector_store.as_retriever()
evolution = EvolutionAPI()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0)

TEMPLATE = '''Você é um vendedor de uma loja de roupas e precisa responder as perguntas do cliente
Esse é o contexto que você deve usar para responder: {context}
Essa é a pergunta que você deve responder: {pergunta}'''
prompt = ChatPromptTemplate.from_template(TEMPLATE)

chain = (
    {"context": retrieval, "pergunta": RunnablePassthrough()}
    | prompt
    | llm
)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = flask.request.json
    instance = data['instance']
    sender_number = data['data']['key']['remoteJid'].split('@')[0]
    message = chain.invoke(data['data']['message']['extendedTextMessage']['text'])
    text_message = str(message.content)
    evolution.send_message(instance, sender_number, text_message)

    return flask.jsonify(message.content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
