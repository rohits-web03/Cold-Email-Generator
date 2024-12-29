import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

DEFAULT_JOB_POST_LINK = "https://www.naukri.com/job-listings-cognizant-hiring-for-net-react-developer-cognizant-technology-solutions-india-ltd-kolkata-6-to-11-years-211124502745?src=jobsearchDesk&sid=17354079545416691&xp=1&px=1"

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value=DEFAULT_JOB_POST_LINK)
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            print("Job Data: ",data)
            if not data:
                st.write("Data not found :(")
                return
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                print("Skills: ",skills)
                links = portfolio.query_links(skills)
                print("Links: ",links)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
                st.divider()
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)