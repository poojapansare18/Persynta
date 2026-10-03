import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import MobileNav from "@/components/layout/MobileNav";
import DigitalFriend from "@/components/settings/DigitalFriend";

export default function DigitalFriendPage() {
  return (
    <div className="min-h-screen bg-[#fafafa]">
      <Sidebar />

      <div className="md:pl-60">
        <Header />

        <main className="p-4 pb-24 md:p-6 md:pb-6">
          <DigitalFriend />
        </main>
      </div>

      <MobileNav />
    </div>
  );
}