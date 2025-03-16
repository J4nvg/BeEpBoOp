import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";
import Image from "next/image";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Megekko PC Builder",
  description: "Build your custom PC",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="px-10 bg-neutral-400 w-full h-[100px] flex flex-row items-center">
        <Image
        src="/megekkoLogo2021.svg"
        width={500}
        height={500}
        alt="Picture of the author"
        className="max-h-50"
        />
        <h1 className="text-1xl font-mono text-white mb-8 text-center">PC Builder</h1>
        </div>
        {children}
        <Toaster />
      </body>
    </html>
  );
}
