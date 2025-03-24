"use client";
import GetCookie from "@/app/_fct/GetCookie";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";

function Page() {
  const [data, setData] = useState(null);
  const [token, setToken] = useState(null);
  const [handleUser, setHandleUser] = useState({});
  const [passwordIsReset, setPasswordIsReset] = useState(false);

  useEffect(() => {
    if (GetCookie({ name: "user" })) {
      const cookieStr = GetCookie({ name: "user" });
      if (cookieStr) {
        const cookie = JSON.parse(decodeURIComponent(cookieStr));
        // const cookie = JSON.parse(decodeURIComponent(cookieStr));
        setToken(cookie.token);
      } else {
        return redirect("/");
      }
      // setToken(cookie.token);
    } else {
      return redirect("/");
    }
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/profil", {
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

  // if (!user) {
  if (data === null) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }
  const user = data.user;

  function handleChange(e) {
    const { id, value } = e.target;
    setHandleUser((prevState) => ({
      ...prevState,
      [id]: value,
    }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    // const today = new Date(Date.now());
    // today.setHours(today.getHours() + 1);
    let userNew = {};

    if (handleUser.email !== undefined && handleUser.email !== user.email) {
      userNew.newEmail = handleUser.email;
      userNew.email = user.email;
    }

    Object.keys(user).forEach((key) => {
      if (handleUser[key] !== undefined && handleUser[key] !== user[key]) {
        userNew[key] = handleUser[key];
      }
    });

    // console.log(userNew);

    fetch("http://localhost:5000/profil", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(userNew),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      })
      .catch((error) => {
        console.error("Error updating profile:", error);
      });
    return redirect("/profil");
  }
  function passwordReset() {
    if (confirm("Confirmer la demande de réinitialisation ?")) {
      fetch(`http://localhost:5000/reset_request/${user.email}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
        })
        .catch((error) => {
          console.error("Error sending password reset request:", error);
        });
      setPasswordIsReset(true);
    }
  }

  return (
    <main className="">
      {passwordIsReset && (
        <div role="alert" className="alert alert-info">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            className="h-6 w-6 shrink-0 stroke-current"
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
      <form
        className="grid gap-3 lg:grid-cols-6 lg:mx-40 lg:my-20"
        onSubmit={(e) => handleSubmit(e)}
      >
        <div className="grid grid-cols-4 items-center lg:col-span-3">
          <span className="">Email :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-3">
            <input
              type="email"
              className="grow"
              defaultValue={user.email}
              onChange={(e) => handleChange(e)}
              id="email"
              required
            />
          </label>
        </div>
        <button
          className="btn btn-warning lg:col-span-3 mx-auto"
          onClick={passwordReset}
          disabled={passwordIsReset}
        >
          Réinitialiser le mot de passe
        </button>
        <div className="grid grid-cols-4 items-center lg:col-span-3">
          <span className="">Nom :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-3">
            <input
              type="text"
              className="grow"
              defaultValue={user.firstname}
              onChange={(e) => handleChange(e)}
              id="firstname"
            />
          </label>
        </div>
        <div className="grid grid-cols-4 items-center lg:col-span-3">
          <span className="">Prénom :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-3">
            <input
              type="text"
              className="grow"
              defaultValue={user.lastname}
              onChange={(e) => handleChange(e)}
              id="lastname"
              required
            />
          </label>
        </div>
        <div className="grid grid-cols-7 items-center lg:col-span-3">
          <span className="col-span-3">Date de naissance :</span>
          <label className="input input-bordered flex items-center gap-2 col-span-4">
            <input
              type="date"
              className="grow"
              defaultValue={new Date(user.birth_at).toISOString().split("T")[0]}
              onChange={(e) => handleChange(e)}
              id="birth_at"
              required
            />
          </label>
        </div>
        <button
          className="btn text-white bg-[var(--color-1)] lg:col-start-3 lg:col-span-2 my-11 w-60 mx-auto"
          type="submit"
        >
          Sauvegarder
        </button>
      </form>
    </main>
  );
}
// }

export default Page;
