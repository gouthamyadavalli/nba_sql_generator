from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_groq import ChatGroq
from .prompts import assistant_context, summarise_result
import json

class Chain:

    def __init__(self, temperature, groq_api_key, model_name):
        self.temperature = temperature
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        self.llm = ChatGroq(
            temperature=self.temperature,
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )

    def generate_sql_query(self, user_query):
        try:
            prompt_extract = PromptTemplate.from_template(
                assistant_context
            )
            prompt_extract = prompt_extract | self.llm
            pgsql_query = prompt_extract.invoke(input={'user_query': user_query})
            print(pgsql_query.content)
            return pgsql_query.content
        except OutputParserException as e:
            return str(e)
        
    def summarise_results(self, results, user_query):
        # Use an LLM to summarise the results
        try : 
            prompt_extract = PromptTemplate.from_template(
                summarise_result
            )
            prompt_extract = prompt_extract | self.llm
            summarised_results = prompt_extract.invoke(input={'results': results, 'user_query': user_query})
            response = json.loads(summarised_results.content)
            return response
        except OutputParserException as e:
            return str(e)
