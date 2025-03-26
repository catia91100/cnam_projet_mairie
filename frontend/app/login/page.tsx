"use client";
import { useState } from "react";
import API_URL from "@/app/config";
import { useSearchParams } from "next/navigation";
import ClearURL from "@/app/components/ClearURL";
import GetCookie from "../_fct/GetCookie";
import { useRouter } from "next/navigation";
import Link from "next/link";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const searchParams = useSearchParams();

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
  const successMessage = searchParams.get("success");
  ClearURL();
  return (
    <main className="mt-[1rem] flex justify-center items-center flex-col relative">
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
            autoComplete="username"
          />
        </label>

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="password"
            className="grow"
            placeholder="Mot de passe"
            required
            onChange={(event) => setPassword(event.target.value)}
            autoComplete="current-password"
          />
        </label>
        <Link className="link text-end text-sm" href="/password/reset">
          Réinitialisation mot de passe
        </Link>
        <button className="btn text-white bg-[var(--color-1)]" type="submit">
          Connexion
        </button>
      </form>
      {successMessage && (
        <div className="alert alert-info mb-6 absolute -top-7 mt-10 lg:mt-0">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            className="h-6 w-6 shrink-0 stroke-current mr-2"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <span>{decodeURIComponent(successMessage)}</span>
        </div>
      )}
    </main>
  );
}

export default Login;
