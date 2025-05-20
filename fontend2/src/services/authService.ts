 import API_URL from '@/config';

export async function login(email: string, password: string) {
  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.token);
      return { success: true };
    } else {
      return { success: false, message: data.message || 'Erreur de connexion.' };
    }
  } catch (error) {
    return { success: false, message: 'Erreur réseau.' };
  }
}