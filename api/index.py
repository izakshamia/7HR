from server.card_info_server import app

def handler(event, context):
    # This function will be called by Vercel's serverless environment
    with app.test_request_context(path=event['path'], method=event['httpMethod']):
        response = app.full_dispatch_request()
        
        # Convert the response to the format Vercel expects
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }
