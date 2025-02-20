# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token

import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "23e81323-5a2c-4b00-b8d3-ae581ca50709"
FLOW_ID = "9eb98555-d58d-4a5d-80da-4c929809b465"
APPLICATION_TOKEN = "<YOUR_APPLICATION_TOKEN>"  # this token will generate after the flow creation
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "Agent-uBYrp": {
    "add_current_date_tool": True,
    "agent_description": "A helpful assistant with access to the following tools:",
    "agent_llm": "Google Generative AI",
    "handle_parsing_errors": True,
    "input_value": "",
    "max_iterations": 15,
    "n_messages": 100,
    "order": "Ascending",
    "sender": "Machine and User",
    "sender_name": "",
    "session_id": "",
    # Custuomize this prompt for ur use case
    "system_prompt": "So this is my writing style and you have to learn this and whatever content you generate on this writing style\nCuriosity-Driven Openings\n\nLinkedIn Post Writing Style Guidelines\n\nHook (First Line):\nStart with an attention-grabbing question, bold statement, or thought-provoking insight.\nKeep it concise and impactful to encourage the \"See more\" click.\nExample: “Struggling to stay relevant in the fast-paced world of AI? Here's how to stay ahead!”\n\nContext (Why It Matters):\nProvide a brief background to establish relevance and connect with the audience.\nUse simple, jargon-free language with short sentences.\nExample: “With technology evolving rapidly, keeping up with the latest trends isn’t just an advantage—it’s a necessity.”\n\nKey Takeaways (Main Body):\nPresent the core message in a structured format using bullet points or numbered lists. Each point should be concise and informative.\n\nInsightful: Highlight the \"why\" behind the topic.\nActionable: Share practical steps, tips, or strategies.\nRelevant: Ensure the information is current and valuable.\nExample:\n\nUse AI-powered tools to stay updated with real-time information.\nWrite posts in a structured format for better readability.\nMaintain a consistent tone and style to build your personal brand.\nCall-to-Action (Engagement):\nEnd with an invitation for interaction:\n“What’s your take on this approach? Let me know in the comments!”\n“Have you tried something similar? Share your experience!”\nHashtags:\nAdd 3–5 relevant hashtags for visibility.\nExample: #LinkedInTips #ContentCreation #AIInsights #ProfessionalGrowth\nInspirational Quote (Topic-Related):\n\"The future belongs to those who prepare for it today.\" – Malcolm X\n\nFinal Engagement Nudge:\nFound this post helpful? Like, share, and drop your thoughts in the comments! Let’s keep the conversation going!\n\nuse google search to get the real time data and outline of the topic.",
    "template": "{sender_name}: {text}",
    "verbose": True,
    "max_output_tokens": None,
    "model_name": "learnlm-1.5-pro-experimental",
    "api_key": "add ur gemini api key", #add gemini api key here
    "top_p": None,
    "temperature": 0.1,
    "n": None,
    "top_k": None,
    "tool_model_enabled": False
  },
  "ChatInput-hMIVu": {
    "background_color": "",
    "chat_icon": "",
    "files": "",
    "input_value": "",
    "sender": "User",
    "sender_name": "User",
    "session_id": "",
    "should_store_message": True,
    "text_color": ""
  },
  "ChatOutput-UgD8m": {
    "background_color": "",
    "chat_icon": "",
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "AI",
    "session_id": "",
    "should_store_message": True,
    "text_color": ""
  },
  "GoogleSearchAPICore-rsQGo": {
    "google_api_key": "add ur google search api key",  # add google search api key here
    "google_cse_id": "Add your cse id",                # add ur cse id here
    "input_value": "",
    "k": 4,
    "tools_metadata": [
      {
        "name": "GoogleSearchAPICore-search_google",
        "description": "search_google(google_api_key: Message, google_cse_id: Message, k: FieldTypes.INTEGER) - Call Google Search API and return results as a DataFrame.",
        "tags": [
          "GoogleSearchAPICore-search_google"
        ]
      }
    ]
  }
}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--application_token", type=str, default=APPLICATION_TOKEN, help="Application Token for authentication")
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=ENDPOINT, components=args.components, tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        application_token=args.application_token
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
