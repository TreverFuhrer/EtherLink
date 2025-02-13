import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

# Database credentials
DB_HOST1 = os.getenv("DB_HOST1")
DB_PORT1 = int(os.getenv("DB_PORT1"))
DB_USER1 = os.getenv("DB_USER1")
DB_PASSWORD1 = os.getenv("DB_PASSWORD1")
DB_NAME1 = os.getenv("DB_NAME1")

# Connect to the database
try:
    conn = pymysql.connect(
        host=DB_HOST1,
        port=DB_PORT1,
        user=DB_USER1,
        password=DB_PASSWORD1,
        database=DB_NAME1
    )
    cursor = conn.cursor()
    print("[Database] Connection successful!")
except Exception as e:
    print(f"[Database] Connection failed: {e}")


def add_server(discord_id, mc_ip, websocket_url):
    """Links a Discord server with a Minecraft server."""
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO linked_servers (discord_server_id, minecraft_server_ip, websocket_url) 
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (discord_id, mc_ip, websocket_url))
        conn.commit()
        return "Server added successfully!"
    except pymysql.err.IntegrityError:
        return "This Discord server is already linked to a Minecraft server."

def get_all_servers():
    """Returns a dictionary of all Discord servers and their WebSocket URLs."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT discord_server_id, minecraft_server_ip, websocket_url FROM linked_servers")
        results = cursor.fetchall()
        return {
            discord_id: {"minecraft_server_ip": mc_ip, "websocket_url": websocket_url}
            for discord_id, mc_ip, websocket_url in results
        }

def add_channel(discord_id, channel_id, channel_name):
    """Adds a new channel to the linked Discord server."""
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO server_channels (discord_server_id, channel_id, channel_name) 
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (discord_id, channel_id, channel_name))
        conn.commit()
        return f"Channel `{channel_name}` added successfully!"
    except Exception as e:
        return f"Error adding channel: {e}"

def get_channels(discord_id):
    """Retrieves all stored channels for a Discord server."""
    with conn.cursor() as cursor:
        sql = "SELECT channel_id, channel_name FROM server_channels WHERE discord_server_id = %s"
        cursor.execute(sql, (discord_id,))
        results = cursor.fetchall()
        return {name: channel_id for channel_id, name in results}
    
def get_discord_id(mc_ip):
    """Retrieves the Discord server ID associated with a Minecraft server IP."""
    with conn.cursor() as cursor:
        sql = "SELECT discord_server_id FROM linked_servers WHERE minecraft_server_ip = %s"
        cursor.execute(sql, (mc_ip,))
        result = cursor.fetchone()
        return result[0] if result else None

def remove_server(discord_id):
    """Removes a Discord server and all associated channels."""
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM linked_servers WHERE discord_server_id = %s"
            cursor.execute(sql, (discord_id,))
        conn.commit()
        return f"Server `{discord_id}` and all its channels have been removed."
    except Exception as e:
        return f"Error removing server: {e}"

def remove_channel(discord_id, channel_name):
    """Removes a specific channel from the linked Discord server."""
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM server_channels WHERE discord_server_id = %s AND channel_name = %s"
            cursor.execute(sql, (discord_id, channel_name))
        conn.commit()
        return f"Channel `{channel_name}` has been removed successfully!"
    except Exception as e:
        return f"Error removing channel: {e}"