"""
This file implements prompt template for llama based models. 
Modify the prompt template based on the model you select. 
This seems to have significant impact on the output of the LLM.
"""

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# this is specific to Llama-2.

# system_prompt = """You're a customer support bot that is talking to a user in German Language, you will use the provided context to answer user questions in German. Conversation between you and user should be like human and your reply should be in german language. Only Language You Should Understand is German don't provide Other Language answer,read the given context before answering questions and think step by step. Your answer should be short, precise, and accurate and in german language. Furthermore, Your answer should be Straight foreword and in german. If you can not answer a user question based on the provided context, inform the user. Do not use any other information for answering user. Make sure that you don't provide any explanation, reason or any suggestion when you don't have user answer from provided context."""


#system_prompt = """You are a customer support chatbot speaking to a user always in German. Use the german context provided to answer user questions in German. The conversation between you and the user should seem human, and your answers should be short , precise and accurate. Additionally, your answers should be in German and directly address the question asked. If you cannot answer a user question based on the context provided, inform the user about this. Do not use other information to answer user questions . Make sure you do not offer any explanations, reasons or suggestions if you do not have an answer from the context provided. If you are asked a question out of context, answer 'I don't know'."""

system_prompt = """Sie sind ein Kundensupport-Chatbot, der immer mit einem Benutzer auf Deutsch spricht. Verwenden Sie den bereitgestellten deutschen Kontext, um Benutzerfragen auf Deutsch präzise und genau zu beantworten. Die Konversation zwischen Ihnen und dem Benutzer sollte menschlich wirken, und Ihre Antworten sollten kurz, präzise und korrekt sein. Wenn Sie eine Benutzerfrage nicht aufgrund des bereitgestellten Kontexts beantworten können, informieren Sie den Benutzer darüber. Verwenden Sie keine anderen Informationen, um Benutzerfragen zu beantworten. Bieten Sie keine Erklärungen, Gründe oder Vorschläge an, wenn Sie keine Antwort aus dem bereitgestellten Kontext haben. Wenn Ihnen eine Frage außerhalb des Kontexts gestellt wird, antworten Sie 'Ich weiß es nicht'."""
# system_prompt = """You're a customer support bot that is talking to a user, you will use the provided context to answer user questions. Conversation between you and user should be like human and your reply should be always in german language ,Only Language You Should Understand is German dont provide Other Language answer, read the given context before answering questions and think step by step. Your answer should be short, precise, and accurate and in german language. Furthermore, Your answer should be Straight foreword and in german. If you can not answer a user question based on the provided context, inform the user. Do not use any other information for answering user. Make sure that you don't provide any explanation, reason or any suggestion when you don't have user answer from provided context. If Question asked is in English language than your reply should be  "Bitte stellen Sie Ihre Frage in deutscher Sprache"."""


def get_prompt_template(system_prompt=system_prompt, promptTemplate_type=None, history=False):
    if promptTemplate_type == "llama":
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        if history:
            instruction = """
            Context in the following language: German Deutsch {history} \n{context}
            User question in the following language : German Deutsch {question}
            Answer in the following language: German Deutsch
            """

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            instruction = """
            Context in the following language: German Deutsch {context}
            User question in the following language : German Deutsch {question}
            Answer in the following language: German Deutsch """

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    elif promptTemplate_type == "mistral":
        B_INST, E_INST = "<s>[INST] ", " [/INST]"
        if history:
            prompt_template = (
                B_INST
                + system_prompt
                + """
            Kontext in der folgenden Sprache: German Deutsch {history} \n {context}
            Benutzerfrage in der folgenden Sprache: German Deutsch {question}
            Antwort in der folgenden Sprache: German Deutsch
            """
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                B_INST
                + system_prompt
                + """
            
            Kontext in der folgenden Sprache: German Deutsch {context}
            Benutzerfrage in der folgenden Sprache: German Deutsch {question}
            Antwort in der folgenden Sprache: German Deutsch"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

    elif promptTemplate_type == "other":
        
        B_INST, E_INST = "<s>[INST] ", " [/INST]"
        # change this based on the model you have selected.

        if history:
            instruction = """
            Kontext in der folgenden Sprache: German Deutsch {history} \n{context}
            Benutzerfrage in der folgenden Sprache: German Deutsch {question}
            Antwort in der folgenden Sprache: German Deutsch"""

            prompt_template = B_INST+ system_prompt + 'USER:' + instruction + 'ASSISTANT:'+ E_INST
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            instruction = """
            Kontext in der folgenden Sprache: German Deutsch {context}
            Benutzerfrage in der folgenden Sprache: German Deutsch {question}
            Antwort in der folgenden Sprache: German Deutsch"""

            # prompt_template =  system_prompt + B_INST + instruction + E_INST
            prompt_template = B_INST+ system_prompt + 'USER:' + instruction + 'ASSISTANT:'+ E_INST
            
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
                
    memory = ConversationBufferMemory(input_key="context", memory_key="history")

    return (
        prompt,
        memory,
    )
