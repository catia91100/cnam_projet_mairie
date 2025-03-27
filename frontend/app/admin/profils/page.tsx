"use client";
import { useEffect, useState, useRef } from "react";
import { redirect } from "next/navigation";
import GetCookie from "@/app/_fct/GetCookie";

import { faX, faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import API_URL from "@/app/config";

import Link from "next/link";

function page() {
  const [user, setUser] = useState(null);
  const [profils, setProfils] = useState([]);
  const modalRef = useRef(null);
  const [selectedProfil, setSelectedProfil] = useState(null);
  const [token, setToken] = useState(null);
  const[data, setData] = useState();

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
        const response = await fetch(`${API_URL}/account/all`, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setProfils(data.users);
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
    };

    if (token) {
      fetchData();
    }
  }, [token]);

  if (profils === null) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }

  function openModal(data) {
    setSelectedProfil(data);
    modalRef.current.showModal();
  }

  return (
    <main className="flex justify-center items-center flex-col">
      <h1 className="text-2xl my-2">Profils</h1>
      <div className="overflow-x-auto xl:w-2/3 max-h-[60vh]">
        <table className="table table-zebra text-center">
          {/* head */}
          <thead className="sticky top-0">
            <tr className="bg-black text-white">
              <th>Email</th>
              <th className="hidden md:table-cell">Nom</th>
              <th className="hidden md:table-cell">Prenom</th>
              <th className="hidden lg:table-cell">Date de naissance</th>
              <th className="hidden lg:table-cell">Dernière connexion</th>
              <th className="hidden lg:table-cell">Date de création</th>
              <th className="hidden md:table-cell">Role</th>
            </tr>
          </thead>
          <tbody className="">
            {profils.map((item, key) => (
              <tr key={key} onClick={() => openModal(item)}>
                <td>{item.email}</td>
                <td className="hidden md:table-cell">{item.firstname}</td>
                <td className="hidden md:table-cell">{item.lastname}</td>
                <td className="hidden lg:table-cell">
                  {new Date(item.birth_at).toLocaleDateString()}
                </td>
                <td className="hidden lg:table-cell">
                  {new Date(item.login_at).toLocaleDateString()}
                </td>
                <td className="hidden lg:table-cell">
                  {new Date(item.created_at).toLocaleDateString()}
                </td>
                <td className="hidden md:table-cell">{item.role || "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Modal */}
        <dialog id="my_modal_4" className="modal fixe" ref={modalRef}>
          <div className="modal-box max-h-screen">
            <div className="modal-action mt-0">
              {selectedProfil !== null ? (
                <div className="grid gap-2 md:grid-cols-2">
                  <div className="">
                    <span>Email :</span>
                    <label className="input input-bordered flex items-center gap-2">
                      <input
                        type="text"
                        className="grow"
                        value={selectedProfil.email}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span>Nom :</span>
                    <label className="input input-bordered flex items-center gap-2">
                      <input
                        type="text"
                        className="grow"
                        value={selectedProfil.firstname}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span>Prénom :</span>
                    <label className="input input-bordered flex items-center gap-2">
                      <input
                        type="text"
                        className="grow"
                        value={selectedProfil.lastname}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span>Date de naissance :</span>
                    <label className="input input-bordered flex items-center gap-2">
                      <input
                        type="date"
                        className="grow"
                        value={new Date(
                          selectedProfil.birth_at
                        ).toLocaleDateString("en-CA")}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span>Date de création :</span>
                    <label className="input input-bordered flex items-center gap-2">
                      <input
                        type="date"
                        className="grow"
                        value={new Date(
                          selectedProfil.created_at
                        ).toLocaleDateString("en-CA")}
                        disabled
                      />
                    </label>
                  </div>
                  <div className="">
                    <span>Dernière connexion :</span>
                    <label className="input input-bordered flex items-center gap-2">
                      <input
                        type="date"
                        className="grow"
                        value={new Date(
                          selectedProfil.login_at
                        ).toLocaleDateString("en-CA")}
                        disabled
                      />
                    </label>
                  </div>
                  <Link
                    className="btn text-white bg-[var(--color-1)] md:col-span-2"
                    href={{
                      pathname: "/admin/profils/edit",
                      query: {
                        firstName: selectedProfil.firstname,
                        lastName: selectedProfil.lastname,
                        email: selectedProfil.email,
                        birthAt: selectedProfil.birth_at,
                        loginAt: selectedProfil.login_at,
                        createdAt: selectedProfil.created_at,
                        role: selectedProfil.role,
                      },
                    }}
                  >
                    Modifier
                  </Link>
                  <button
                    onClick={() => {
                      if (confirm("Confirmez la suppression ?")) {
                        window.location.href = "/admin/profils";
                      }
                    }}
                    className="btn btn-warning max-w-16 ms-auto"
                  >
                    <FontAwesomeIcon icon={faTrash} />
                  </button>
                </div>
              ) : (
                <>pas de data</>
              )}
              <button
                className="absolute right-4 top-2"
                onClick={() => {
                  modalRef.current.close();
                }}
              >
                <FontAwesomeIcon icon={faX} className="fa-xs" />
              </button>
            </div>
          </div>
        </dialog>
      </div>
    </main>
  );
}

export default page;
