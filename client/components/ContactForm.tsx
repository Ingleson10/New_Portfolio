"use client";

import { FormEvent, useState } from "react";
import { sendContactMessage } from "@/lib/api";

type StatusType = "idle" | "loading" | "success" | "error";

export default function ContactForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");

  const [status, setStatus] = useState<StatusType>("idle");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    setStatus("loading");
    setError(null);

    if (!name || !email || !subject || !message) {
      setStatus("error");
      setError("Preencha todos os campos.");
      return;
    }

    try {
      await sendContactMessage({ name, email, subject, message });

      setStatus("success");
      setName("");
      setEmail("");
      setSubject("");
      setMessage("");
    } catch (err: unknown) {
      setStatus("error");

      // 🔧 correção do erro: Property 'message' does not exist on type '{}'
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Erro ao enviar mensagem.");
      }
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        maxWidth: "480px",
        display: "flex",
        flexDirection: "column",
        gap: "0.75rem",
      }}
    >
      <div>
        <label
          htmlFor="name"
          style={{
            display: "block",
            marginBottom: "0.25rem",
            fontSize: "0.9rem",
          }}
        >
          Nome
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{
            width: "100%",
            padding: "0.5rem 0.6rem",
            borderRadius: "0.4rem",
            border: "1px solid #ccc",
            fontSize: "0.95rem",
          }}
        />
      </div>

      <div>
        <label
          htmlFor="email"
          style={{
            display: "block",
            marginBottom: "0.25rem",
            fontSize: "0.9rem",
          }}
        >
          E-mail
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "0.5rem 0.6rem",
            borderRadius: "0.4rem",
            border: "1px solid #ccc",
            fontSize: "0.95rem",
          }}
        />
      </div>

      <div>
        <label
          htmlFor="subject"
          style={{
            display: "block",
            marginBottom: "0.25rem",
            fontSize: "0.9rem",
          }}
        >
          Assunto
        </label>
        <input
          id="subject"
          type="text"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          style={{
            width: "100%",
            padding: "0.5rem 0.6rem",
            borderRadius: "0.4rem",
            border: "1px solid #ccc",
            fontSize: "0.95rem",
          }}
        />
      </div>

      <div>
        <label
          htmlFor="message"
          style={{
            display: "block",
            marginBottom: "0.25rem",
            fontSize: "0.9rem",
          }}
        >
          Mensagem
        </label>
        <textarea
          id="message"
          rows={4}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{
            width: "100%",
            padding: "0.5rem 0.6rem",
            borderRadius: "0.4rem",
            border: "1px solid #ccc",
            fontSize: "0.95rem",
            resize: "vertical",
          }}
        />
      </div>

      {status === "error" && error && (
        <p style={{ color: "#b00020", fontSize: "0.9rem" }}>{error}</p>
      )}

      {status === "success" && (
        <p style={{ color: "#0a7b35", fontSize: "0.9rem" }}>
          Mensagem enviada com sucesso! 🚀
        </p>
      )}

      <button
        type="submit"
        disabled={status === "loading"}
        style={{
          marginTop: "0.5rem",
          padding: "0.6rem 1rem",
          borderRadius: "0.5rem",
          border: "none",
          backgroundColor: "#111827",
          color: "#fff",
          fontSize: "0.95rem",
          cursor: status === "loading" ? "wait" : "pointer",
          opacity: status === "loading" ? 0.8 : 1,
        }}
      >
        {status === "loading" ? "Enviando..." : "Enviar mensagem"}
      </button>
    </form>
  );
}
