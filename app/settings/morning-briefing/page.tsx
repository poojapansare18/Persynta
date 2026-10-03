import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import MobileNav from "@/components/layout/MobileNav";
import MorningBriefing from "@/components/settings/MorningBriefing";

export default function MorningBriefingPage() {
  return (
    <div className="min-h-screen bg-[#fafafa]">
      <Sidebar />

      <div className="md:pl-60">
        <Header />

        <main className="p-4 pb-24 md:p-6 md:pb-6">
          <MorningBriefing />
        </main>
      </div>

      <MobileNav />
    </div>
  );
}