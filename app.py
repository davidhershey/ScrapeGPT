import streamlit as st
from dotenv import load_dotenv
from prompts import system_prompt, write_scraper_prompt
from gpt_tools import generate_function_name, write_scraper, try_debug
from streamlit_ace import st_ace
from utils import run_code, write_to_disk, redact_test_output
from search_for_sections import get_scraping_instructions

st.set_page_config(layout="wide")

st.title("Build and Scrapers Python with GPT-4")

load_dotenv()

session_states = {"function_name", "final_scraper", "scraper", "scraping_instructions"}

for k in session_states:
    if k not in st.session_state:
        st.session_state[k] = None


def reset_session_state():
    for k in session_states:
        st.session_state[k] = None


url = st.text_input(
    "Sample URL",
    value="https://www.espn.com/nba/injuries",
    on_change=reset_session_state,
)

task = st.text_area(
    "Describe what you want to scrape from this page",
    value="A list of every injured player on every team. Include their name, team, position, status, and the comment field",
    on_change=reset_session_state,
)

if st.button("Get Started!") or st.session_state["function_name"] is not None:
    if st.session_state["function_name"] is None:
        st.session_state["function_name"] = generate_function_name(url, task)
    st.session_state["function_name"] = st.text_input(
        "Name of the function to generate:", st.session_state["function_name"]
    )


@st.cache_data(persist=True)
def learn_to_scrape(url, task):
    return get_scraping_instructions(url, task)


if st.session_state["function_name"] is not None:
    if st.button("Build a scraper!"):
        with st.spinner(
            "Scannning the website to learn how to scrape it (this will take a minute)"
        ):
            st.session_state["scraping_instructions"] = learn_to_scrape(url, task)

        with st.spinner("Writing a scraper with those instructions"):
            st.session_state["scraper"] = write_scraper(
                url,
                task,
                st.session_state["function_name"],
                st.session_state["scraping_instructions"],
            )

if st.session_state["scraping_instructions"] is not None:
    with st.expander("Scraping Instructions"):
        st.write(st.session_state["scraping_instructions"])

if st.session_state["scraper"] is not None:
    st.write(
        "#### Here's a first draft of your scraper -- feel free to edit it, then you can automatically debug it below"
    )
    st.session_state["scraper"] = st_ace(
        value=st.session_state["scraper"], language="python", theme="ambiance"
    )


if st.session_state["scraper"] is not None:
    st.header("Automatic Debugger")
    st.write(
        "When you're ready, have GPT-4 iteratively debug the above code to make sure it works"
    )
    num_rounds = st.slider("Maximum Debugging Rounds", 1, 50, 5, 1)
    debug_model = st.selectbox(
        "What model to use for debugging", ["gpt-4", "gpt-3.5-turbo"]
    )
    # maximum_output_length = st.slider('How many words do we allow in the output of a program (larger number make it likely that you will exceed token limits)', 100, 2000, 1500, 100)
    creation_log = [
        {"role": "system", "content": system_prompt()},
        {
            "role": "user",
            "content": write_scraper_prompt(
                url,
                task,
                st.session_state["function_name"],
                st.session_state["scraping_instructions"],
            ),
        },
        {"role": "assistant", "content": f"```py\n{st.session_state['scraper']}\n```"},
    ]
    if st.button("Start Debugging"):
        write_to_disk(st.session_state["scraper"], st.session_state["function_name"])
        working_code = st.session_state["scraper"]
        for i in range(num_rounds):
            st.subheader(f"Round {i+1}")

            code_col, output_col = st.columns(2)
            output, err, return_code = run_code(st.session_state["function_name"])
            err = redact_test_output(err)
            with code_col:
                st_ace(
                    key=f"debug_round_{i}",
                    value=working_code,
                    language="python",
                    theme="ambiance",
                    readonly=True,
                )
            with output_col:
                with st.expander("STDOUT:"):
                    st.code(output)
                with st.expander("STDERR:"):
                    st.code(err)

            if return_code == 0:  # it worked!
                st.session_state["final_scraper"] = working_code
                break
            else:  # there was an error, debug
                old_code = working_code
                working_code, creation_log, response = try_debug(
                    working_code,
                    creation_log,
                    st.session_state["function_name"],
                    output,
                    err,
                    model=debug_model,
                )
                with output_col:
                    with st.expander("GPT's reasoning"):
                        st.write(response)
                write_to_disk(working_code, st.session_state["function_name"])


if st.session_state["final_scraper"] is not None:
    st.header("Final Code")
    st_ace(
        value=st.session_state["final_scraper"],
        language="python",
        theme="ambiance",
        key="final_scraper",
        readonly=True,
    )
