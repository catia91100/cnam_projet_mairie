"use client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

function ClearURL() {
  const router = useRouter();

  useEffect(() => {
    // Nettoie l'URL après un court délai pour que le message flash soit affiché
    setTimeout(() => {
      router.replace(window.location.pathname);
    }, 3000);
  }, [router]);

  return null; // Ce composant ne rend rien, il sert juste à nettoyer l'URL
}

export default ClearURL;
