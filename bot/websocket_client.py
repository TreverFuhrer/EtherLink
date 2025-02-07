import asyncio
import json
import websockets
import os
from dotenv import load_dotenv
from handlers import chat_handler

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")

# Event dictionary: Maps events to handler functions
EVENTS = {
    "CHAT_MESSAGE": chat_handler.process_chat_message
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
    """ Handles incoming WebSocket messages. """
    signal = await websocket.recv()                
    data = json.loads(signal)
    event_type = data.get("type")
    request_id = data.get("request_id")

    # Check if this is a response to a pending request
    if request_id and request_id in pending_requests:
        pending_requests[request_id].set_result(data)
    else:
        # Route the signal to the correct event handler
        handler = EVENTS.get(event_type)
        if handler:
            await handler(data)
        else:
            print(f"Unrecognized event type: {event_type}")


# Send signal message to plugin
async def send_signal(message_type, data, ctx=None):
    """Send a JSON message to the WebSocket server."""
    if plugin_connection:
        signal = {"type": message_type, **data}
        await plugin_connection.send(json.dumps(signal))
    else:
        error_msg = "Error, WebSocket connection not established."
        if ctx:
            await ctx.reply(error_msg, ephemeral=True)  # Send error message to the user
        else:
            print(error_msg)


pending_requests = {}

async def send_request(message_type, data, timeout=5):
    """ Sends a request to the WebSocket server and waits for a response. """
    if not plugin_connection:
        return {"error": "WebSocket connection not established"}

    # Create a unique request ID
    request_id = f"{message_type}-{data.get('username', 'unknown')}-{os.urandom(4).hex()}"
    data["request_id"] = request_id  # Attach request ID

    # Create an asyncio.Future to wait for a response
    future = asyncio.Future()
    pending_requests[request_id] = future

    try:
        # Send the request
        await plugin_connection.send(json.dumps({"type": message_type, **data}))

        # Wait for response or timeout
        response = await asyncio.wait_for(future, timeout)
        return response
    except asyncio.TimeoutError:
        return {"error": "Request timed out"}
    finally:
        pending_requests.pop(request_id, None)  # Cleanup