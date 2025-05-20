 'use client';

import { useEffect, useState } from 'react';
import { fetchUserProfile } from '@/utils/api';

export default function DashboardPage() {
  const [user, setUser] = useState<{ name: string } | null>(null);

  useEffect(() => {
    async function loadUser() {
      try {
        const data = await fetchUserProfile();
        setUser(data);
      } catch (error) {
        console.error('Erreur:', error);
      }
    }

    loadUser();
  }, []);

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      {user ? (
        <p>Bienvenue, <strong>{user.name}</strong> !</p>
      ) : (
        <p>Chargement du profil...</p>
      )}
    </div>
  );
}