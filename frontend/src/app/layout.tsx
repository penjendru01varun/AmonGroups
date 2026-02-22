import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MAITRI - AI Assistant for Astronaut Well-Being",
  description: "Multi-Agent AI System for Psychological & Physical Well-Being of Astronauts",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link 
          href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap" 
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
