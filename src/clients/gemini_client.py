from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiClient:
    def __init__(self, api_key: str, temperature: float):
        self.api_key = api_key
        self.temperature = temperature
        self.model = self._initialize_model()

    def _initialize_model(self):
        return ChatGoogleGenerativeAI(
            model='gemini-2.5-flash',
            temperature=self.temperature
        )

    def generate_message(self, request):
        response = self.model.invoke(request)
        return response.content
