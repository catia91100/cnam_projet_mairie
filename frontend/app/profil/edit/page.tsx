"use client";
import GetCookie from "@/app/_fct/GetCookie";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import API_URL from "@/app/config";

function ProfilEdit() {
  const [data, setData] = useState(null);
  const [token, setToken] = useState(null);
  const [handleUser, setHandleUser] = useState({});
  const [passwordIsReset, setPasswordIsReset] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const cookieStr = GetCookie({ name: "user" });
    if (cookieStr) {
      const cookie = JSON.parse(decodeURIComponent(cookieStr));
      setToken(cookie.token);
    } else {
      router.push("/"); // Redirection si le cookie n'est pas trouvé
    }
  }, [router]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_URL}/account`, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setData(data);
        // Initialiser handleUser avec les valeurs actuelles de l'utilisateur
        setHandleUser({
          email: data.email, // Ajout de l'email dans l'état pour la modification
          birth_at: new Date(data.birth_at).toISOString().split("T")[0],
          firstname: data.firstname,
          lastname: data.lastname,
        });
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
    };

    if (token) {
      fetchData();
    }
  }, [token]);

  if (!data) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }

  const user = data;

  function handleChange(e) {
    const { id, value } = e.target;
    setHandleUser((prevState) => ({
      ...prevState,
      [id]: value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();

    // Ajoutez l'email modifié au body si nécessaire
    const userNew = {
      email: handleUser.email || user.email, // Si l'email est modifié, il est inclus
      birth_at: handleUser.birth_at,
      firstname: handleUser.firstname || user.firstname,
      lastname: handleUser.lastname || user.lastname,
    };

    try {
      const response = await fetch(`${API_URL}/account/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(userNew),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      // const message =
      //   data.success === "User updated successfully" ||
      //   data.success === "No changes to update."
      //     ? "User updated successfully"
      //     : "Error updating user";

      // Si data contient 'new_email', rediriger vers profil avec le nouvel email
      if (data.user.new_email) {
        router.push(`/profil?new_email=${data.user.new_email}`);
      } else {
        router.push(`/profil?success=${true}`);
      }
    } catch (error) {
      console.error("Erreur lors de la mise à jour du profil:", error);
    }
  }

  async function handlePasswordReset(e) {
    try {
      e.preventDefault();
      const response = await fetch(`${API_URL}/security/reset-request/${handleUser.email}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      setPasswordIsReset(true);
      setShowModal(false);
    } catch (error) {
      console.error("Error sending password reset request:", error);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="relative space-y-6 max-w-lg mx-auto p-6 bg-white shadow-md rounded-lg"
    >
      <button
        type="button"
        className="absolute top-4 right-4 btn btn-secondary p-2 rounded-full w-12"
        onClick={() => {
          // Ajoutez votre lien de retour ici
          router.push("/profil");
        }}
      >
        ✕
      </button>

      <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
        Modifier votre profil
      </h1>

      <div className="grid gap-6">
        <label className="block">
          <span className="font-semibold text-gray-700">Email :</span>
          <input
            type="email"
            className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={handleUser.email}
            onChange={handleChange}
            id="email"
          />
        </label>

        <label className="block">
          <span className="font-semibold text-gray-700">Nom :</span>
          <input
            type="text"
            className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={handleUser.lastname}
            onChange={handleChange}
            id="lastname"
            required
          />
        </label>

        <label className="block">
          <span className="font-semibold text-gray-700">Prénom :</span>
          <input
            type="text"
            className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={handleUser.firstname}
            onChange={handleChange}
            id="firstname"
          />
        </label>

        <label className="block">
          <span className="font-semibold text-gray-700">
            Date de naissance :
          </span>
          <input
            type="date"
            className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={handleUser.birth_at}
            onChange={handleChange}
            id="birth_at"
            required
          />
        </label>
      </div>
      <div className="flex">
        <button
          type="button"
          className="btn btn-warning w-full max-w-xs mx-auto my-4 rounded-full"
          onClick={() => setShowModal(true)}
          disabled={passwordIsReset}
        >
          Réinitialiser le mot de passe
        </button>
      </div>

      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <p className="mb-4 text-gray-700">
              Confirmez-vous la réinitialisation du mot de passe ?
            </p>
            <div className="flex justify-center space-x-4">
              <button
                className="btn btn-error rounded-full"
                onClick={() => setShowModal(false)}
              >
                Annuler
              </button>
              <button
                className="btn btn-success rounded-full"
                onClick={handlePasswordReset}
              >
                Confirmer
              </button>
            </div>
          </div>
        </div>
      )}
      <div className="flex">
        <button
          type="submit"
          className="btn text-white bg-[var(--color-1)] w-full max-w-xs mx-auto mt-8 p-3 rounded-full"
        >
          Sauvegarder
        </button>
      </div>
    </form>
  );
}

export default ProfilEdit;
