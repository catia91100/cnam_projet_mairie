"use client";
import GetCookie from "@/app/_fct/GetCookie";
import { useState, useEffect } from "react";
import { redirect, useSearchParams } from "next/navigation";
import API_URL from "@/app/config";
import Link from "next/link";

function Profil() {
  const [data, setData] = useState(null);
  const [token, setToken] = useState(null);
  const searchParams = useSearchParams(); // Pour récupérer les paramètres de l'URL

  useEffect(() => {
    if (GetCookie({ name: "user" })) {
      let cookie = JSON.parse(decodeURIComponent(GetCookie({ name: "user" })));
      setToken(cookie.token);
    } else {
      return redirect("/");
    }
  }, []);

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
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
    };

    if (token) {
      fetchData();
    }
  }, [token]);

  if (data === null) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }

  let user = data; // Utilisation directe des données retournées

  // Récupérer les paramètres success et new_email de l'URL
  const successMessage = searchParams.get("success");
  const newEmailMessage = searchParams.get("new_email");
  return (
    <main className="grid gap-6 lg:grid-cols-6s lg:mx-40 lg:my-20 relative p-6 bg-white shadow-md rounded-lg">
      <div className="relative space-y-6 max-w-lg mx-auto p-6 bg-white shadow-md rounded-lg">
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
          Profil
        </h1>

        <div className="grid gap-6">
          <label className="block">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-gray-700">Email :</span>
              {user.role === "ROLE_ADMIN" && (
                // <div className="grid grid-cols-4 items-center lg:col-span-3">
                <span className="badge badge-primary col-span-3 rounded-full">
                  Admin
                </span>
                // </div>
              )}
            </div>
            <input
              type="email"
              className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={user.email}
              disabled
            />
          </label>

          <label className="block">
            <span className="font-semibold text-gray-700">Nom :</span>
            <input
              type="text"
              className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={user.lastname}
              disabled
            />
          </label>

          <label className="block">
            <span className="font-semibold text-gray-700">Prénom :</span>
            <input
              type="text"
              className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={user.firstname}
              disabled
            />
          </label>

          <label className="block">
            <span className="font-semibold text-gray-700">
              Date de naissance :
            </span>
            <input
              type="date"
              className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={new Date(user.birth_at).toISOString().split("T")[0]}
              disabled
            />
          </label>

          <label className="block">
            <span className="font-semibold text-gray-700">
              Date de création :
            </span>
            <input
              type="date"
              className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={new Date(user.created_at).toISOString().split("T")[0]}
              disabled
            />
          </label>

          <label className="block">
            <span className="font-semibold text-gray-700">
              Date de connexion :
            </span>
            <input
              type="date"
              className="input input-bordered w-full max-w-md mt-2 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={new Date(user.login_at).toISOString().split("T")[0]}
              disabled
            />
          </label>
        </div>
        <div>
          <Link
            className="btn text-white bg-[var(--color-1)] w-full max-w-xs mx-auto mt-8 p-3 rounded-full"
            href={"/profil/edit"}
          >
            Modifier
          </Link>
        </div>

        {/* Infobulle conditionnelle */}
        {(successMessage || newEmailMessage) && (
          <div className="alert alert-info mb-6 absolute -top-7 mt-10 lg:mt-0 rounded-full">
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
              {successMessage ? "Informations enregistrées" : null}
              {newEmailMessage
                ? "Informations enregistrées, un mail vous a été envoyé pour valider votre nouveau mail"
                : null}
            </span>
          </div>
        )}
      </div>
    </main>
  );
}

export default Profil;
