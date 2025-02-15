package org.toki.neoplugin.events;

import org.bukkit.Bukkit;
import org.bukkit.Server;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.scheduler.BukkitTask;
import org.json.JSONObject;
import org.toki.neoplugin.NeoPlugin;
import org.toki.neoplugin.websocket.InitWebSocket;


public class PlayerCountListener implements Listener {

    private final InitWebSocket webSocket;
    private static BukkitTask scheduledTask = null;

    public PlayerCountListener(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    // Join Event
    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        schedulePlayerCountUpdate();
    }

    // Leave Event
    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        schedulePlayerCountUpdate();
    }

    // Combine simultaneous event calls into one
    private void schedulePlayerCountUpdate() {
        // Cancel any existing scheduled update to avoid duplicates
        if (scheduledTask != null && !scheduledTask.isCancelled()) {
            scheduledTask.cancel();
        }

        // Schedule a single update for player count after a short delay
        scheduledTask = Bukkit.getScheduler().runTaskLater(
            NeoPlugin.getInstance(),
            this::sendUpdatedPlayerCount,
            5L // # ticks
            /*
             * Pure Vanilla (No proxies)	1-2 ticks (50-100ms)
             *  Proxies (Geyser/Floodgate)	3-5 ticks (150-250ms)
             *  Heavy Plugins (VoiceChat)	5 ticks (250ms)
             */
        );
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
