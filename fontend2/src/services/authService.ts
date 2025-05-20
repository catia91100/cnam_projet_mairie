import API_URL from "@/config";

 export async function login(email: string, password: string) {
  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include' // Important pour les cookies
    });
    
    const data = await res.json();
    
    if (res.ok) {
      // Stockage multiple pour compatibilité
      localStorage.setItem('token', data.access_token);
      document.cookie = `token=${data.access_token}; path=/; Secure; SameSite=Lax`;
      return { success: true };
    }
    return { success: false, message: data.msg || 'Échec de connexion' };
  } catch (error) {
    return { success: false, message: 'Erreur réseau' };
  }
}