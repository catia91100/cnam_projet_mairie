"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import API_URL from "../config";

function CompleterInscription() {
  const params = useSearchParams();
  const router = useRouter();
  const token = params.get("token");

  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [passwordErrors, setPasswordErrors] = useState([]);
  const [formData, setFormData] = useState({
    email: "",
    firstname: "",
    lastname: "",
    birth_at: "",
    password: "",
    confirmPassword: "",
    token: "",
  });

  useEffect(() => {
    if (!token) {
      router.push("/404");
      return;
    }

    fetch(`${API_URL}/security/validation-email?token=${token}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.email && data.token && data.verification === true) {
          setFormData((prev) => ({
            ...prev,
            email: data.email,
            token: data.token,
          }));
        } else {
          router.push("/404");
        }
      })
      .catch(() => {
        router.push("/404");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token, router]);

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
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (name === "password") validatePassword(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setErrorMessage("Les mots de passe ne correspondent pas.");
      return;
    }
    if (passwordErrors.length > 0) {
      setErrorMessage(
        "Le mot de passe ne respecte pas les critères de sécurité."
      );
      return;
    }

    const payload = {
      token: formData.token,
      user: {
        firstname: formData.firstname,
        lastname: formData.lastname,
        birth_at: formData.birth_at,
        password: formData.password,
      },
    };

    try {
      const response = await fetch(
        `${API_URL}/security/completer-inscription`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      );
      const data = await response.json();
      if (response.ok) {
        alert("Inscription complétée avec succès !");
        router.push("/login");
      } else {
        setErrorMessage(data.message || "Une erreur est survenue.");
      }
    } catch (err) {
      setErrorMessage("Impossible de contacter le serveur.");
    }
  };

  if (loading) return <p>Chargement...</p>;

  return (
    <main className="mt-[1rem] flex justify-center items-center flex-col">
      <h1 className="text-2xl my-5">Complétez votre inscription</h1>
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
            value={formData.email}
            disabled
          />
        </label>

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="text"
            name="lastname"
            className="grow"
            placeholder="Nom"
            value={formData.lastname}
            onChange={handleChange}
            required
          />
        </label>

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="text"
            name="firstname"
            className="grow"
            placeholder="Prénom"
            value={formData.firstname}
            onChange={handleChange}
            required
          />
        </label>

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="date"
            name="birth_at"
            className="grow"
            value={formData.birth_at}
            onChange={handleChange}
            required
          />
        </label>

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="password"
            name="password"
            className="grow"
            placeholder="Mot de passe"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </label>

        {passwordErrors.length > 0 && (
          <ul className="text-red-500">
            {passwordErrors.map((err, index) => (
              <li key={index}>{err}</li>
            ))}
          </ul>
        )}

        <label className="input input-bordered flex items-center gap-2">
          <input
            type="password"
            name="confirmPassword"
            className="grow"
            placeholder="Confirmer le mot de passe"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </label>

        <button
          className="btn text-white bg-[var(--color-1)]"
          type="submit"
          disabled={passwordErrors.length > 0}
        >
          S&apos;inscrire
        </button>
      </form>
    </main>
  );
}

export default CompleterInscription;
