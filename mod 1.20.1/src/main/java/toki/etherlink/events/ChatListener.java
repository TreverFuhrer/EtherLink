package toki.etherlink.events;

import net.fabricmc.fabric.api.message.v1.ServerMessageEvents;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import toki.etherlink.websocket.InitWebSocket;

import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ChatListener {
    @SuppressWarnings("unused")
    private static final Logger LOGGER = LoggerFactory.getLogger("etherlink");
    private final InitWebSocket webSocket;

    public ChatListener(InitWebSocket webSocket) {
        this.webSocket = webSocket;
    }

    public void register() {
        ServerMessageEvents.CHAT_MESSAGE.register((message, sender, signedMessage) -> {
            ServerPlayerEntity player = sender;
            String username = player.getEntityName();
            MinecraftServer server = player.getServer();
            String mc_ip = server != null ? server.getServerIp() : "Unknown";

            // Get user chat message
            String chat = message.getContent().getString();

            // Create a JSON object for the chat message
            JSONObject json = new JSONObject();
            json.put("mc_ip", mc_ip);
            json.put("type", "CHAT_MESSAGE");
            json.put("username", username);
            json.put("message", chat);

            // Log and send the message
            webSocket.sendSignal(json.toString());
        });
    }
}
