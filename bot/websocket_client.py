import asyncio
import json
import websockets
import os
from dotenv import load_dotenv
from handlers import chat_handler
#, whitelist_handler  # Import event handlers

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")

# Event dictionary: Maps events to handler functions
EVENTS = {
    "CHAT_MESSAGE": chat_handler.process_chat_message
    #"WHITELIST_REQUEST": whitelist_handler.process_whitelist_request
}

# Global Variable
plugin_connection = None

# Connect bot to plugin websocket server
async def connect_to_websocket():
    global plugin_connection
    attempts = 0
    sleep_duration = 10
    if (attempts > 12):
        sleep_duration = 60

    while True:
        try:
            async with websockets.connect(
                WEBSOCKET_URL,
                extra_headers={"AUTH_TOKEN": AUTH_TOKEN}
            ) as websocket:
                print("Connected to the WebSocket server.")
                plugin_connection = websocket
                # Handle plugin signal messages
                while True:
                    await handle_signals(websocket)
        except (websockets.ConnectionClosedError, ConnectionRefusedError) as e:
            print(f"WebSocket connection lost: {e}. Retrying in {sleep_duration} seconds...")
            plugin_connection = None
            attempts += 1
            await asyncio.sleep(sleep_duration) # Wait before retrying
        except OSError as e:
            print(f"Connection attempt failed: {e}. Retrying in {sleep_duration} seconds...")
            plugin_connection = None
            attempts += 1
            await asyncio.sleep(sleep_duration) # Wait before retrying
        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(sleep_duration) # Wait before retrying


# Handle incoming signal message
async def handle_signals(websocket):
    signal = await websocket.recv()
    #print(f"Received from Minecraft server: {signal}")
                
    # Parse the signal as JSON
    data = json.loads(signal)
    event_type = data.get("type")

    # Route the signal to the correct event handler
    handler = EVENTS.get(event_type)
    if handler:
        await handler(data)
    else:
        print(f"Unrecognized event type: {event_type}")


# Send signal message to plugin
async def send_signal(message_type, data):
    """Send a JSON message to the WebSocket server."""
    if plugin_connection:
        signal = {"type": message_type, **data}
        await plugin_connection.send(json.dumps(signal))
    else:
        print("WebSocket connection not established.")

# Send signal message to plugin
async def send_signal(message_type, data, interaction):
    """Send a JSON message to the WebSocket server."""
    if plugin_connection:
        signal = {"type": message_type, **data}
        await plugin_connection.send(json.dumps(signal))
    else:
        await interaction.response.send_message("WebSocket connection not established.", ephemeral=True)
        print("WebSocket connection not established.")


# Start client
def start_websocket_client():
    asyncio.create_task(connect_to_websocket())