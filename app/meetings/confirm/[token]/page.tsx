"use client";

import { apiUrl } from "@/lib/api/client";

import { useEffect, useState } from "react";

type Meeting = {
  id: number;
  title: string;
  agenda: string | null;
  start_at: string;
  end_at: string;
  meeting_url: string | null;
  status: string;
};

type PageState =
  | "loading"
  | "preview"
  | "confirming"
  | "success"
  | "error";

export default function MeetingConfirmationPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const [state, setState] = useState<PageState>("loading");
  const [meeting, setMeeting] = useState<Meeting | null>(null);
  const [error, setError] = useState("");
  const [token, setToken] = useState("");

  useEffect(() => {
    const loadMeeting = async () => {
      try {
        const { token } = await params;

        setToken(token);

        const response = await fetch(
          apiUrl(`/meetings/confirm/${token}`),
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            typeof data.detail === "string"
              ? data.detail
              : "Unable to load this meeting.",
          );
        }

        setMeeting(data);
        setState("preview");
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Something went wrong.",
        );

        setState("error");
      }
    };

    loadMeeting();
  }, [params]);

  const confirmMeeting = async () => {
    setState("confirming");
    setError("");

    try {
      const response = await fetch(
        apiUrl(`/meetings/confirm/${token}`),
        {
          method: "POST",
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : data.detail?.message
              ? data.detail.message
              : "Unable to schedule this meeting.",
        );
      }

      setMeeting(data);
      setState("success");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong.",
      );

      setState("error");
    }
  };

  if (state === "loading") {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#FAFAFA] px-6">
        <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
          <div className="mx-auto mb-5 h-8 w-8 animate-spin rounded-full border-2 border-gray-300 border-t-gray-900" />

          <h1 className="text-xl font-semibold text-gray-900">
            Loading meeting
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Please wait while Persynta loads the meeting details.
          </p>
        </div>
      </main>
    );
  }

  if (state === "error") {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#FAFAFA] px-6">
        <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
          <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-full bg-red-50 text-red-600">
            !
          </div>

          <h1 className="text-xl font-semibold text-gray-900">
            Meeting could not be confirmed
          </h1>

          <p className="mt-3 text-sm leading-6 text-gray-500">
            {error}
          </p>

          <p className="mt-6 text-xs text-gray-400">
            The confirmation link may have expired, or the selected
            time may no longer be available.
          </p>
        </div>
      </main>
    );
  }

  if (state === "preview" && meeting) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#FAFAFA] px-6">
        <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
          <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 text-blue-700">
            ?
          </div>

          <h1 className="text-2xl font-semibold tracking-tight text-gray-900">
            Confirm your meeting
          </h1>

          <p className="mt-2 text-sm leading-6 text-gray-500">
            Review the details below before Persynta adds the
            meeting to your Google Calendar.
          </p>

          <div className="mt-7 rounded-xl bg-gray-50 p-5">
            <h2 className="font-medium text-gray-900">
              {meeting.title}
            </h2>

            {meeting.agenda && (
              <div className="mt-4">
                <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
                  Agenda
                </p>

                <p className="mt-1 text-sm leading-6 text-gray-600">
                  {meeting.agenda}
                </p>
              </div>
            )}

            <div className="mt-5 space-y-3 text-sm text-gray-600">
              <p>
                <span className="font-medium text-gray-900">
                  Start:
                </span>{" "}
                {new Date(meeting.start_at).toLocaleString()}
              </p>

              <p>
                <span className="font-medium text-gray-900">
                  End:
                </span>{" "}
                {new Date(meeting.end_at).toLocaleString()}
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={confirmMeeting}
            className="mt-6 w-full rounded-lg bg-gray-900 px-4 py-3 text-sm font-medium text-white transition hover:bg-gray-800"
          >
            Confirm & Schedule
          </button>

          <p className="mt-4 text-center text-xs leading-5 text-gray-400">
            Persynta will check your calendar again before
            scheduling the meeting.
          </p>
        </div>
      </main>
    );
  }

  if (state === "confirming") {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#FAFAFA] px-6">
        <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
          <div className="mx-auto mb-5 h-8 w-8 animate-spin rounded-full border-2 border-gray-300 border-t-gray-900" />

          <h1 className="text-xl font-semibold text-gray-900">
            Scheduling your meeting
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Persynta is checking your calendar and creating
            the meeting.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#FAFAFA] px-6">
      <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
        <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-full bg-green-50 text-green-700">
          ✓
        </div>

        <h1 className="text-2xl font-semibold tracking-tight text-gray-900">
          Meeting scheduled
        </h1>

        <p className="mt-2 text-sm text-gray-500">
          Persynta successfully added the meeting to your
          Google Calendar.
        </p>

        {meeting && (
          <div className="mt-7 rounded-xl bg-gray-50 p-5">
            <h2 className="font-medium text-gray-900">
              {meeting.title}
            </h2>

            {meeting.agenda && (
              <p className="mt-2 text-sm text-gray-500">
                {meeting.agenda}
              </p>
            )}

            <div className="mt-4 space-y-2 text-sm text-gray-600">
              <p>
                <span className="font-medium text-gray-900">
                  Start:
                </span>{" "}
                {new Date(meeting.start_at).toLocaleString()}
              </p>

              <p>
                <span className="font-medium text-gray-900">
                  End:
                </span>{" "}
                {new Date(meeting.end_at).toLocaleString()}
              </p>
            </div>
          </div>
        )}

        {meeting?.meeting_url && (
          <a
            href={meeting.meeting_url}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-6 block rounded-lg bg-gray-900 px-4 py-3 text-center text-sm font-medium text-white transition hover:bg-gray-800"
          >
            Open Google Meet
          </a>
        )}
      </div>
    </main>
  );
}