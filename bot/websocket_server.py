import asyncio
import json
import websockets
from event_handlers import chat_handler#, whitelist_handler  # Import event handlers

# Event dictionary to route each type to its handler
EVENT_ROUTERS = {
    "CHAT_MESSAGE": chat_handler.process_chat_message,
    #"WHITELIST_REQUEST": whitelist_handler.process_whitelist_request
}

async def handle_message(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        event_type = data.get("type")
        
        # Route to the appropriate handler if event type is recognized
        handler = EVENT_ROUTERS.get(event_type)
        if handler:
            # Call respective handler function
            await handler(data)  
        else:
            print(f"Unrecognized event type: {event_type}")

async def start_websocket_server():
    server = await websockets.serve(handle_message, "localhost", 6789)
    print("WebSocket server started on ws://localhost:6789")
    await server.wait_closed()
