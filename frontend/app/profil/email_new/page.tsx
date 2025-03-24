"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

function Page() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [data, setData] = useState({});

  useEffect(() => {
    if (token) {
      fetch("http://localhost:5000/email_new", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
      })
        .then((response) => setData(response.json()))
        .then((data) => {
          document.cookie =
            "user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  }, [token]);
  if (!data) {
    return (
      <main className="flex justify-center items-center">
        <span className="loading loading-dots loading-lg"></span>
      </main>
    );
  }
  return (
    <main className="mt-[1rem] flex justify-center items-center flex-col">
    <h1 className="text-2xl my-5">
      Modification prise en compte, vous pouvez vous connecter avec votre
      nouvel identifiant.
    </h1>
    {useEffect(() => {
      const timer = setTimeout(() => {
        window.location.href = "/";
      }, 3000);
      return () => clearTimeout(timer);
    }, [])}
    </main>
  );
}

export default Page;
