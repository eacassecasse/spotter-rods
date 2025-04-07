import { useState } from "react";
import "./App.css";
import { useAuth } from "@/context/AuthContext";
import { LoginForm } from "./components/login-form";

function App() {
  const { user } = useAuth();

  return (
    <>
      {user ? (
        <main className="h-screen w-screen grid grid-cols-3 gap-8 m-auto p-8">
          <div className="col-span-2 border border-green-700 rounded-md">1</div>
          <div className="col-span-1 border border-green-700 rounded-md">2</div>
          <div className="col-span-1 border border-green-700 rounded-md">3</div>
          <div className="col-span-1 border border-green-700 rounded-md">4</div>
          <div className="col-span-1 border border-green-700 rounded-md">5</div>
        </main>
      ) : (
        <main className="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
          <div className="w-full max-w-sm md:max-w-3xl">
            <LoginForm/>
          </div>
        </main>
      )}
    </>
  );
}

export default App;
