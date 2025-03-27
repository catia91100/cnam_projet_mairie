"use client";
import { useState } from "react";
import API_URL from "@/app/config";

function ResetPasswordRequest() {
  const [email, setEmail] = useState("");
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/security/reset-request/${email}`
      );

      if (!response.ok) {
        throw new Error("Erreur lors de l'envoi de la demande.");
      }

      setSuccess(true);
    } catch () {
      setError("Impossible d'envoyer la demande. Vérifiez votre email.");
    }
  };

  return (
    <main className="mt-[1rem] flex justify-center items-center flex-col relative">
      <h1 className="text-2xl my-5">Réinitialisation du mot de passe</h1>

      {success ? (
        <p className="text-green-500 text-center">
          Un email de réinitialisation a été envoyé. Veuillez vérifier votre
          boîte de réception.
        </p>
      ) : (
        <form className="grid gap-3 w-80" onSubmit={handleSubmit}>
          {error && <p className="text-red-500">{error}</p>}

          <input
            type="email"
            className="input input-bordered"
            placeholder="Votre adresse email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button className="btn text-white bg-[var(--color-1)]" type="submit">
            Envoyer le lien de réinitialisation
          </button>
        </form>
      )}
    </main>
  );
}

export default ResetPasswordRequest;
