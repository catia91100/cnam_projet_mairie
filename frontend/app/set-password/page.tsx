"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import API_URL from "@/app/config";
import GetCookie from "@/app/_fct/GetCookie";

function SetPassword() {
  const router = useRouter();
  const [message, setMessage] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordRepeat, setPasswordRepeat] = useState("");
  const [passwordErrors, setPasswordErrors] = useState([]); // Stocke les erreurs de validation
  const [successMessage, setSuccessMessage] = useState("");
  const [token, setToken] = useState(null);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const tokenParam = urlParams.get("token");

    if (tokenParam) {
      fetch(
        `${API_URL}/security/set-password?token=${encodeURIComponent(
          tokenParam
        )}`
      )
        .then((response) => {
          if (!response.ok) {
            return;
          }
          return response.json();
        })
        .then((data) => {
          if (data) {
            setToken(data.token);
            // setEmail(data.email);
          }
        });
      // .catch(() => router.push("/404"));
    }
  }, [router]);

  // Vérification de la force du mot de passe
  const validatePassword = (password) => {
    const errors = [];
    if (password.length < 8 || password.length > 64) {
      errors.push("Le mot de passe doit contenir entre 8 et 64 caractères.");
    }
    if (!/[A-Z]/.test(password)) {
      errors.push("Le mot de passe doit contenir au moins une majuscule.");
    }
    if (!/[a-z]/.test(password)) {
      errors.push("Le mot de passe doit contenir au moins une minuscule.");
    }
    if (!/\d/.test(password)) {
      errors.push("Le mot de passe doit contenir au moins un chiffre.");
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push(
        "Le mot de passe doit contenir au moins un caractère spécial."
      );
    }
    setPasswordErrors(errors);
    return errors.length === 0; // Retourne true si aucun problème
  };

  function handleSubmitPassword(e) {
    e.preventDefault();

    if (password !== passwordRepeat) {
      setMessage(true);
      setSuccessMessage("");
      setTimeout(() => setMessage(false), 3000);
      return;
    }

    if (!validatePassword(password)) {
      return; // Ne pas envoyer la requête si la validation échoue
    }

    fetch(`${API_URL}/security/set-password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ password, token }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Échec de la réinitialisation du mot de passe");
        }
        return response.json();
      })
      .then(() => {
        setSuccessMessage(
          "Mot de passe réinitialisé, vous pouvez vous connecter."
        );
        setMessage(false);
        const value = GetCookie({ name: "user" });

        if (value) {
          document.cookie =
            "user= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/";
        }
      })
      .catch(() => {
        setMessage(true);
        setTimeout(() => setMessage(false), 3000);
      });
  }

  if (successMessage) {
    return (
      <main className="mt-[1rem] flex justify-center items-center flex-col">
        <h1 className="text-2xl my-5">{successMessage}</h1>
      </main>
    );
  }

  if (!token) {
    return (
      <main className="mt-[1rem] flex justify-center items-center flex-col">
        <h1 className="text-2xl my-5 text-center">
          Formulaire de Réinitialisation de mot de passe
        </h1>
        <p>Chargement en cours...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen mt-[1rem] p-5 flex justify-center items-center flex-col">
      <h1 className="text-2xl my-5">Réinitialisation du mot de passe</h1>
      <form className="grid gap-3" onSubmit={handleSubmitPassword}>
        {message && (
          <div role="alert" className="alert alert-error">
            <span>Les deux mots de passe doivent être identiques.</span>
          </div>
        )}

        <input
          type="password"
          className="input input-bordered"
          placeholder="Nouveau mot de passe"
          required
          onChange={(e) => {
            setPassword(e.target.value);
            validatePassword(e.target.value);
          }}
        />
        {passwordErrors.length > 0 && (
          <ul className="text-red-500 text-sm">
            {passwordErrors.map((error, index) => (
              <li key={index}>⚠️ {error}</li>
            ))}
          </ul>
        )}

        <input
          type="password"
          className="input input-bordered"
          placeholder="Confirmez le mot de passe"
          required
          onChange={(e) => setPasswordRepeat(e.target.value)}
        />

        <button className="btn text-white bg-[var(--color-1)]" type="submit">
          Réinitialiser
        </button>
      </form>
    </main>
  );
}

export default SetPassword;
