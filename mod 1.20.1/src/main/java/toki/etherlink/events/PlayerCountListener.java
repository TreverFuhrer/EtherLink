package toki.etherlink.events;

import org.json.JSONObject;

import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.server.MinecraftServer;
import toki.etherlink.websocket.InitWebSocket;

public class PlayerCountListener {
    private final InitWebSocket webSocket;

    public PlayerCountListener(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    public void register() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            sendUpdatedPlayerCount(server);
        });
        ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {
            sendUpdatedPlayerCount(server);
        });
    }

    // Send signal of type PLAYER_COUNT_UPDATE to websocket client
    private void sendUpdatedPlayerCount(MinecraftServer server) {
        String mc_ip = server != null ? server.getServerIp() : "Unknown";
        int playerCount = server.getCurrentPlayerCount();;

        JSONObject json = new JSONObject();
        json.put("mc_ip", mc_ip);
        json.put("type", "PLAYER_COUNT_UPDATE");
        json.put("player_count", playerCount);

        // Log and send the message
        webSocket.sendSignal(json.toString());
    }
}
