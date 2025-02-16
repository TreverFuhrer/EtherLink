package org.toki.neoplugin.events;

import org.bukkit.Bukkit;
import org.bukkit.Server;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.scheduler.BukkitRunnable;
import org.bukkit.scheduler.BukkitTask;
import org.json.JSONObject;
import org.toki.neoplugin.NeoPlugin;
import org.toki.neoplugin.websocket.InitWebSocket;

public class PlayerCountListener implements Listener {
    private static final long COOLDOWN_INTERVAL = 302000; // 5 minutes + 2 seconds in milliseconds
    private long lastUpdateTime = 0;
    private boolean pendingUpdate = false;
    private static BukkitTask scheduledTask = null;

    private final InitWebSocket webSocket;

    public PlayerCountListener(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        handlePlayerChange();
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        handlePlayerChange();
    }

    private void handlePlayerChange() {
        long currentTime = System.currentTimeMillis();
        if (currentTime - lastUpdateTime >= COOLDOWN_INTERVAL) {
            sendUpdatedPlayerCount();
            lastUpdateTime = currentTime;
        } else if (!pendingUpdate) {
            pendingUpdate = true;
            long delay = Math.max(1, (COOLDOWN_INTERVAL - (currentTime - lastUpdateTime)) / 50); // Convert ms to ticks
            if (scheduledTask != null && !scheduledTask.isCancelled()) {
                scheduledTask.cancel();
            }
            scheduledTask = new BukkitRunnable() {
                @Override
                public void run() {
                    if (pendingUpdate) {
                        sendUpdatedPlayerCount();
                        pendingUpdate = false;
                        lastUpdateTime = System.currentTimeMillis();
                    }
                }
            }.runTaskLater(NeoPlugin.getInstance(), delay);
        }
    }

    private void sendUpdatedPlayerCount() {
        if (webSocket == null) return;

        Server server = Bukkit.getServer();
        int playerCount = server.getOnlinePlayers().size();

        JSONObject json = new JSONObject();
        json.put("mc_ip", server.getIp());
        json.put("type", "PLAYER_COUNT_UPDATE");
        json.put("player_count", playerCount);

        webSocket.sendSignal(json.toString());
    }
}
