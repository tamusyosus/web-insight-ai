"""
app.py

Production Streamlit interface for Web RAG Chatbot.

Responsibilities:
1. Collect webpage URLs from user.
2. Build knowledge base.
3. Maintain chat history.
4. Retrieve relevant chunks.
5. Display AI answer with evidence.
"""


import streamlit as st
import time
from urllib.parse import urlparse



from ragchat import (
    build_pipeline,
    retrieve,
    answer_question
)

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Web Insight AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Load CSS
# ---------------------------------------------------

def load_css():
    """
    Load custom CSS from style.css.
    """

    with open("style.css", "r", encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )


load_css()



# ------------------------------------
# URL Validation
# ------------------------------------

def is_valid_url(url:str) -> bool:
    """
    Validate URL format.
    """

    try:

        result = urlparse(url)

        return (
            result.scheme in ["http", "https"]
            and result.netloc
        )

    except Exception:

        return False



# ---------------------------------------------------
# Cached RAG Pipeline
# ---------------------------------------------------

@st.cache_resource(
    show_spinner="⏳ Setting everything up.."
)
def create_pipeline(urls:tuple):

    return build_pipeline(urls)



# ---------------------------------------------------
# Session State
# ---------------------------------------------------

def initialize_session():

    defaults = {

        "pipeline": None,

        "messages": []

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


initialize_session()



# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.markdown(
    """
    <div class="main-title">
        🌐 Web Insight AI
    </div>

    <div class="sub-title">
        Ask questions and get answers from your selected webpages.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# Build Knowledge Base\
# ---------------------------------------------------

status_placeholder = st.empty()

build_button = False
urls_input = ""

if st.session_state.pipeline is None:

    st.subheader("🌐Add WebSites")

    st.write(
            "Enter one or more website URLs. Once they're analyzed, you can ask questions about their content."
    )

        

    urls_input = st.text_area(
        "Websit URLs",
        height=180,
        placeholder="""Enter one website URL per line

Example:

https://example.com/article1

https://example.com/article2"""
    )

    build_button = st.button(
        " Analyze Websites",
        type="primary",
        use_container_width=True
    )


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
with st.sidebar:


    st.header("⚙️ Settings")

    response_style = st.selectbox(
        "Response Style",
        [
            "Brief",
            "Balanced",
            "Detailed",
        ],
    
        help="Choose how much webpage information to use when answering.."
    )
    if response_style == "Brief":
        k = 2

    elif response_style == "Balanced":
        k = 4

    else:
        k = 6
     



    clear_chat_button = st.button(

        "💬 New Conversation",

        use_container_width=True
    )

    reset_button = st.button(

        "🗑️ Clear Sources",

        use_container_width=True
    )

    st.divider()
      

# ---------------------------------------------------
# Clear Chat
# ---------------------------------------------------

if clear_chat_button:

    st.session_state.messages = []

    st.success("🗑 Conversation cleared successfully.")

    st.rerun()

# ------------------------------------
# Reset Knowledge Base
# ------------------------------------

if reset_button:


    st.session_state.pipeline = None

    st.session_state.messages = []


    st.cache_resource.clear()


    st.success(
        "🗑️ All webpages have been removed."
    )


    st.rerun()




# ---------------------------------------------------
# Build Knowledge Base
# ---------------------------------------------------


if build_button:

    urls = []

    for line in urls_input.splitlines():

        url = line.strip()

        if not url:
            continue

        if is_valid_url(url):

            urls.append(url)

        else:

            st.warning(
                f"⚠️ Invalid URL skipped: {url}"
            )

    # Remove duplicate URLs while preserving order
    urls = list(dict.fromkeys(urls))

    if len(urls) < 1:

        status_placeholder.error(
               "Please add at least one valid webpage link."
        )

        st.stop()

    with st.spinner(
      "🔎 Analyzing your webpages..." 
      
    ):

        
        start = time.time()

        try:

           pipeline = create_pipeline(tuple(urls))

        except Exception as e:
   
           status_placeholder.error(
               "❌ Couldn't process the webpages.\n\n"
               "Please check the links and try again."
           )
           st.exception(e)
           

           st.stop()

        elapsed = time.time() - start


        st.session_state.pipeline = pipeline



        status_placeholder.success(
            f"""
        ✅ Sources are ready!

        • Webpages processed: {len(urls)}

        • Processing time: {elapsed:.2f} seconds

        You can now ask questions about your webpages.
        """
        )

        st.rerun()


# ---------------------------------------------------
# Check Pipeline Exists
# ---------------------------------------------------

if st.session_state.pipeline is None:


    st.info(

       "👆 Add your webpages and click 'Analyze Websites' to get started."

    )


    st.stop()



pipeline = st.session_state.pipeline


chunks = pipeline["chunks"]

sources = pipeline["sources"]

embedder = pipeline["embedder"]

index = pipeline["index"]

generator = pipeline["generator"]



# ---------------------------------------------------
# Display Previous chat Messages
# ---------------------------------------------------

st.subheader("💬 Conversation")

if len(st.session_state.messages) == 0:

    st.info(
        """
👋 Welcome!

Your websites have been analyzed successfully.

Ask any question about their content.
"""
    )

    

for message in st.session_state.messages:


    with st.chat_message(

        message["role"]

    ):

        st.markdown(

            message["content"]

        )



# ---------------------------------------------------
# User Question
# ---------------------------------------------------

question = st.chat_input(

    "Ask anything about the websites"

)



if question:


    st.session_state.messages.append(

        {

            "role":"user",

            "content":question

        }

    )


    with st.chat_message("user"):

        st.markdown("###👤 You")

        st.markdown(question)



    # -------------------------------
    # Retrieval
    # -------------------------------


    with st.spinner(
        "🔍 Searching your webpages..."

    ):


        hits = retrieve(

            question,

            embedder,

            index,

            chunks,

            sources,

            k

        )


    if not hits:

        st.warning(
               """
No relevant information was found.

Try:

- asking a more specific question
- indexing another webpage
- increasing the Relevant Sources setting
"""
        )

        st.stop()
    # -------------------------------
    # Generate Answer
    # -------------------------------


    with st.spinner(" 🤖 Preparing your answer...." ):

        answer = answer_question(
            
                        question,
            
                        hits,
            
                        generator
            
                    )



    # -------------------------------
    # Assistant Response
        # -------------------------------
    with st.chat_message("assistant"):

        st.markdown(" 🤖 Assistant")

        st.markdown(answer)

        with st.expander("📚 Sources Used"):

            for hit in hits:

                with st.expander(
                    f"🌐 {hit['source']} ({hit['score']*100:.0f}% relevant)"
                ):

                    st.markdown(
                        f"""
                        <div class="source-box">
                        {hit["text"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.link_button(
                        "Open Website",
                        hit["source"]
                    )
        


    st.session_state.messages.append(

        {

            "role":"assistant",

            "content":answer

        }

    )
    

st.markdown("---")

st.caption(
                  """
Developed by **Sushmita**

🌐 GitHub: https://github.com/tamusyosus 

💼 LinkedIn: https://www.linkedin.com/in/sushmitagurung/ 

Powered by AI
"""
)


   
