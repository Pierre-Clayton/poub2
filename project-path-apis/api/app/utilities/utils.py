import random
import string
import os, base64
import sqlalchemy
from flask import current_app
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import requests
from openai import OpenAI




class UtilFunctions(object):
    """
    This is a class of helper fuctions
    formating phone numbers
    generating random passwords
    """

    def genrandomstring(self, N=36):
        return ''.join(random.choices(string.digits + string.ascii_lowercase, k=N))
    # Helper Functions
    def verify_google_token(token):
        try:
            id_info = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                current_app.config['GOOGLE_CLIENT_ID']
            )
            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return None
            return id_info
        except ValueError:
            return None

    def connect_unix_socket(self) -> sqlalchemy.engine.base.Engine:
        pool = sqlalchemy.create_engine(
            current_app.config['SQLALCHEMY_DATABASE_URI'],
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,  # 30 seconds
            pool_recycle=1800,  # 30 minutes
            # [END_EXCLUDE]
        )
        return pool


    def ask_openai_with_context(self,client,prompt, user_data, relevant_docs):
        context = "\n\n".join(relevant_docs)
        full_prompt = f"""
                    User Data: {user_data}

                    Relevant Documents:
                    {context}

                    User Query: {prompt}
                    """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": full_prompt}]
        )
        return response

        # conversation_history[user_id].append({"role": "user", "content": payload.query})

        # # Hand off to chat service
        # response_data = chat_with_llm(
        #     query=payload.query,
        #     top_k=payload.top_k,
        #     temperature=payload.temperature,
        #     user_id=user_id,
        #     personality_store=personality_store,
        #     conversation_history=conversation_history[user_id]
        # )

        # # Append assistant response
        # conversation_history[user_id].append({"role": "assistant", "content": response_data["answer"]})

    def chat_with_llm(self,query: str,top_k: int,temperature: float,user_id: str,personality_store: dict,conversation_history: list,context_docs: str):
        """
        1) Classify the query type (unblocker/planner/explainer/default).
        2) Retrieve top_k chunks from FAISS.
        3) Build a system prompt from the matching template.
        4) Call the LLM with the system prompt + context + user query.
        5) Return the final answer + partial context.
        """

        # (1) Determine question type
        question_type = self.classify_query_type(query)

        # (2) Retrieve top_k context from FAISS
        query_emb = self.get_embedding(query)
        results = context_docs
        context_text = "\n".join([r["chunk"] for r in results])

        # (3) Build system prompt
        base_prompt = PROMPT_TEMPLATES.get(question_type, PROMPT_TEMPLATES["default"])
        personality_type = personality_store.get(user_id)
        if personality_type:
            base_prompt += f"\nNote: The user's personality is described as {personality_type}. Tailor your style to best engage and serve this profile.\n"

        system_message = base_prompt + "\n=== FAISS Context ===\n" + context_text

        # (4) Create final messages
        # If you want to incorporate full conversation, you can:
        # - Build a longer list of user+assistant messages
        # For brevity, we do a single user message below
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query}
        ]

        try:
            response = client.chat.completions.create(model="gpt-4o",
            messages=messages,
            temperature=temperature)
            final_answer = response.choices[0].message.content.strip()
            return {
                "query": query,
                "top_k": top_k,
                "question_type": question_type,
                "personality_type": personality_type,
                "context_used": [r["chunk"][:150] for r in results],  # partial to avoid huge payload
                "answer": final_answer
            }
        except Exception as e:
            return {
                "error": str(e),
                "query": query,
                "question_type": question_type
            }




class EMAILSENDER(object):
    """Handdles all the logic and requirements for sending emails"""
    
    def SendDynamic(self, recipients, file, template_id: str, template_data: dict) -> None:
        """ Send a dynamic email to a list of email addresses
        :returns API response code
        :raises Exception e: raises an exception """
        # create Mail object and populate

        sg_sender_id = current_app.config['SENDGRID_SENDER']
        sg = SendGridAPIClient(current_app.config['SENDGRID_APIKEY'])


        message = Mail(
            from_email=sg_sender_id,
            to_emails=recipients)
        # pass custom values for our HTML placeholders
        message.dynamic_template_data = template_data
        message.template_id = template_id
        # create our sendgrid client object, pass it our key, then send and return our response objects
        with open(f'{file["location"]}', 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(f'{file["location"]}'),
            FileType(self.attachment_type[f'{file["type"]}']),
            Disposition('attachment'))
        message.attachment = attachedFile

        try:
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            print(f"Response code: {code}")
            print(f"Response headers: {headers}")
            print(f"Response body: {body}")
            print("Dynamic Messages Sent!")
        except Exception as e:
            print("Error: {0}".format(e))

    def SendDynamicSlim(self, recipients, template_id: str, template_data: dict) -> None:
        """ Send a dynamic email to a list of email addresses
        :returns API response code
        :raises Exception e: raises an exception """
        # create Mail object and populate
        sg_sender_id = current_app.config['SENDGRID_SENDER']
        sg = SendGridAPIClient(current_app.config['SENDGRID_APIKEY'])

        message = Mail(
            from_email=sg_sender_id,
            to_emails=recipients)
        # pass custom values for our HTML placeholders
        message.dynamic_template_data = template_data
        message.template_id = template_id
        # create our sendgrid client object, pass it our key, then send and return our response objects 
        try:
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            print(f"Response code: {code}")
            print(f"Response headers: {headers}")
            print(f"Response body: {body}")
            print("Dynamic Messages Sent!")
        except Exception as e:
            print("Error: {0}".format(e))


