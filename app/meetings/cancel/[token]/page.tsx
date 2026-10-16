"use client";

import { apiUrl } from "@/lib/api/client";

import { useEffect, useState } from "react";

type Meeting = {
  id: number;
  title: string;
  agenda: string | null;
  start_at: string;
  end_at: string;
  location: string | null;
  meeting_url: string | null;
  status: string;
};

type PageState =
  | "loading"
  | "preview"
  | "cancelling"
  | "success"
  | "error";

export default function CancelMeetingPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const [token, setToken] = useState<string | null>(null);
  const [meeting, setMeeting] = useState<Meeting | null>(null);
  const [state, setState] = useState<PageState>("loading");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    params.then(({ token }) => {
      setToken(token);
    });
  }, [params]);

  useEffect(() => {
    if (!token) return;

    const loadMeeting = async () => {
      try {
        const response = await fetch(
          apiUrl(`/meetings/cancel/${token}`)
        );

        if (!response.ok) {
          const data = await response.json();
          throw new Error(
            data.detail || "Unable to load meeting."
          );
        }

        const data = await response.json();

        setMeeting(data);
        setState("preview");
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load meeting."
        );
        setState("error");
      }
    };

    loadMeeting();
  }, [token]);

  const handleCancel = async () => {
    if (!token) return;

    setState("cancelling");
    setError("");

    try {
      const response = await fetch(
        apiUrl(`/meetings/cancel/${token}`),
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const data = await response.json();

        throw new Error(
          data.detail || "Unable to cancel meeting."
        );
      }

      const data = await response.json();

      setMeeting(data);
      setState("success");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to cancel meeting."
      );

      setState("error");
    }
  };

  if (state === "loading") {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p className="text-sm text-gray-500">
          Loading meeting...
        </p>
      </main>
    );
  }

  if (state === "error") {
    return (
      <main className="min-h-screen flex items-center justify-center px-6">
        <div className="w-full max-w-md rounded-2xl border bg-white p-8 text-center shadow-sm">
          <h1 className="text-xl font-semibold">
            Unable to cancel meeting
          </h1>

          <p className="mt-3 text-sm text-gray-500">
            {error}
          </p>
        </div>
      </main>
    );
  }

  if (!meeting) {
    return null;
  }

  if (state === "success") {
    return (
      <main className="min-h-screen flex items-center justify-center px-6">
        <div className="w-full max-w-md rounded-2xl border bg-white p-8 text-center shadow-sm">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-gray-100">
            ✓
          </div>

          <h1 className="mt-5 text-2xl font-semibold">
            Meeting cancelled
          </h1>

          <p className="mt-3 text-sm text-gray-500">
            The meeting has been cancelled successfully.
          </p>

          <div className="mt-6 rounded-xl bg-gray-50 p-4 text-left">
            <p className="font-medium">
              {meeting.title}
            </p>

            <p className="mt-1 text-sm text-gray-500">
              {new Date(meeting.start_at).toLocaleString()}
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-6">
      <div className="w-full max-w-md rounded-2xl border bg-white p-8 shadow-sm">
        <div className="text-center">
          <p className="text-sm font-medium text-gray-500">
            Persynta
          </p>

          <h1 className="mt-3 text-2xl font-semibold">
            Cancel this meeting?
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Review the meeting details before cancelling.
          </p>
        </div>

        <div className="mt-8 space-y-4 rounded-xl bg-gray-50 p-5">
          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
              Meeting
            </p>

            <p className="mt-1 font-medium">
              {meeting.title}
            </p>
          </div>

          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
              Date & time
            </p>

            <p className="mt-1 text-sm text-gray-700">
              {new Date(meeting.start_at).toLocaleString()}
              {" – "}
              {new Date(meeting.end_at).toLocaleTimeString()}
            </p>
          </div>

          {meeting.agenda && (
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
                Agenda
              </p>

              <p className="mt-1 text-sm text-gray-700">
                {meeting.agenda}
              </p>
            </div>
          )}
        </div>

        <button
          onClick={handleCancel}
          disabled={state === "cancelling"}
          className="mt-6 w-full rounded-xl bg-gray-900 px-4 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {state === "cancelling"
            ? "Cancelling..."
            : "Cancel Meeting"}
        </button>

        <p className="mt-4 text-center text-xs text-gray-400">
          This action cannot be undone.
        </p>
      </div>
    </main>
  );
}