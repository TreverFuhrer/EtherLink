package org.toki.neoplugin.websocket;

import org.json.JSONObject;

/**
 * Handles incoming signal from Discord Bot
 */
public class IncomingSignal {
    
    public static void routeSignal(String signal) {
        JSONObject json = new JSONObject(signal);
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
