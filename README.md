# Inference Gateway

## Overview
The Inference Gateway provides a proxy endpoint for model inference requests, allowing seamless interaction with deployed models in OICM.

## API Endpoint
```
PATH: /models/{model_id}/proxy/{path:path}
```

### Path Parameters
- `model_id`: Identifier of the deployed model in OICM
- `path`: Resource path of the upstream model service (e.g., v1/chat/completions)

## HTTP Methods
- GET
- POST

## Authentication
Authentication is required via the Authorization header using a Bearer token:
```
Authorization: Bearer {token}
```
The token must be a valid API Key obtained from the OICM application and associated with the specified `model_id`.

## Headers
All request headers are proxied to the upstream service as-is. Notable headers include:

## Request Payload
The gateway accepts any payload format that is supported by the target model. 

### Streaming Configuration
Streaming can be enabled through two methods:
1. Setting the `Accept: text/event-stream` header
2. Including `{"stream": true}` in the JSON payload

## Response
The response format matches the output produced by the target model. The response will be delivered in streaming mode when either:
- The `Accept: text/event-stream` header is present in the request
- The request payload is a JSON object containing `{"stream": true}`

## Examples

### Basic Request
```http
POST https://inference.develop.openinnovation.ai/models/42c4f31d-9f7d-4f64-b8ad-3c63ada3df53/proxy/v1/chat/completions
Authorization: Bearer your-api-key
Content-Type: application/json

{
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}
```

### Streaming Request
```http
POST /models/gpt-4/proxy/chat/completions
Authorization: Bearer your-api-key
Accept: text/event-stream
Content-Type: application/json

{
    "messages": [
        {"role": "user", "content": "Hello"}
    ],
    "stream": true
}
```
