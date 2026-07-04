import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI(title="Diagnostic AI Customer Agent API")

class ChatRequest(BaseModel):
    customer_query: str

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY environment variable is missing!")

# 1. Initialize Objects
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.3)
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
vector_store = Chroma(embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 2. Setup Prompt
system_prompt = (
    "You are a Senior Customer Support Specialist at SwiftDelivery Logistics.\n"
    "Use the following pieces of retrieved context to answer the question. "
    "If the question is completely unrelated to shipping, logistics, company policy, or returns, "
    "politely refuse to answer and state that you can only help with delivery logistics.\n\n"
    "Context:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 3. Clean Linear Execution Block
@app.post("/api/chat")
def handle_customer_chat(request: ChatRequest):
    try:
        query = request.customer_query
        print(f"📥 Received User Query: {query}")
        
        # Step A: Perform Database Search explicitly
        print("🔍 Searching database documents...")
        docs = retriever.invoke(query)
        context_text = "\n\n".join(doc.page_content for doc in docs)
        print(f"📄 Found context content length: {len(context_text)}")

        # Step B: Assemble Message Data structures
        formatted_messages = prompt.format_messages(context=context_text, input=query)

        # Step C: Call LLM and parse directly
        print("🤖 Invoking Gemini Model call...")
        response = llm.invoke(formatted_messages)
        
        # Smart Text Extractor:
        # If Gemini returns a list/dict object, extract the inner text field cleanly
        final_output = response.content
        if isinstance(final_output, list) and len(final_output) > 0:
            if isinstance(final_output[0], dict) and 'text' in final_output[0]:
                final_output = final_output[0]['text']
        
        return {
            "status": "success",
            "query": query,
            "response": str(final_output)
        }
        
    except Exception as e:
        # Crucial: This prints the exact line/reason why it breaks to your Anaconda terminal
        print(f"❌ CRITICAL BACKEND EXCEPTION ENCOUNTERED: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "API Diagnostic server active."}