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

    let userNew = {
      email: user.email,
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
      if (
        data.message === "User updated successfully" ||
        data.message === "No changes to update."
      ) {
        console.log("Mise à jour réussie");
        router.push("/profil");
      }
    } catch (error) {
      console.error("Erreur lors de la mise à jour du profil:", error);
    }
  }

  async function passwordReset() {
    if (confirm("Confirmer la demande de réinitialisation ?")) {
      try {
        const response = await fetch(`${API_URL}/reset_request/${user.email}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        setPasswordIsReset(true);
      } catch (error) {
        console.error("Error sending password reset request:", error);
      }
    }
  }

  return (
    <main className="grid gap-6 lg:mx-40 lg:my-20 px-4">
      {passwordIsReset && (
        <div role="alert" className="alert alert-info mb-6">
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
          <span>
            Un mail vous a été envoyé afin de réinitialiser votre mot de passe.
          </span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        <h2 className="text-2xl font-semibold text-center">
          Modifier votre profil
        </h2>

        <div className="flex items-center justify-between space-x-4">
          <span className="font-medium">Email :</span>
          <input
            type="email"
            className="input input-bordered w-full max-w-xl"
            value={user.email}
            disabled
          />
        </div>

        <button
          className="btn btn-warning w-full max-w-xs mx-auto my-4"
          onClick={passwordReset}
          disabled={passwordIsReset}
        >
          Réinitialiser le mot de passe
        </button>

        <div className="flex items-center justify-between space-x-4">
          <span className="font-medium">Nom :</span>
          <input
            type="text"
            className="input input-bordered w-full max-w-xl"
            value={handleUser.lastname}
            onChange={handleChange}
            id="lastname"
            required
          />
        </div>

        <div className="flex items-center justify-between space-x-4">
          <span className="font-medium">Prénom :</span>
          <input
            type="text"
            className="input input-bordered w-full max-w-xl"
            value={handleUser.firstname}
            onChange={handleChange}
            id="firstname"
          />
        </div>

        <div className="flex items-center justify-between space-x-4">
          <span className="font-medium">Date de naissance :</span>
          <input
            type="date"
            className="input input-bordered w-full max-w-xl"
            value={handleUser.birth_at}
            onChange={handleChange}
            id="birth_at"
            required
          />
        </div>

        <button
          className="btn text-white bg-[var(--color-1)] w-full max-w-xs mx-auto mt-8"
          type="submit"
        >
          Sauvegarder
        </button>
      </form>
    </main>
  );
}

export default ProfilEdit;
