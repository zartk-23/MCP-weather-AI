import json

def handler(event, context = None):
    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        msg = body['message'].lower()
        if 'hi' in msg:
            response = "Hello! I'm your MCP AI. Ask about weather!"
        elif 'weather' in msg:
            response = "It's 22°C and sunny in London! ☀️"
        else:
            response = f"You said: {body['message']}"
        return {
            'statusCode': 200,
            'body': json.dumps({'response': response})
        }
    return {
        'statusCode': 200,
        'body': json.dumps({'response': 'API ready! Send POST with {"message": "hi"}'})
    }
