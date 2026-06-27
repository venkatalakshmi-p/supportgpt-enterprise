"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    setChatHistory((prev) => [...prev, { sender: "user", text: userMessage }]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });
      const data = await res.json();
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: data.answer },
      ]);
    } catch {
      setChatHistory((prev) => [
        ...prev,
        { sender: "bot", text: "Error: Could not connect to server." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", padding: "20px" }}>
      <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
        SupportGPT Enterprise
      </h1>

      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "8px",
          height: "400px",
          overflowY: "auto",
          padding: "16px",
          marginBottom: "16px",
        }}
      >
        {chatHistory.map((chat, i) => (
          <div
            key={i}
            style={{
              textAlign: chat.sender === "user" ? "right" : "left",
              margin: "8px 0",
            }}
          >
            <span
              style={{
                background: chat.sender === "user" ? "#0070f3" : "#eee",
                color: chat.sender === "user" ? "white" : "black",
                padding: "8px 12px",
                borderRadius: "12px",
                display: "inline-block",
                maxWidth: "80%",
              }}
            >
              {chat.text}
            </span>
          </div>
        ))}
        {loading && <p>Typing...</p>}
      </div>

      <div style={{ display: "flex", gap: "8px" }}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={sendMessage}
          style={{
            padding: "10px 20px",
            borderRadius: "8px",
            background: "#0070f3",
            color: "white",
            border: "none",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}