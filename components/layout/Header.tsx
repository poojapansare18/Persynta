"use client";

import { Bell } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export default function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-white/95 px-4 backdrop-blur md:px-6">
      <div>
        <p className="text-sm text-gray-500">Personal AI companion</p>
      </div>

      <div className="flex items-center gap-4">
        <button
          aria-label="Notifications"
          className="rounded-full p-2 text-gray-600 transition hover:bg-gray-100"
        >
          <Bell size={20} />
        </button>

        <Avatar>
          <AvatarFallback>PP</AvatarFallback>
        </Avatar>
      </div>
    </header>
  );
}