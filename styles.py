import streamlit as st


def load_styles():

    st.markdown(
        """
        <style>

        /* =====================================================
           MAIN PAGE
        ===================================================== */

        .block-container {
            max-width: 1200px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }


        /* =====================================================
           MAIN TITLE
        ===================================================== */

        .main-title {
            font-size: 42px;
            font-weight: 750;
            letter-spacing: -1px;
            margin-bottom: 6px;
        }


        /* =====================================================
           SUBTITLE
        ===================================================== */

        .subtitle {
            font-size: 17px;
            color: #7a7a7a;
            margin-bottom: 35px;
        }


        /* =====================================================
           TASK COUNT
        ===================================================== */

        .task-count {
            font-size: 18px;
            font-weight: 600;
            margin-top: 15px;
            margin-bottom: 18px;
        }


        /* =====================================================
           INPUTS
        ===================================================== */

        div[data-testid="stTextInput"] input {
            border-radius: 10px;
            padding: 12px 14px;
        }

        div[data-testid="stTextArea"] textarea {
            border-radius: 10px;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        div[data-testid="stButton"] button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 44px;
            transition: all 0.2s ease;
        }

        div[data-testid="stButton"] button:hover {
            transform: translateY(-1px);
        }


        /* =====================================================
           LINK BUTTON
        ===================================================== */

        div[data-testid="stLinkButton"] a {
            border-radius: 10px;
            font-weight: 600;
            min-height: 44px;
        }


        /* =====================================================
           DATA EDITOR
        ===================================================== */

        div[data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
        }

        </style>
        """,
        unsafe_allow_html=True
    )