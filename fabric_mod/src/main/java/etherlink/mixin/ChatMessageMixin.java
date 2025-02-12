package etherlink.mixin;

import etherlink.websocket.InitWebSocket;
import net.minecraft.network.packet.c2s.play.ChatMessageC2SPacket;
import net.minecraft.server.network.ServerPlayNetworkHandler;
import net.minecraft.server.network.ServerPlayerEntity;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(ServerPlayNetworkHandler.class)
public class ChatMessageMixin {
    private static final Logger LOGGER = LoggerFactory.getLogger("etherlink");
    private final InitWebSocket ws;

    public ChatMessageMixin(InitWebSocket webSocket) {
        this.ws = webSocket;
    }

    @Inject(method = "onChatMessage", at = @At("HEAD"))
    private void onChatMessage(ChatMessageC2SPacket packet, CallbackInfo info) {
        ServerPlayNetworkHandler handler = (ServerPlayNetworkHandler) (Object) this;
        ServerPlayerEntity player = handler.player;
        String message = packet.chatMessage();

        // Process the chat message
        handleChatMessage(player, message);
    }

    private void handleChatMessage(ServerPlayerEntity player, String message) {
        String username = player.getEntityName();
        String mcIp = player.getServer().getServerIp();

        // Create a JSON object for the chat message
        JSONObject json = new JSONObject();
        json.put("mc_ip", mcIp);
        json.put("type", "CHAT_MESSAGE");
        json.put("username", username);
        json.put("message", message);

        // Send to Discord bot
        ws.sendSignal(json.toString());

        LOGGER.info("Processed chat message from {}: {}", username, message);
    }
}
