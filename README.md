# End-to-End-Book-Recommendation-System-with-Mistral-AI-and-AWS-Bedrock-Integration
![unnamed](https://github.com/user-attachments/assets/18fb097c-81a0-4ba3-a08c-eea23503acd5)

# **End-to-End Book Recommendation System**

## **Table of Contents**
- [Overview](#overview)
- [Architecture](#architecture)
- [Process Flow](#process-flow)
- [AWS Setup](#aws-setup)
  - [Dataset](#dataset)
  - [Frontend Deployment](#frontend-deployment)
  - [Backend Configuration](#backend-configuration)
  - [API Gateway Setup](#api-gateway-setup)
  - [AWS Lambda Configuration](#aws-lambda-configuration)
  - [CloudWatch Monitoring](#cloudwatch-monitoring)
- [Achievements](#achievements)
- [Contributing](#contributing)
- [License](#license)

## **Overview**
The End-to-End Book Recommendation System integrates a React frontend with various AWS services to process user preferences and generate book recommendations. This document details the setup and configuration of AWS components involved in this architecture.

## **Architecture**
![image](https://github.com/user-attachments/assets/1a08705f-2074-4df3-94dc-4be0e1e2069b) <!-- Add an architecture diagram showing AWS components and their interactions -->

## **Process Flow**
1. **User Input**: Captured via the React frontend.
2. **Request Handling**: Processed by AWS Lambda, which interacts with other AWS services.
3. **Keyword Generation**: Performed by AWS Bedrock with Mistral AI.
4. **Book Data Retrieval**: From Amazon S3, filtered based on generated keywords.
5. **Response Delivery**: Recommendations are sent back to the frontend.

## **AWS Setup**

## **Dataset**
Dataset - https://www.kaggle.com/datasets/bahramjannesarr/goodreads-book-datasets-10m

### **Frontend Deployment**
The React application is hosted on Amazon S3, which serves the frontend assets and ensures scalability.

1. **Create an S3 Bucket**:
   - Go to the Amazon S3 console.
   - Create a new S3 bucket.
   - Set up bucket policies to allow public access for static website hosting.

2. **Deploy React Application**:
   - Build the React application using `npm run build`.
   - Upload the build folder to the S3 bucket.

3. **Enable Static Website Hosting**:
   - In the S3 bucket properties, enable static website hosting.
   - Specify the index document (e.g., `index.html`).

4. **Configure CDN (Optional)**:
   - Set up Amazon CloudFront for content delivery and caching.

![image](https://github.com/user-attachments/assets/303e5cff-e65d-491b-aa1d-edd695b6c187)
 <!-- Add an image of the S3 bucket configuration and CloudFront setup -->

### **Backend Configuration**

#### **API Gateway Setup**
API Gateway serves as the interface between the frontend and backend.

1. **Create an API**:
   - Go to the API Gateway console.
   - Create a new REST API.

2. **Set Up Resources and Methods**:
   - Define resources and HTTP methods (e.g., POST) for the API.
   - Integrate the API methods with AWS Lambda functions.

3. **Configure CORS**:
   - Enable Cross-Origin Resource Sharing (CORS) to allow requests from the frontend.

4. **Deploy the API**:
   - Create a deployment stage and deploy the API.
   - 
![image](https://github.com/user-attachments/assets/4d9bcd9e-6d71-4f72-ba23-91015293a0f8)
 <!-- Add an image of the API Gateway configuration and deployment -->

### **AWS Lambda Configuration**
AWS Lambda executes the backend logic for processing and generating recommendations.

1. **Create a Lambda Function**:
   - Go to the AWS Lambda console.
   - Create a new Lambda function.
   - Choose Python as the runtime.

2. **Configure Lambda Layers**:
   - Add the `boto3` library as a Lambda layer to interact with other AWS services.

3. **Upload Lambda Code**:
   - Upload or paste the code into the Lambda function editor.
   - Set up environment variables and permissions as needed.

4. **Set Lambda Triggers**:
   - Link the Lambda function with API Gateway as a trigger.

![image](https://github.com/user-attachments/assets/27560a33-1890-441e-a468-0a903aa1717d) <!-- Add an image of the Lambda function configuration and code editor -->

### **CloudWatch Monitoring**
AWS CloudWatch monitors Lambda performance and logs.

1. **Access CloudWatch Logs**:
   - Go to the CloudWatch console.
   - View logs generated by Lambda functions.

2. **Set Up Alarms**:
   - Create CloudWatch Alarms to monitor Lambda performance and errors.
   - Configure notifications for critical issues.

![image](https://github.com/user-attachments/assets/b930c3d0-9c07-4948-aa75-a72089d05cc2)
 <!-- Add an image of the CloudWatch dashboard showing logs and alarms -->

## **Achievements**
- **Seamless Integration**: Combined frontend and AWS services for a scalable recommendation system.
- **Efficient Processing**: Utilized AWS Lambda and Bedrock for keyword generation and recommendation.
- **Scalable Hosting**: Deployed the frontend on S3 with optional CDN for enhanced performance.

![image](https://github.com/user-attachments/assets/63b101f7-5d2b-4c64-b483-c6719b93e99c)


