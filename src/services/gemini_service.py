from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

class GeminiService:
    def __init__(self, api_key: str, document: str, temperature: float):
        self.api_key = api_key
        self.document_path = document
        self.temperature = temperature

        self.model = self._initialize_model()
        self.embeddings = self._create_embeddings()
        self.vector_store = self._create_vector_store()
        self.chain = self._create_chain()

    def _initialize_model(self):
        return ChatGoogleGenerativeAI(
            model='gemini-2.5-flash',
            temperature=self.temperature
        )

    def _create_embeddings(self):
        return GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=self.api_key
        )

    def _create_vector_store(self):
        loader = CSVLoader(file_path=self.document_path)
        documents = loader.load()
        return FAISS.from_documents(documents, self.embeddings)

    def _create_chain(self):
        template = (
            "Você é um vendedor de uma loja de roupas e precisa responder as perguntas do cliente.\n"
            "Contexto para usar ao responder: {context}\n"
            "Pergunta que você deve responder: {pergunta}\n"
            "Esse é o histórico das mensagens anteriores: {messages_history}"
        )
        prompt = ChatPromptTemplate.from_template(template)
        retrieval = self.vector_store.as_retriever()
        return ({"context": retrieval, "pergunta": RunnablePassthrough()} | prompt | self.model)

    def generate_message(self, user_message: str):
        message = self.chain.invoke(user_message)
        return str(message.content)
