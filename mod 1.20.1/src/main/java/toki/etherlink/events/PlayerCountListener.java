package toki.etherlink.events;

import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.server.MinecraftServer;
import org.json.JSONObject;
import org.slf4j.Logger;

import toki.etherlink.EtherLink;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

public class PlayerCountListener {
    private static final Logger LOGGER = EtherLink.LOGGER;
    private static final long INTERVAL = 300; // 5 minutes in seconds
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
    private ScheduledFuture<?> playerCountTask = null;

    public void register() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            synchronized (this) {
                if (playerCountTask == null || playerCountTask.isCancelled()) {
                    startPlayerCountTask(server);
                }
            }
        });
        LOGGER.info("[EtherLink] PlayerCountListener registered successfully.");
    }

    private void startPlayerCountTask(MinecraftServer server) {
        LOGGER.info("[EtherLink] Starting player count task.");
        playerCountTask = scheduler.scheduleAtFixedRate(() -> {
            sendUpdatedPlayerCount(server);
        },1, INTERVAL, TimeUnit.SECONDS);
    }

    private void stopPlayerCountTask() {
        LOGGER.info("[EtherLink] Stopping player count task.");
        if (playerCountTask != null) {
            playerCountTask.cancel(false);
            playerCountTask = null;
        }
    }

    private void sendUpdatedPlayerCount(MinecraftServer server) {
        if (EtherLink.getWebSocket() == null) return;

        int playerCount = server.getPlayerManager().getCurrentPlayerCount();
        String mcIp = server.getServerIp();

        if (playerCount == 0 && playerCountTask != null) {
            stopPlayerCountTask();
        }

        LOGGER.info("[NeoPlugin] Going to send player update signal with IP: " + mcIp + " and Player Count: " + playerCount);

        JSONObject json = new JSONObject();
        json.put("mc_ip", mcIp);
        json.put("type", "PLAYER_COUNT_UPDATE");
        json.put("player_count", playerCount);

        try {
            EtherLink.getWebSocket().sendSignal(json.toString());
            LOGGER.info("[EtherLink] Sent player count update: " + playerCount);
        } catch (Exception e) {
            LOGGER.error("[EtherLink] Error sending player count update: " + e.getMessage(), e);
        }
    }

    // Ensure the scheduler is properly shut down when the server stops
    public void shutdown() {
        LOGGER.info("[EtherLink] Shutting down scheduler.");
        scheduler.shutdown();
        try {
            if (!scheduler.awaitTermination(60, TimeUnit.SECONDS)) {
                scheduler.shutdownNow();
                if (!scheduler.awaitTermination(60, TimeUnit.SECONDS))
                    LOGGER.error("[EtherLink] Scheduler did not terminate.");
            }
        } catch (InterruptedException ie) {
            scheduler.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
