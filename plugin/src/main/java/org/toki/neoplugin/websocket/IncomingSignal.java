package org.toki.neoplugin.websocket;

import org.bukkit.Bukkit;
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
            case "SERVER_CHAT":
                String command = "say " + json.getString("message");;
                Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), command);
                break;
            default:
                System.out.println("Unknown event type: " + eventType);
        }
    }
}
