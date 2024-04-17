import os
from dotenv import load_dotenv


# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    """
    """ 
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        print(ai_key)

        # Create client using endpoint and key   
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(
                    endpoint=ai_endpoint, 
                    credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = '/home/caron/codes_formation_Azure/AI-102-AIEngineer/05-analyze-text/Python/text-analysis/reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), 
                        encoding='utf8').read()
            # print('\n' + text)
            # Get language
            detected_language = ai_client.detect_language(documents=[text])[0]
            print(f"\nLanguage:{detected_language.primary_language.name}")
            # Get sentiment
            sentiment_analysis = ai_client.analyze_sentiment(documents=[text])[0]
            print(f"\nSentiment:{sentiment_analysis.sentiment}")
            # Get key phrases
            phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))

            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nEntities")
                for entity in entities:
                    print('\t{} ({})'.format(entity.text, entity.category))
                    
            # Get linked entities
            entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("\nLinks")
                for linked_entity in entities:
                    print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()