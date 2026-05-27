/**
 * hooks/useSocket.js — Socket.IO connection with real-time events
 */
import { useEffect, useRef } from "react";
import { io } from "socket.io-client";
import useStore from "../store/useStore";

let socketInstance = null;

export function useSocket() {
  const { addNotification, setOnlineCount } = useStore();
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    socketInstance = io("/", {
      transports: ["websocket", "polling"],
      reconnectionAttempts: 5,
      reconnectionDelay: 2000,
    });

    socketInstance.on("connect", () => {
      socketInstance.emit("notification_subscribe");
    });

    socketInstance.on("online_count", ({ count }) => {
      setOnlineCount(count);
    });

    socketInstance.on("live_notification", (notif) => {
      addNotification(notif);
    });

    return () => {
      socketInstance?.disconnect();
      initialized.current = false;
    };
  }, []);

  return socketInstance;
}

export function joinRoom(room) {
  socketInstance?.emit("join_room", { room });
}

export function sendMessage(room, message) {
  socketInstance?.emit("send_message", { room, message });
}

export function sendTyping(room) {
  socketInstance?.emit("typing", { room });
}

export function onMessage(cb) {
  socketInstance?.on("receive_message", cb);
  return () => socketInstance?.off("receive_message", cb);
}

export function onTyping(cb) {
  socketInstance?.on("user_typing", cb);
  return () => socketInstance?.off("user_typing", cb);
}

export function onSystemMessage(cb) {
  socketInstance?.on("system_message", cb);
  return () => socketInstance?.off("system_message", cb);
}
