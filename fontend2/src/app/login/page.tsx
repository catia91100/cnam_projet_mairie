 'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { login } from '@/services/authService';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await login(email, password);
    if (result.success) {
      router.push('/dashboard');
    } else {
      setError(result.message);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-80 space-y-4">
        <h2 className="text-xl font-bold">Connexion</h2>
        {error && <p className="text-red-500">{error}</p>}
        <input
          type="email"
          placeholder="Email"
          className="input input-bordered w-full"
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Mot de passe"
          className="input input-bordered w-full"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button className="btn bg-blue-600 text-white w-full" type="submit">
          Se connecter
        </button>
      </form>
    </div>
  );
}