"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/auth-store";
import Sidebar from "@/components/layout/Sidebar";
import Footer from "@/components/layout/Footer";
import AhaduLogo from "@/components/AhaduLogo";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, checkAuth } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return null;
  }

  if (!isAuthenticated) return null;

  return (
    <div className="flex min-h-screen bg-[#F5F5F5]">
      <Sidebar />
      <div className="ml-64 flex-1 flex flex-col min-h-screen">
        <div className="flex-1">
          {children}
        </div>
        <Footer />
      </div>
    </div>
  );
}
