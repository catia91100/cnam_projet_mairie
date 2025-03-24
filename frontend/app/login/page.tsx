"use client";
import { useState } from "react";
import API_URL from "../config";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${API_URL}/security/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        // Stocker les informations utilisateur dans un cookie ou localStorage
        document.cookie = `user=${encodeURIComponent(
          JSON.stringify(data.user)
        )}; path=/; max-age=3600;`;
        window.location.href = "/";
      } else {
        setErrorMessage(data.message || "Email ou mot de passe incorrect!");
      }
    } catch (error) {
      setErrorMessage("Une erreur est survenue lors de la connexion.");
    }
  };

  return (
    <main className="mt-[1rem] flex justify-center items-center flex-col">
      <h1 className="text-2xl my-5">Formulaire de connexion</h1>
      <form className="grid gap-3" onSubmit={handleSubmit}>
        {errorMessage && (
          <div role="alert" className="alert alert-error">
            <span>{errorMessage}</span>
          </div>
        )}

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="email"
            className="grow"
            placeholder="Email"
            required
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="password"
            className="grow"
            placeholder="Mot de passe"
            required
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        <a className="link text-end text-sm" href="/password/reset">
          Réinitialisation mot de passe
        </a>
        <button className="btn text-white bg-[var(--color-1)]" type="submit">
          Connexion
        </button>
      </form>
    </main>
  );
}

export default Login;
