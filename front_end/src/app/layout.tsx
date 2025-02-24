"use client";

import React from "react";
import { WalletProvider, useWallet, ConnectButton } from "@razorlabs/razorkit";
import "@razorlabs/razorkit/style.css";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarProvider,
} from "@/components/ui/sidebar";
import Link from "next/link";
import { usePathname } from "next/navigation";
import "@mosaicag/swap-widget/style.css";
import "./globals.css";
import LandingPage from "@/components/LandingPage";
import Image from "next/image";
import { Suspense } from "react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <WalletProvider autoConnect={true}>
          <LayoutContent>{children}</LayoutContent>
        </WalletProvider>
      </body>
    </html>
  );
}

function LayoutContent({ children }: { children: React.ReactNode }) {
  const wallet = useWallet();
  const pathname = usePathname();

  if (pathname.startsWith("/address")) {
    return <Suspense>{children}</Suspense>;
  }

  // Show landing page if wallet is NOT connected
  if (!wallet.connected) {
    return <LandingPage />;
  }

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <div className="absolute top-4 right-4 z-50">
          <ConnectButton />
        </div>

        <Sidebar>
          <SidebarHeader>
            <h2 className="text-2xl font-semibold p-4 pb-0">Gfin 🤝🏼</h2>
            <Image
              src="/movement.png"
              width={150}
              height={150}
              alt="Movement Labs"
              className="inline ml-4"
            />
          </SidebarHeader>
          <SidebarContent>
            <nav className="space-y-2 p-4">
              <Link
                href="/"
                className={`block p-2 rounded ${
                  pathname === "/" ? "bg-gray-200" : ""
                }`}
              >
                Portfolio
              </Link>
              <Link
                href="/chat"
                className={`block p-2 rounded ${
                  pathname === "/chat" ? "bg-gray-200" : ""
                }`}
              >
                Goals & Tasks
              </Link>
            </nav>
          </SidebarContent>
        </Sidebar>
        <main className="flex-1 w-full">{children}</main>
      </div>
    </SidebarProvider>
  );
}
