 import './globals.css';
import Navbar from '@/components/Navbar';

export const metadata = {
  title: 'Mon projet de Mairie',
  description: 'Application Next.js avec Authentification',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>
        <Navbar />
        <main className="p-4">{children}</main>
      </body>
    </html>
  );
}
