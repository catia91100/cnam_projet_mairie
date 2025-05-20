 'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/utils/auth';

export default function DashboardPage() {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Tableau de bord</h1>
      <p>Bienvenue dans votre espace personnel.</p>
    </div>
  );
}