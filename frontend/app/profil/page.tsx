"use client";
import GetCookie from "../_fct/GetCookie";
import { useState, useEffect } from "react";
import { redirect } from "next/navigation";
import API_URL from "../config";

function Profil() {
  const [data, setData] = useState(null);
  const [token, setToken] = useState(null);

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

  return (
    <main className="grid gap-3 lg:grid-cols-6 lg:mx-40 lg:my-20">
      <h1 className="text-2xl my-5">Profil</h1>

      {/* Affichage des informations de l'utilisateur */}
      <div className="grid grid-cols-4 items-center lg:col-span-3">
        <span className="">Email :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="text" className="grow" value={user.email} disabled />
        </label>
      </div>
      <div className="grid grid-cols-4 items-center lg:col-span-3">
        <span className="">Nom :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="text" className="grow" value={user.lastname} disabled />
        </label>
      </div>
      <div className="grid grid-cols-4 items-center lg:col-span-3">
        <span className="">Prénom :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input type="text" className="grow" value={user.firstname} disabled />
        </label>
      </div>
      <div className="grid grid-cols-7 items-center lg:col-span-3">
        <span className="col-span-3">Date de naissance :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-4">
          <input
            type="date"
            className="grow"
            value={new Date(user.birth_at).toISOString().split("T")[0]}
            disabled
          />
        </label>
      </div>
      <div className="grid grid-cols-7 items-center lg:col-span-3">
        <span className="col-span-4">Date de création :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input
            type="date"
            className="grow"
            value={new Date(user.created_at).toISOString().split("T")[0]}
            disabled
          />
        </label>
      </div>
      <div className="grid grid-cols-7 items-center lg:col-span-3">
        <span className="col-span-4">Dernière connexion :</span>
        <label className="input input-bordered flex items-center gap-2 col-span-3">
          <input
            type="date"
            className="grow"
            value={new Date(user.login_at).toISOString().split("T")[0]}
            disabled
          />
        </label>
      </div>

      {/* Si le rôle est présent, l'afficher */}
      {user.role === "ROLE_ADMIN" && (
        <div className="grid grid-cols-4 items-center lg:col-span-3">
          <span className="">Rôle :</span>
          {/* <label className="input input-bordered flex items-center gap-2 col-span-3"> */}
            <span className="badge badge-primary">Admin</span>
          {/* </label> */}
        </div>
      )}

      <a
        className="btn text-white bg-[var(--color-1)] lg:col-start-3 lg:col-span-2 my-11 w-60 mx-auto"
        href="/profil/edit"
      >
        Modifier
      </a>
    </main>
  );
}

export default Profil;
