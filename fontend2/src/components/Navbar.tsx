 'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { isAuthenticated, logout } from '@/utils/auth';
import { useEffect, useState } from 'react';

export default function Navbar() {
  const router = useRouter();
  const [auth, setAuth] = useState<boolean | null>(null);
   useEffect(() => {
   setAuth(isAuthenticated());
  }, []);
  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between">
      <Link href="/" className="font-bold">MonApp</Link>
      <div className="space-x-4">
        {auth ? (
          <>
            <Link href="/dashboard">Dashboard</Link>
            <button onClick={handleLogout} className="underline">Déconnexion</button>
          </>
        ) : (
          <Link href="/login">Connexion</Link>
        )}
      </div>
    </nav>
  );
}