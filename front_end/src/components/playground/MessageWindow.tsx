"use client";

import { useRef, useEffect } from "react";
import { Message } from "ai";
import SentientIcon from "@/assets/SentientSvg";

interface MessageWindowProps {
  messages: Message[];
  isLoading: boolean;
}

export function MessageWindow({ messages, isLoading }: MessageWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${
            message.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          {message.role !== "user" && (
            <div className="mr-2 flex items-center">
              <SentientIcon />
            </div>
          )}
          <div
            className={`max-w-3xl p-3 rounded-lg ${
              message.role === "user"
                ? "bg-blue-400 text-white"
                : "bg-white text-gray-800"
            }`}
          >
            {message.role === "user" ? message.content : ""}
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-gray-200 p-3 rounded-lg">
            <TypingIndicator />
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex items-center space-x-2">
      <div className="animate-pulse text-gray-900">Analyzing...</div>
    </div>
  );
}
