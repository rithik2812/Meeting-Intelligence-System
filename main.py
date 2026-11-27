import streamlit as st
import json

from graph import process_meeting

st.set_page_config(
    page_title="Meeting Intelligence System",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI-Powered Meeting Intelligence System")

st.markdown(
    """
    Transform unstructured meeting transcripts into
    actionable insights using a multi-agent AI workflow.
    """
)

st.divider()

transcript = st.text_area(
    "Enter Meeting Transcript",
    height=250,
    placeholder="""
    Example:

    John: We need to complete the dashboard by Friday.
    Sarah: I will handle the data cleaning.
    Alex: I will prepare the visualization.
    John: Let's review the progress next Monday.
    """
)

if st.button("Analyze Meeting", type="primary"):

    if not transcript.strip():
        st.warning("Please enter a meeting transcript.")

    else:
        try:
            with st.spinner(
                "Running meeting intelligence agents..."
            ):
                result = process_meeting(transcript)

            st.success("Meeting analysis completed!")

            summary = result["summary"]
            tasks = result["tasks"]
            deadlines = result["deadlines"]
            email = result["email"]

            tab1, tab2, tab3, tab4 = st.tabs([
                "Summary",
                "Action Items",
                "Deadlines",
                "Follow-up Email"
            ])

            with tab1:
                st.subheader(summary["title"])

                st.write(summary["summary"])

                st.markdown("### Key Discussion Points")

                for point in summary["key_points"]:
                    st.markdown(f"- {point}")

                st.markdown("### Decisions")

                for decision in summary["decisions"]:
                    st.markdown(f"- {decision}")

            with tab2:
                st.subheader("Extracted Action Items")

                if tasks["action_items"]:
                    st.dataframe(
                        tasks["action_items"],
                        use_container_width=True
                    )
                else:
                    st.info("No action items identified.")

            with tab3:
                st.subheader("Detected Deadlines")

                if deadlines["deadlines"]:
                    st.dataframe(
                        deadlines["deadlines"],
                        use_container_width=True
                    )
                else:
                    st.info("No deadlines identified.")

            with tab4:
                st.subheader(email["subject"])

                st.text_area(
                    "Generated Follow-up Email",
                    value=email["body"],
                    height=300
                )

                st.download_button(
                    "Download Email",
                    data=email["body"],
                    file_name="follow_up_email.txt",
                    mime="text/plain"
                )

            st.divider()

            st.download_button(
                "Download Complete Analysis (JSON)",
                data=json.dumps(result, indent=4),
                file_name="meeting_analysis.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info(
                "Check your OpenAI API key and installed dependencies."
            )
