import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



from .models import Conversation
from django.http import JsonResponse
import os
from rest_framework import viewsets
from django.shortcuts import render


from .models import StressLevel



os.environ["OPENAI_API_KEY"] = "sk-"






from .serializers import StressLevelInputSerializer
# Import your ML model
from joblib import load
model = load('stress_model.joblib')




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_stress_level(request):
    serializer = StressLevelInputSerializer(data=request.data)
    
    if serializer.is_valid():
        # Extract data from the serializer
        input_data = serializer.validated_data
    
        # Convert the input data to a DataFrame (required format for the model)
        input_df = pd.DataFrame([input_data])
        # Preprocess data and pass it to the ML model for prediction
        result = model.predict(input_df)[0]

        stress_level = StressLevel.objects.create(user=request.user,level=result)
        stress_level.save()

        print(result)
        return Response({"result": result}, status=status.HTTP_200_OK)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#recommendation

import openai
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

path_to_csv = os.path.join(os.getcwd(), 'reco.csv')

loader = CSVLoader(file_path=path_to_csv)

index_creator = VectorstoreIndexCreator()
docsearch = index_creator.from_loaders([loader])
chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")

from apis.models import Conversation

import re

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend(request):
    user_conversations= Conversation.objects.filter(user=request.user)
    convers = []
    for i in user_conversations:
        convers.append(i.user_message)
    convers = " ".join(convers)

    system_msg = 'You are a helpful assistant who extracts the symptoms from the conversation and provides the user with a list of symptoms. You just print the symtpoms,dont say useless stuffs, just say Treated Symptoms:(symptoms))'

    user_msg = convers
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                            {"role": "user", "content": user_msg}])
    
    #return the recommendation
    stress_level = StressLevel.objects.filter(user=request.user).order_by('-measured_on').first()
    if stress_level is not None:
        stress_level = stress_level.level

    if stress_level == 0:
        stress_level = "Acute Stress"
    elif stress_level == 1:
        stress_level = "Episodic Acute Stress"
    elif stress_level == 2:
        stress_level = "Chronic Stress"
    print("stress level: ",stress_level)
    
    

    query = "These are the: " + response.choices[0]["message"]["content"] + " .And Stress Levels Treatedis "+ stress_level + " .Recommend the psyciatrist If you can't find the exact, just recommend the nearest one. 'I recommend you to visit Dr. XYZ, he is a good doctor."
    try:
        recom = chain({"question": query})
    except Exception as e:
        return JsonResponse({"recommend":"Sorry, I can't find the exact symptoms. Please try again"},status=200)
    print(recom['result'])

    return JsonResponse({"recommend":recom['result']},status=200)







#Chatbot

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a patient and an Doctor. The Doctor gives very short and sweet answers for every question. If the doctor does not know the answer to a question or if the user asks questions other than the health related, it truthfully says it does not know."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])


llm = ChatOpenAI(temperature=0)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory,prompt=prompt,llm=llm)





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def doctorai(request):
    user_input = request.data.get("message")
    response = conversation.predict(input=user_input)
    Conversation.objects.create(user=request.user,user_message=user_input, bot_response=response)
    return JsonResponse({"message": response}, status=200)



