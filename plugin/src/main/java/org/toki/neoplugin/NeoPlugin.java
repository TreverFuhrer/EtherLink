package org.toki.neoplugin;

import java.net.URI;

import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;
import org.toki.neoplugin.events.ChatListener;
import org.toki.neoplugin.websocket.WebSocketClient;

import io.github.cdimascio.dotenv.Dotenv;

public final class NeoPlugin extends JavaPlugin {

    private WebSocketClient webSocketClient;

    @Override // Startup
    public void onEnable() {
        Dotenv dotenv = Dotenv.configure().filename(".env").load();
        String wsUrl = dotenv.get("WEBSOCKET_URL");

        // Prevent null Url
        if (wsUrl == null) { 
            getLogger().severe("WebSocket URL not set in environment variables.");
            return;
        }

        // Attempt connection to websocket server
        try {
            URI serverUri = new URI(wsUrl);
            this.webSocketClient = new WebSocketClient(serverUri);
            this.webSocketClient.connectToServer();
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Register all event listeners
        Bukkit.getPluginManager().registerEvents(new ChatListener(webSocketClient), this);

        // Startup log message
        getLogger().info("NeoPlugin enabled and WebSocket client connected.");    
    }

    @Override // Close WebSocket connection when the plugin is disabled
    public void onDisable() {
        if (webSocketClient != null) webSocketClient.disconnectFromServer();
        getLogger().info("NeoPlugin disabled and WebSocket client disconnected.");
    }    
}
