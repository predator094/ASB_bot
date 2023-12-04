from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.utilities import SerpAPIWrapper
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from langchain.tools.ifttt import IFTTTWebhook
import os
from wolfram import *
import dotenv

dotenv.load_dotenv()


serp_api_key = st.secrets["SERP_API_KEY"]


# vector databasea and classes
# pinecone database
pinecone.init(
    api_key="ed3f1c85-b57a-4192-ae06-3015215da4d3",  # 71038238-854c-40ab-b350-d4d2ca3fbb13
    environment="gcp-starter",
)
index_name = "quad"  # ipcbot
embeddings = OpenAIEmbeddings()


# vector databases class
class vecd:
    def __init__(self, index_name):
        self.index = index_name

    def run(
        self,
        query: str,
    ):
        docsearch = Pinecone.from_existing_index(self.index, embeddings)
        docs = docsearch.similarity_search(query, k=8)
        return docs


db = vecd(index_name)

search = SerpAPIWrapper(
    serpapi_api_key=serp_api_key,
)
llm_math_chain = LLMMathChain.from_llm(llm=OpenAI(temperature=0), verbose=True)
# wolfram = WolframAlphaAPIWrapper(wolfram_alpha_appid="RU4KTG-89WY6RY239")

# Telegram voice call tool
url = f"https://maker.ifttt.com/trigger/test_hook/json/with/key/jZ16EY2f66l17e6Jbj4IC0LQv3a1iSU2UJSLSRJRU4B"
tele = IFTTTWebhook(
    name="map",
    description="Send a location to the users device with a location ",
    url=url,
)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful when you need to programmatically access Google's search results, perform custom web searches, or integrate Google search capabilities into your application, website, or research project. It provides access to structured search data, enabling a wide range of applications, from enhancing search functionality to collecting competitive intelligence and monitoring online content.",
    ),
    Tool(
        name="map",
        func=tele.run,
        description="Send a location to the users device with a location",
    ),
    Tool(
        name="DBMS_book",
        func=db.run,
        description="useful for when you need to search throungh the DBMS notes and DATA ANALYSIS and ALGORITHM(DMM) and questions book",
    ),
    Tool(
        name="Wolfram_alpha",
        func=wolfram.run,
        description="Useful when needed to do any mathematics , question regarding science and technology , society and culture or everyday life ",
    ),
]
