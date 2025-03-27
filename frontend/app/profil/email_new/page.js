"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import API_URL from "@/app/config";
import { Suspense } from "react";

function EmailNew() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [data, setData] = useState({});
  const router = useRouter();

  useEffect(() => {
    if (token) {
      fetch(`${API_URL}/account/update-email?token=${token}`, {
        // Pass the token as a GET parameter
        method: "GET", // Use GET instead of POST
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          setData(data);
          // Delete the user cookie
          document.cookie =
            "user=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  }, [token]);

  useEffect(() => {
    if (Object.keys(data).length > 0) {
      const timer = setTimeout(() => {
        router.push("/login"); // Redirect using useRouter and push
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [data, router]);

  if (!data || Object.keys(data).length === 0) {
    return;
  }

  return (
    <main className="mt-[1rem] flex justify-center items-center flex-col">
      <h1 className="text-2xl my-5">
        Modification prise en compte, vous pouvez vous connecter avec votre
        nouvel identifiant.
      </h1>
    </main>
  );
}

import React from "react";

function Page() {
  return (
    <Suspense
      fallback={
        <main className="flex justify-center items-center">
          <span className="loading loading-dots loading-lg"></span>
        </main>
      }
    >
      <EmailNew />
    </Suspense>
  );
}

export default Page;
