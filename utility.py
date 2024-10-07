from fastapi import HTTPException, status
from groq import Groq
import pandas as pd
import json
import io

client = Groq(
    api_key="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",
)

async def get_file(file: str):

    message = "File Not found"
    status_code = status.HTTP_400_BAD_REQUEST

    try:
        temporary_list = []
        if not file.filename.endswith(".xlsx"):   # checking file extension
            message = "Unsupported file type"
            status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            raise HTTPException(status_code, message)

        # Read the file content asynchronously
        file_data = await file.read()  # Read file asynchronously

        # Use an in-memory buffer to pass the file data to pandas
        excel_file = io.BytesIO(file_data)
        df = pd.read_excel(excel_file)

        # iterating data in row
        for id, row in df.iterrows():
            print(row['Review'])
            try:
                a = sentiment_analysis_of_text(row['Review'])
                json_object = json.loads(a)
            except Exception:
                message = "Groq APi unsuccessful"


            context = {"Reviews": row['Review']} | json_object['sentiment']
            temporary_list.append(context)

        # converting 2D temporary_list in DataFrame
        content = pd.DataFrame(temporary_list)

        # Converting to CSV
        content.to_csv('Output_Sentiment.csv', index=False)

        # Response
        status_code = status.HTTP_200_OK
        message = "File Successfully uploaded and converted to csv"
        return status_code, message

    except Exception:
        return status_code, f"{message}"

def sentiment_analysis_of_text(text: str) -> str:

    # define model for Sentiment Analysis
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a data analyst API capable of sentiment analysis that responds in JSON.  "
                           "Only Include The JSON schema should include"
                           "\n{\n \"sentiment\":  {\n \"positive\": score,\n \"negative\": score,\n \"neutral\": score\n },\n \"confidence_score\": \"number(0-1)\"\n }"
                           " just send required json"
            },
            {
                "role": "user",
                "content": str(f"{text}")
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    return chat_completion.choices[0].message.content
