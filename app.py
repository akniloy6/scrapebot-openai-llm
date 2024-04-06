import streamlit as st
import requests

st.title("Web Data Extractor using OpenAI LLM GPT 3.5 Turbo")
product_link = st.text_input("Give link to web page for scraping")


def convert_to_formatted_dict(input_list):
    properties = {item: {"type": "string"} for item in input_list}
    formatted_dict = {"properties": properties}
    return formatted_dict

def get_schemas():
    custom_schemas = st.text_input("Enter custom schema items (separated by commas)", "").replace(" ", "").split(",")
    all_schemas = [schema for schema in custom_schemas if schema]
    unique_schemas = list(set(all_schemas))
    return unique_schemas

user_defined_schema = get_schemas()
selected_schemas = st.multiselect("Schemas", user_defined_schema, placeholder="Press enter to add more", label_visibility="hidden")

token_limit = 4000
flag = False

if st.button("Get Data"):
    selected_schemas = convert_to_formatted_dict(selected_schemas)
    flag = True

    if product_link and flag:
        try:
            payload = {
                "url": product_link,
                "tags": ["span"],
                "schema": selected_schemas
                #"token_limit": token_limit
            }
            response = requests.post("http://localhost:8000/extract", json=payload)
            if response.status_code == 200:
                extracted_data = response.json()
                st.write("Extracted Data:", extracted_data)
            else:
                st.write("Error:", response.json().get("error"))
        except Exception as e:
            st.write("An error occurred:", str(e))