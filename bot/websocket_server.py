import asyncio
import json
import websockets
from event_handlers import chat_handler
#, whitelist_handler  # Import event handlers

# Event dictionary, Routes to each event.py
EVENTS = {
    "CHAT_MESSAGE": chat_handler.process_chat_message
    #"WHITELIST_REQUEST": whitelist_handler.process_whitelist_request
}

# Handles incoming connection with Plugin
async def handle_connection(websocket, path):
    async for connection_data in websocket:
        data = json.loads(connection_data)
        event_type = data.get("type")
        
        # If event type is recognized
        # Calls respective handler function
        handler = EVENTS.get(event_type)
        if handler:
            await handler(data) # Call event
        else:
            print(f"Unrecognized event type: {event_type}")

# Function to start websocket
async def start_websocket_server():
    server = await websockets.serve(handle_connection, "localhost", 6789)
    print("WebSocket server started on ws://localhost:6789")
    await server.wait_closed()
