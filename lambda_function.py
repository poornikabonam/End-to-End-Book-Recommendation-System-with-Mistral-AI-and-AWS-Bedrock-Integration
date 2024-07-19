import boto3
import botocore.config
import json
import csv
from datetime import datetime
from io import StringIO

def keyword_generate_using_bedrock(topic: str) -> str:
    """
    Generates keywords from the provided topic using Amazon Bedrock's Mistral model.
    
    Parameters:
        topic (str): The input query or topic from which to generate keywords.
        
    Returns:
        list: A list of themes derived from the input topic.
    """
    # Construct the prompt for the model
    prompt = f"""<s>[INST]Human:Generate keywords from this query to help find suitable book recommendations that would fulfill their preference: {topic}
    Assistant:[/INST]
    """

    # Define parameters for the Bedrock model invocation
    body = {
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50
    }

    try:
        # Initialize the Bedrock client
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1",
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))
        
        # Invoke the model with the prompt
        response = bedrock.invoke_model(body=json.dumps(body), modelId="mistral.mistral-large-2402-v1:0")

        # Read and parse the response
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        text_output = response_data['outputs'][0]['text']

        # Split the response text into lines, clean up, and extract themes
        lines = text_output.split('\n')
        parsed_list = [line.strip() for line in lines if line.strip()]
        themes = [item.split('. ')[1] for item in parsed_list]
        
        return themes

    except Exception as e:
        # Handle exceptions and errors
        print(f"Error generating keywords: {e}")
        return []

def save_blog_details_s3(s3_key, s3_bucket, generate_blog):
    """
    Saves generated keywords to an S3 bucket.
    
    Parameters:
        s3_key (str): The S3 object key where the data will be stored.
        s3_bucket (str): The name of the S3 bucket.
        generate_blog (str): The content to be saved to S3.
    """
    s3 = boto3.client('s3')

    try:
        # Upload the content to S3
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=generate_blog)
        print("Keywords saved to S3")

    except Exception as e:
        # Handle exceptions and errors
        print("Error when saving to S3:", e)

def fetch_books_from_s3(keywords):
    """
    Fetches and filters book recommendations from an S3-hosted CSV based on the provided keywords.
    
    Parameters:
        keywords (list): List of keywords to filter the books.
        
    Returns:
        list: A list of recommended book names.
    """
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    try:
        # Fetch the CSV file from S3
        obj = s3.get_object(Bucket='bookrecomm', Key='books_data.csv')
        print("Fetched book data from S3")

    except Exception as e:
        # Handle exceptions and errors
        print(f"Error fetching object from S3: {e}")
        return []

    try:
        # Read and decode the CSV data
        csv_data = obj['Body'].read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(csv_data))

    except Exception as e:
        # Handle exceptions and errors
        print(f"Error reading CSV data: {e}")
        return []

    # Ensure the CSV file has headers
    if not csv_reader.fieldnames:
        print("No fieldnames found in the CSV file")
        return []

    # Function to calculate match score based on keywords
    def calculate_match_score(description):
        description_lower = description.lower()
        score = sum(description_lower.count(keyword.lower()) for keyword in keywords)
        return score

    # Create a list of books with their match scores
    books_with_scores = []
    try:
        for row in csv_reader:
            description = row['Description']
            score = calculate_match_score(description)
            if score > 0:  # Include only books with a positive match score
                books_with_scores.append((row['Name'], score))

    except Exception as e:
        # Handle exceptions and errors
        print(f"Error processing CSV data: {e}")
        return []

    # Sort books by match score in descending order and extract book names
    sorted_books = sorted(books_with_scores, key=lambda x: x[1], reverse=True)
    sorted_book_names = [book[0] for book in sorted_books]
    
    print(sorted_book_names)
    return sorted_book_names[:10]

def lambda_handler(event, context):
    """
    AWS Lambda function handler to process the event, generate keywords, and fetch book recommendations.
    
    Parameters:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object for the Lambda function.
        
    Returns:
        dict: The HTTP response with status code and body containing the book recommendations.
    """
    # Parse the input event
    event = json.loads(event['body'])
    topic = event['topic']

    # Generate keywords using Bedrock
    generate_keywords = keyword_generate_using_bedrock(topic=topic)
    print("Generated keywords:", generate_keywords)

    if generate_keywords:
        # Fetch books based on generated keywords
        response_body = fetch_books_from_s3(generate_keywords)

    else:
        print("No keywords were generated")
        response_body = []

    # Return the response
    return {
        'statusCode': 200,
        'body': json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',  # Allow all origins
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        }
    }
