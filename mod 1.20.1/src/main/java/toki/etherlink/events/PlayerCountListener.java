package toki.etherlink.events;

import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.server.MinecraftServer;
import org.json.JSONObject;
import toki.etherlink.websocket.InitWebSocket;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class PlayerCountListener {
    private static final long COOLDOWN_INTERVAL = 301000; // 5 minutes + 1 seconds (ms)
    private final InitWebSocket webSocket;
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
    private long lastUpdateTime = 0;
    private boolean pendingUpdate = false;
    
    public PlayerCountListener(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    public void register() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> handlePlayerChange(server));
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> handlePlayerChange(server));
    }

    private synchronized void handlePlayerChange(MinecraftServer server) {
        long currentTime = System.currentTimeMillis();
        if (currentTime - lastUpdateTime >= COOLDOWN_INTERVAL) {
            sendUpdatedPlayerCount(server);
            lastUpdateTime = currentTime;
        } 
        else if (!pendingUpdate) {
            pendingUpdate = true;
            long delay = (COOLDOWN_INTERVAL - (currentTime - lastUpdateTime)) / 1000;
            scheduler.schedule(() -> {
                if (pendingUpdate) {
                    sendUpdatedPlayerCount(server);
                    pendingUpdate = false;
                    lastUpdateTime = System.currentTimeMillis();
                }
            }, Math.max(2, delay), TimeUnit.SECONDS);
        }
    }

    private void sendUpdatedPlayerCount(MinecraftServer server) {
        try {
            if (webSocket == null || server == null) return;
            int playerCount = server.getPlayerManager().getCurrentPlayerCount();
            JSONObject json = new JSONObject();
            json.put("mc_ip", server.getServerIp());
            json.put("type", "PLAYER_COUNT_UPDATE");
            json.put("player_count", playerCount);
            webSocket.sendSignal(json.toString());
        } catch (Exception e) {
            System.err.println("Error sending player count update: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
