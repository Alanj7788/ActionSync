import pandas as pd
import streamlit as st

from ai_service import extract_action_items
from styles import load_styles


st.set_page_config(
    page_title="Instant Meeting Action Taker",
    page_icon="📋",
    layout="wide"
)

load_styles()


st.markdown(
    """
    <div class="main-title">
        📋 Instant Meeting Action Taker
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Convert meeting discussions into clear, actionable tasks
        using Generative AI.
    </div>
    """,
    unsafe_allow_html=True
)


st.subheader("📝 Meeting Details")

meeting_title = st.text_input(
    "Meeting Title",
    placeholder="Example: Project Release Discussion"
)


st.subheader("📝 Meeting Notes")

meeting_notes = st.text_area(
    "Paste your meeting notes or transcript below",
    height=280,
    placeholder="""Example:

Project Manager: Let's discuss the upcoming release.

Alan: I will complete the authentication module by Friday.

Rahul: I will test the login and registration modules by Monday.

Project Manager: Rahul, please share any critical issues with the team immediately.""",
    label_visibility="collapsed"
)


extract_button = st.button(
    "✨ Extract Action Items",
    type="primary",
    use_container_width=True
)


if extract_button:

    if not meeting_title.strip():

        st.warning(
            "Please enter a meeting title."
        )

    elif not meeting_notes.strip():

        st.warning(
            "Please paste some meeting notes first."
        )

    else:

        with st.spinner(
            "🤖 Analyzing meeting notes..."
        ):

            try:

                task_data = extract_action_items(
                    meeting_notes
                )

                st.session_state[
                    "meeting_title"
                ] = meeting_title

                st.session_state[
                    "tasks"
                ] = task_data

                st.success(
                    f"Successfully extracted "
                    f"{len(task_data)} action items!"
                )

            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "analyzing the meeting."
                )

                st.exception(e)


if "tasks" in st.session_state:

    st.divider()

    st.subheader("✅ Action Items")

    tasks = st.session_state["tasks"]

    st.markdown(
        f"""
        <div class="task-count">
            {len(tasks)} tasks identified
        </div>
        """,
        unsafe_allow_html=True
    )

    df = pd.DataFrame(tasks)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={

            "Task": st.column_config.TextColumn(
                "Task",
                width="large"
            ),

            "Owner": st.column_config.TextColumn(
                "Owner",
                width="medium"
            ),

            "Deadline": st.column_config.TextColumn(
                "Deadline",
                width="medium"
            ),

            "Follow-up": st.column_config.TextColumn(
                "Follow-up",
                width="large"
            )
        }
    )

    st.session_state["tasks"] = (
        edited_df.to_dict(
            orient="records"
        )
    )


if "tasks" in st.session_state:

    st.divider()

    csv_data = pd.DataFrame(
        st.session_state["tasks"]
    ).to_csv(
        index=False
    )

    st.download_button(
        label="⬇️ Download CSV",
        data=csv_data,
        file_name="meeting_action_items.csv",
        mime="text/csv",
        type="primary",
        use_container_width=True
    )


if "tasks" in st.session_state:

    st.divider()

    if st.button(
        "🗑️ Clear Results",
        use_container_width=True
    ):

        del st.session_state["tasks"]

        if "meeting_title" in st.session_state:

            del st.session_state[
                "meeting_title"
            ]

        st.rerun()