"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import API_URL from "../config";

function CompleterInscription() {
  const params = useSearchParams();
  const router = useRouter();
  const token = params.get("token");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
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
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (name === "password") {
      validatePassword(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setError("Les mots de passe ne correspondent pas.");
      return;
    }

    if (passwordErrors.length > 0) {
      setError("Le mot de passe ne respecte pas les critères de sécurité.");
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
        setError(data.message || "Une erreur est survenue.");
      }
    } catch (err) {
      setError("Impossible de contacter le serveur.");
    }
  };

  if (loading) {
    return <p>Chargement...</p>;
  }

  return (
    <div>
      <h1>Complétez votre inscription</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>Email :</label>
        <input type="email" name="email" value={formData.email} disabled />

        <label>Nom :</label>
        <input
          type="text"
          name="lastname"
          value={formData.lastname}
          onChange={handleChange}
          required
        />

        <label>Prénom :</label>
        <input
          type="text"
          name="firstname"
          value={formData.firstname}
          onChange={handleChange}
          required
        />

        <label>Date de naissance :</label>
        <input
          type="date"
          name="birth_at"
          value={formData.birth_at}
          onChange={handleChange}
          required
        />

        <label>Mot de passe :</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        {passwordErrors.length > 0 && (
          <ul style={{ color: "red" }}>
            {passwordErrors.map((err, index) => (
              <li key={index}>{err}</li>
            ))}
          </ul>
        )}

        <label>Répétez le mot de passe :</label>
        <input
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={passwordErrors.length > 0}>
          S&apos;inscrire
        </button>
      </form>
    </div>
  );
}

export default CompleterInscription;
