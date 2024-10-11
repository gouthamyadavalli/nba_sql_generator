import os
import sys
from dotenv import load_dotenv
from langchain_pipeline.langchain_integration import Chain
import streamlit as st
from langchain_pipeline.sql_engine import execute_sql_query
load_dotenv()

if "chain" not in st.session_state:
    st.session_state.chain = Chain(0, os.getenv("GROQ_API_KEY"), os.getenv("MODEL"))


def create_streamlit_app():
    st.title("NBA Assistant Coach - Data Query Tool")

# User input section for asking questions
    user_query = st.text_input("Enter your question about NBA data:", "")

    if st.button("Generate SQL Query"):
        with st.spinner("Generating SQL query..."):
            sql_query = st.session_state.chain.generate_sql_query(user_query)
            # st.code(sql_query, language='sql')

            # Execute the SQL query and display results
            results = execute_sql_query(sql_query)

            # Display the results in tabular format
            if not results.empty:
                st.success("Query executed successfully!")
                st.write("### Query Results")
                st.dataframe(results)

                with st.spinner("Generating summary..."):
                    summarized_answer = st.session_state.chain.summarise_results(results, user_query)
                    st.write("### Summarized Answer")
                    st.write(summarized_answer)
            else:
                st.error("No results found or error executing the query.")
if __name__ == "__main__":
    create_streamlit_app()
