package org.toki.neoplugin.events;

import java.util.Collection;
import java.util.logging.Logger;

import org.bukkit.Bukkit;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.scheduler.BukkitRunnable;
import org.bukkit.scheduler.BukkitTask;
import org.json.JSONObject;
import org.toki.neoplugin.NeoPlugin;

public class PlayerCountListener implements Listener {
    private static final long INTERVAL = 6000L; // 5 minutes in ticks 
    private BukkitTask playerCountTask = null;
    private Logger logger = NeoPlugin.logger();

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        if (playerCountTask == null) {
            startPlayerCountTask();
        }
    }

    private void startPlayerCountTask() {
        logger.info("[NeoPlugin] Player joined - Started player count task");
        playerCountTask = new BukkitRunnable() {
            @Override
            public void run() {
                logger.info("[NeoPlugin] Continuing player count task");
                sendUpdatedPlayerCount();
            }
        }.runTaskTimer(NeoPlugin.getInstance(), 0L, INTERVAL);
    }

    private void stopPlayerCountTask() {
        logger.info("[NeoPlugin] Stopping player count task");
        if (playerCountTask != null) {
            playerCountTask.cancel();
            playerCountTask = null;
        }
        else {
            logger.info("[NeoPlugin] Tried to stop player count task with playerCountTask == null");
        }
    }

    private void sendUpdatedPlayerCount() {
        if (NeoPlugin.getWebSocket() == null) return;

        Collection<?> onlinePlayers = Bukkit.getOnlinePlayers();
        if (onlinePlayers.isEmpty() && playerCountTask != null) {
            stopPlayerCountTask();
        }

        logger.info("[NeoPlugin] Going to send player update signal with IP: " + Bukkit.getIp() + " and Player Count: " + onlinePlayers.size());

        JSONObject json = new JSONObject();
        json.put("mc_ip", Bukkit.getIp());
        json.put("type", "PLAYER_COUNT_UPDATE");
        json.put("player_count", onlinePlayers.size());

        // Send to discord bot
        try {
            logger.info("[NeoPlugin] Attempting to send player count update signal");
            NeoPlugin.getWebSocket().sendSignal(json.toString());
        } catch (Exception e) {
            logger.info("[NeoPlugin] Error sending player count update: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
