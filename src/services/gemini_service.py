from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.clients.gemini_client import GeminiClient
class GeminiService:
    def __init__(self, api_key: str, document: str, temperature: float):
        self.api_key = api_key
        self.document_path = document
        self.temperature = temperature
        self.client = GeminiClient(self.api_key, self.temperature)

        self.embeddings = self._create_embeddings()
        self.vector_store = self._create_vector_store()
        self.prompt_template = self._create_prompt_template()

    def _create_embeddings(self):
        return GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=self.api_key
        )

    def _create_vector_store(self):
        loader = CSVLoader(file_path=self.document_path)
        documents = loader.load()
        return FAISS.from_documents(documents, self.embeddings)

    def _generate_context(self, user_message):
        retriever = self.vector_store.as_retriever(search_kwargs={"k":4})
        rag_docs = retriever.invoke(user_message)
        return rag_docs

    def _create_prompt_template(self):
        template = '''
            SYSTEM:
                Você é um atendente profissional da empresa. Fale de maneira educada, objetiva e direta.
            CONTEXT:
                [CUSTOMER_INFORMATION]
                    {customer_information}
                [CONVERSATION_HISTORY]
                    {conversation_history}
                [RAG_RESULTS]
                    {rag_context}
            TASK:
                Use exclusivamente as informações acima. Nunca invente dados.
                Se não souber algo, diga que não encontrou essa informação.
            USER_MESSAGE:
                {user_message}
        '''
        return ChatPromptTemplate.from_template(template)

    def generate_message(self,
                         user_message: str,
                         customer_information: str,
                         conversation_history: str
                        ):

        rag_docs = self._generate_context(user_message)
        rag_context = "\n--\n".join([d.page_content for d in rag_docs])

        prompt = self.prompt_template.format_messages(
            customer_information = customer_information,
            conversation_history = conversation_history,
            rag_context = rag_context,
            user_message = user_message
        )

        response = self.client.generate_message(prompt)
        return response
