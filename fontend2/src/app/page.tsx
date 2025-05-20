export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold mb-4">Bienvenue sur l'application de la Mairie</h1>
      <p className="text-lg mb-8">Connectez-vous pour accéder à votre compte.</p>
      <a href="/login" className="bg-blue-500 text-white px-4 py-2 rounded">
        Se connecter
      </a>
    </div>
  );
}
