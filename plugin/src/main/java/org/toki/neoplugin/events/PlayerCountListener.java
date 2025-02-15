package org.toki.neoplugin.events;

import org.bukkit.Bukkit;
import org.bukkit.Server;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.json.JSONObject;
import org.toki.neoplugin.websocket.InitWebSocket;


public class PlayerCountListener implements Listener {

    private final InitWebSocket webSocket;

    public PlayerCountListener(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        Bukkit.getLogger().info("[NeoPlugin] Player joined: " + event.getPlayer().getName());
        sendUpdatedPlayerCount();
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        Bukkit.getLogger().info("[NeoPlugin] Player left: " + event.getPlayer().getName());
        sendUpdatedPlayerCount();
    }

    // Send signal of type PLAYER_COUNT_UPDATE to websocket client
    private void sendUpdatedPlayerCount() {
        if (webSocket == null) return;
        Server server = Bukkit.getServer();
        String mc_ip = server.getIp();
        int playerCount = server.getOnlinePlayers().size();

        JSONObject json = new JSONObject();
        json.put("mc_ip", mc_ip);
        json.put("type", "PLAYER_COUNT_UPDATE");
        json.put("player_count", playerCount);

        // Log and send the message
        webSocket.sendSignal(json.toString());
    }
}
