package org.toki.neoplugin.events;

import org.bukkit.event.Listener;

import org.bukkit.event.EventHandler;
import org.json.JSONObject;
import org.toki.neoplugin.websocket.InitWebSocket;

import io.papermc.paper.event.player.AsyncChatEvent;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.serializer.gson.GsonComponentSerializer;

public class ChatListener implements Listener {

    private final InitWebSocket webSocket;

    public ChatListener(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    @EventHandler
    public void onPlayerChat(AsyncChatEvent event) {
        String username = event.getPlayer().getName();
        Component messageComponent = event.message();

        // Serialize the Component to a JSON string
        String messageJson = GsonComponentSerializer.gson().serialize(messageComponent);

        // Create a JSON object for the chat message
        JSONObject json = new JSONObject(); 
        json.put("type", "CHAT_MESSAGE");
        json.put("username", username);
        json.put("message", messageJson);

        // Send to discord bot
        webSocket.sendSignal(json.toString());
    }
    
}
