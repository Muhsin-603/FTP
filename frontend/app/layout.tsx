import type { Metadata } from "next";
import { Geist, Geist_Mono, Courier_Prime } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const courier = Courier_Prime({
  weight: "400",
  variable: "--font-courier",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SECURE ACCESS // GATEWAY",
  description: "frontend by LordSA",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${courier.variable} ${courier.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
