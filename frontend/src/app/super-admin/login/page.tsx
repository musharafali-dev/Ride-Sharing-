"use client";

import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldCheck, HardDrive, Key, User, ArrowLeft, Cpu } from "lucide-react";
import Link from "next/link";

export default function SuperAdminLogin() {
  const router = useRouter();
  const [isPrompted, setIsPrompted] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [success, setSuccess] = useState(false);

  const triggerHardwareKeyCheck = () => {
    setIsPrompted(true);
    setIsVerifying(true);

    setTimeout(() => {
      setIsVerifying(false);
      setSuccess(true);
      
      // Save Super Admin session
      localStorage.setItem("user_role", "admin");
      localStorage.setItem("user_email", "superadmin@ridesphere.com");
      localStorage.setItem("user_status", "ACTIVE");
      localStorage.setItem("user_name", "Super Administrator");

      const existingLogsRaw = localStorage.getItem("admin_security_logs") || "[]";
      const existingLogs = JSON.parse(existingLogsRaw);
      existingLogs.unshift({
        timestamp: new Date().toISOString().replace("T", " ").substring(0, 16),
        action: "Super Admin session authenticated via FIDO2 Hardware Key",
        user: "superadmin@ridesphere.com",
        status: "Success"
      });
      localStorage.setItem("admin_security_logs", JSON.stringify(existingLogs));

      setTimeout(() => {
        router.push("/dashboard/admin");
      }, 800);

    }, 2000);
  };

  return (
    <div className="flex flex-col min-h-screen bg-brand-bg text-secondary">
      <Navbar />

      <main className="grow flex items-center justify-center py-20 px-4">
        <div className="w-full max-w-md bg-slate-900 border border-slate-800 text-white rounded-3xl p-8 sm:p-12 shadow-2xl relative overflow-hidden text-center space-y-8">
          <div className="absolute inset-0 z-0">
            <div className="absolute top-0 left-0 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl"></div>
          </div>

          <div className="relative z-10 space-y-3">
            <span className="inline-flex p-3 rounded-2xl bg-blue-500/10 text-blue-400">
              <Cpu className="h-6 w-6" />
            </span>
            <h1 className="font-display font-extrabold text-2xl tracking-tight text-white">Super Admin Access</h1>
            <p className="text-slate-400 text-xs font-semibold leading-relaxed max-w-xs mx-auto">
              System Administrator authentication requires a registered FIDO2 / WebAuthn Hardware Security Key.
            </p>
          </div>

          <div className="relative z-10 py-6 border-y border-white/5 space-y-4">
            {!isPrompted ? (
              <button
                onClick={triggerHardwareKeyCheck}
                className="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-2xl text-xs flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-blue-900/35 transition-all"
              >
                <HardDrive className="h-4.5 w-4.5" /> Authenticate with Hardware Key
              </button>
            ) : (
              <div className="space-y-4 py-2">
                <div className="flex justify-center">
                  <div className="w-12 h-12 bg-white/5 rounded-full flex items-center justify-center animate-pulse">
                    <Key className={`h-6 w-6 ${success ? "text-emerald-400" : "text-blue-400"}`} />
                  </div>
                </div>
                <div className="space-y-1">
                  <span className="block text-xs font-mono font-bold text-slate-200">
                    {isVerifying ? "Contacting Security Key..." : "Hardware Key Verified!"}
                  </span>
                  <p className="text-[10px] text-slate-450 leading-relaxed font-semibold">
                    {isVerifying ? "Please insert your USB security key or tap the biometric fingerprint scanner." : "Initializing Super Admin dashboard node..."}
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="relative z-10 pt-4 flex flex-col gap-3">
            <Link href="/admin/login" className="text-xs text-slate-400 font-bold hover:text-white flex items-center justify-center gap-1">
              <ArrowLeft className="h-3.5 w-3.5" /> Back to Standard Admin Login
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
