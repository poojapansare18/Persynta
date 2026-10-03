import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header";
import MobileNav from "@/components/layout/MobileNav";
import Notes from "@/components/notes/Notes";

export default function NotesPage() {
  return (
    <div className="min-h-screen bg-muted/30">
      <div className="flex">
        <Sidebar />

        <div className="flex min-h-screen flex-1 flex-col">
          <Header />

          <main className="flex-1 px-4 py-6 pb-24 md:px-8 md:py-8 md:pb-8">
            <div className="mx-auto max-w-7xl">
              <Notes />
            </div>
          </main>
        </div>
      </div>

      <MobileNav />
    </div>
  );
}