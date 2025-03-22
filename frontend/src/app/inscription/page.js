"use client";
import { useState } from "react";

function Inscription() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [isSuccess, setIsSuccess] = useState(false); // Gérer l'état du succès
  const [responseMessage, setResponseMessage] = useState(""); // Message de succès ou d'erreur

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Vérifier si l'email est valide
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email");
      return;
    }

    try {
      // Les données envoyées doivent être sous ce format :
      // {
      //   "email": "test@email.com"
      // }
      const response = await fetch("http://backend:5000/security/inscription", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }), // Envoyer l'email dans le body
      });

      const data = await response.json();

      if (response.ok) {
        // Si la requête réussit (200 OK), afficher une alerte de succès
        setIsSuccess(true);
        setResponseMessage(`Inscription réussie avec l'email: ${data.email}`);
        setEmail(""); // Réinitialiser l'email après succès
        setError(""); // Réinitialiser l'erreur
      } else {
        // Si la réponse est une erreur 400
        if (response.status === 400) {
          setError(`Invalid data: ${data.error}`);
        }
        // Si la réponse est une erreur 409 (email déjà utilisé)
        else if (response.status === 409) {
          setError(data.error); // Email déjà utilisé
        }
        // Si la réponse est une erreur 500 (erreur serveur)
        else if (response.status === 500) {
          setError(`Server error: ${data.error}`);
        } else {
          setError("Une erreur s'est produite, veuillez réessayer.");
        }
      }
    } catch (err) {
      // Gérer les erreurs réseau ou autres exceptions
      setError("Erreur de réseau, veuillez réessayer.");
    }
  };

  const handleAlertClose = () => {
    // Après que l'alerte est fermée, l'input se vide et l'état est réinitialisé
    setIsSuccess(false);
    setResponseMessage(""); // Réinitialiser le message
  };

  return (
    <div>
      <h1>Inscription</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">S&apos;inscrire</button>
      </form>

      {/* Afficher l'alerte si l'inscription a réussi */}
      {isSuccess && (
        <div>
          <div style={{ color: "green", marginTop: "20px" }}>
            <p>{responseMessage}</p>
            <button onClick={handleAlertClose}>Fermer</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Inscription;
