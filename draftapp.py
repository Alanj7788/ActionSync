import pandas as pd
import streamlit as st

from dotenv import load_dotenv

from ai_service import extract_action_items
from google_sheets import save_tasks_to_google_sheets
from styles import load_styles


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Instant Meeting Action Taker",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "is_saving" not in st.session_state:

    st.session_state["is_saving"] = False


# ============================================================
# LOAD CUSTOM STYLES
# ============================================================

load_styles()


# ============================================================
# HEADER
# ============================================================

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


# ============================================================
# MEETING DETAILS
# ============================================================

st.subheader("📝 Meeting Details")

meeting_title = st.text_input(
    "Meeting Title",
    placeholder="Example: Project Release Discussion"
)


# ============================================================
# MEETING NOTES
# ============================================================

st.subheader("📝 Meeting Notes")

meeting_notes = st.text_area(
    "Paste your meeting notes or transcript below",
    height=280,
    placeholder="""Example:

Akhil will prepare the project presentation by Monday.

Jerin needs to test the login and registration modules by Wednesday.

Abin will prepare the database documentation.

The team should discuss deployment with the manager next Monday.

The login testing is high priority.""",
    label_visibility="collapsed"
)


# ============================================================
# EXTRACT ACTION ITEMS
# ============================================================

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

                # Save meeting data
                st.session_state[
                    "meeting_title"
                ] = meeting_title

                st.session_state[
                    "tasks"
                ] = task_data

                # Remove old Google Sheet
                if "sheet_url" in st.session_state:

                    del st.session_state[
                        "sheet_url"
                    ]

                st.session_state[
                    "is_saving"
                ] = False

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


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "tasks" in st.session_state:

    st.divider()

    st.subheader(
        "✅ Action Items"
    )

    tasks = st.session_state[
        "tasks"
    ]

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

            "Priority":
                st.column_config.SelectboxColumn(
                    "Priority",
                    options=[
                        "High",
                        "Medium",
                        "Low",
                        "Not specified"
                    ]
                ),

            "Follow-up":
                st.column_config.TextColumn(
                    "Follow-up",
                    width="large"
                ),

            "Status":
                st.column_config.SelectboxColumn(
                    "Status",
                    options=[
                        "Not Started",
                        "In Progress",
                        "Completed",
                        "Blocked"
                    ]
                ),
        }
    )

    # Save table edits
    st.session_state[
        "tasks"
    ] = edited_df.to_dict(
        orient="records"
    )


# ============================================================
# SAVE TO GOOGLE SHEETS + DOWNLOAD CSV
# ============================================================

if "tasks" in st.session_state:

    st.divider()

    col1, col2 = st.columns(2)


    # ========================================================
    # GOOGLE SHEETS BUTTON
    # ========================================================

    with col1:

        # AFTER SAVING
        if "sheet_url" in st.session_state:

            st.link_button(
                "↗ Open Google Sheet",
                st.session_state[
                    "sheet_url"
                ],
                type="primary",
                use_container_width=True
            )

        # BEFORE SAVING
        else:

            save_button_placeholder = st.empty()

            save_clicked = (
                save_button_placeholder.button(
                    "💾 Save to Google Sheets",
                    type="primary",
                    use_container_width=True,
                    disabled=st.session_state[
                        "is_saving"
                    ]
                )
            )

            if save_clicked:

                # Change state
                st.session_state[
                    "is_saving"
                ] = True

                # Replace same button
                save_button_placeholder.button(
                    "⏳ Saving...",
                    type="primary",
                    use_container_width=True,
                    disabled=True
                )

                try:

                    sheet_url = (
                        save_tasks_to_google_sheets(
                            st.session_state[
                                "meeting_title"
                            ],
                            st.session_state[
                                "tasks"
                            ]
                        )
                    )

                    # Store URL
                    st.session_state[
                        "sheet_url"
                    ] = sheet_url

                    st.session_state[
                        "is_saving"
                    ] = False

                    # Rerun to show Open button
                    save_button_placeholder.empty()

                    st.rerun()

                except Exception as e:

                    st.session_state[
                        "is_saving"
                    ] = False

                    st.error(
                        "Unable to save tasks "
                        "to Google Sheets."
                    )

                    st.exception(e)


    # ========================================================
    # CSV DOWNLOAD
    # ========================================================

    with col2:

        csv_data = (
            pd.DataFrame(
                st.session_state["tasks"]
            )
            .to_csv(index=False)
        )

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="meeting_action_items.csv",
            mime="text/csv",
            use_container_width=True
        )


# ============================================================
# CLEAR RESULTS
# ============================================================

if "tasks" in st.session_state:

    st.divider()

    if st.button(
        "🗑️ Clear Results",
        use_container_width=True
    ):

        keys_to_remove = [
            "tasks",
            "meeting_title",
            "sheet_url",
            "is_saving"
        ]

        for key in keys_to_remove:

            if key in st.session_state:

                del st.session_state[key]

        st.rerun()