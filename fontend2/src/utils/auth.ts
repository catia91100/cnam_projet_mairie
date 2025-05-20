 export function isAuthenticated(): boolean {
  return typeof window !== 'undefined' && !!localStorage.getItem('token');
}

export function logout() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
}