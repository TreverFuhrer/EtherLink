package org.toki.neoplugin.websocket;

import org.json.JSONObject;

/**
 * Handles incoming connection from Discord Bot
 */
public class IncomingConnection {
    
    public static void routeConnect(String data) {
        JSONObject json = new JSONObject(data);
        String eventType = json.getString("type");

        switch (eventType) {
            case "CHAT_MESSAGE":
                //ChatHandler.handleChatMessage(json);
                break;
            // Add more cases for other event types as needed
            default:
                System.out.println("Unknown event type: " + eventType);
        }
    }
}
