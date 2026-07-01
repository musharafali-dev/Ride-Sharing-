import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-display",
});

export const metadata: Metadata = {
  title: "RideSphere - Multi-Vehicle Rental & Tourism Booking Platform",
  description: "Book city rides, rent self-drive vehicles, bikes, luxury cars, tourist buses, and customize tour packages.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <body
        className={`${inter.variable} ${outfit.variable} antialiased bg-[#07090e] text-[#f1f5f9] min-h-screen flex flex-col font-sans`}
      >
        {children}
      </body>
    </html>
  );
}
