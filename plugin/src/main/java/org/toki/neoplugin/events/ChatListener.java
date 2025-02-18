package org.toki.neoplugin.events;

import org.bukkit.event.Listener;
import org.bukkit.Bukkit;
import org.bukkit.event.EventHandler;
import org.json.JSONObject;

import io.papermc.paper.event.player.AsyncChatEvent;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.serializer.gson.GsonComponentSerializer;
import org.toki.neoplugin.NeoPlugin;

public class ChatListener implements Listener {

    @EventHandler
    public void onPlayerChat(AsyncChatEvent event) {
        if (NeoPlugin.getWebSocket() == null) {
            System.err.println("Error: webSocket null at start of onPlayerChat");
            return;
        }
        String username = event.getPlayer().getName();
        Component messageComponent = event.message();
        String mc_ip = Bukkit.getServer().getIp();

        // Serialize the Component to a JSON string
        String messageJson = GsonComponentSerializer.gson().serialize(messageComponent);

        // Create a JSON object for the chat message
        JSONObject json = new JSONObject();
        json.put("mc_ip", mc_ip);
        json.put("type", "CHAT_MESSAGE");
        json.put("username", username);
        json.put("message", messageJson);

        // Send to discord bot
        try {
            NeoPlugin.getWebSocket().sendSignal(json.toString());
        } catch (Exception e) {
            System.err.println("Error sending player count update: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
}
