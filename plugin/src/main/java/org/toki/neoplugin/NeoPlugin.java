package org.toki.neoplugin;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import org.bukkit.Bukkit;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.plugin.java.JavaPlugin;

import io.papermc.paper.event.player.AsyncChatEvent;
import net.kyori.adventure.text.serializer.plain.PlainTextComponentSerializer;

public final class NeoPlugin extends JavaPlugin implements Listener {

    @Override // Plugin startup logic
    public void onEnable() {
        Bukkit.getPluginManager().registerEvents(this, this);
    }

    @Override // Plugin shutdown logic
    public void onDisable() {
        // Clean up stuff on shutdown
    }

    /** Detect player chat event
     * Gets messsage of a player chat in game
     * @param event a AsyncChatEvent
     */
    @EventHandler
    public void onPlayerChat(AsyncChatEvent event) {
        String playerName = event.getPlayer().getName();
        String message = PlainTextComponentSerializer.plainText().serialize(event.message());

        sendChatMessageToDiscord(playerName, message);
    }

    private void sendChatMessageToDiscord(String playerName, String message) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            URI uri = URI.create("http://127.0.0.1:5000/minecraft_chat");
            String jsonInputString = String.format("{\"username\": \"%s\", \"message\": \"%s\"}", playerName, message);
    
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(uri)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonInputString))
                    .build();
    
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    
            if (response.statusCode() == 200) {
                System.out.println("Event sent to Discord bot successfully.");
            } else {
                System.out.println("Failed to send event: " + response.body());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
}
