"use client";

import { useEffect, useState } from "react";

type Guest = {
  id: number;
  name: string;
  email: string;
};

type Meeting = {
  id: number;
  title: string;
  agenda: string | null;
  start_at: string;
  end_at: string;
  location: string | null;
  status: string;
  guests: Guest[];
};

type GuestForm = {
  name: string;
  email: string;
};

function getLocalParts(value: string) {
  const date = new Date(value);

  const pad = (n: number) =>
    String(n).padStart(2, "0");

  return {
    date:
      `${date.getFullYear()}-` +
      `${pad(date.getMonth() + 1)}-` +
      `${pad(date.getDate())}`,

    time:
      `${pad(date.getHours())}:` +
      `${pad(date.getMinutes())}`,
  };
}

function toISOString(
  date: string,
  time: string,
) {
  return new Date(
    `${date}T${time}`,
  ).toISOString();
}

export default function ChangeMeetingPage({
  params,
}: {
  params: Promise<{ token: string }>;
}) {
  const [token, setToken] = useState("");

  const [meeting, setMeeting] =
    useState<Meeting | null>(null);

  const [title, setTitle] = useState("");
  const [agenda, setAgenda] = useState("");
  const [location, setLocation] = useState("");

  const [date, setDate] = useState("");
  const [startTime, setStartTime] =
    useState("");
  const [endTime, setEndTime] =
    useState("");

  const [guests, setGuests] =
    useState<GuestForm[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState(false);

  useEffect(() => {
    params.then(({ token }) => {
      setToken(token);

      fetch(
        `http://localhost:8000/meetings/change/${token}`
      )
        .then(async (response) => {
          const body = await response.json();

          if (!response.ok) {
            throw new Error(
              body.detail ||
                "Unable to load meeting."
            );
          }

          return body;
        })
        .then((data: Meeting) => {
          const start =
            getLocalParts(
              data.start_at,
            );

          const end =
            getLocalParts(
              data.end_at,
            );

          setMeeting(data);

          setTitle(data.title);
          setAgenda(
            data.agenda || "",
          );
          setLocation(
            data.location || "",
          );

          setDate(start.date);
          setStartTime(start.time);
          setEndTime(end.time);

          setGuests(
            data.guests.map(
              (guest) => ({
                name: guest.name,
                email: guest.email,
              }),
            ),
          );

          setLoading(false);
        })
        .catch((err) => {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load meeting.",
          );

          setLoading(false);
        });
    });
  }, [params]);

  function addGuest() {
    setGuests([
      ...guests,
      {
        name: "",
        email: "",
      },
    ]);
  }

  function removeGuest(index: number) {
    setGuests(
      guests.filter(
        (_, i) => i !== index,
      ),
    );
  }

  function updateGuest(
    index: number,
    field: keyof GuestForm,
    value: string,
  ) {
    setGuests(
      guests.map(
        (guest, i) =>
          i === index
            ? {
                ...guest,
                [field]: value,
              }
            : guest,
      ),
    );
  }

  async function submitChanges(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setSaving(true);

    try {
      const response =
        await fetch(
          `http://localhost:8000/meetings/change/${token}`,
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json",
            },
            body: JSON.stringify({
              title,
              agenda:
                agenda || null,
              location:
                location || null,

              start_at:
                toISOString(
                  date,
                  startTime,
                ),

              end_at:
                toISOString(
                  date,
                  endTime,
                ),

              guests,
            }),
          },
        );

      const body =
        await response.json();

      if (!response.ok) {
        if (
          typeof body.detail ===
          "object"
        ) {
          throw new Error(
            body.detail.message ||
              "Unable to change meeting.",
          );
        }

        throw new Error(
          body.detail ||
            "Unable to change meeting.",
        );
      }

      setMeeting(body);
      setSuccess(true);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong.",
      );
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#FAFAFA] flex items-center justify-center">
        <p className="text-sm text-gray-500">
          Loading meeting...
        </p>
      </main>
    );
  }

  if (!meeting) {
    return (
      <main className="min-h-screen bg-[#FAFAFA] flex items-center justify-center p-6">
        <div className="w-full max-w-md rounded-2xl border bg-white p-8 text-center">
          <h1 className="text-xl font-semibold text-gray-900">
            Unable to change meeting
          </h1>

          <p className="mt-3 text-sm text-gray-500">
            {error}
          </p>
        </div>
      </main>
    );
  }

  if (success) {
    return (
      <main className="min-h-screen bg-[#FAFAFA] flex items-center justify-center p-6">
        <div className="w-full max-w-lg rounded-2xl border bg-white p-8">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-50 text-green-600">
            ✓
          </div>

          <h1 className="mt-6 text-2xl font-semibold text-gray-900">
            Meeting updated
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Your meeting details have
            been updated successfully.
          </p>

          <div className="mt-6 rounded-xl border bg-gray-50 p-4">
            <p className="font-medium text-gray-900">
              {meeting.title}
            </p>

            <p className="mt-1 text-sm text-gray-500">
              {new Date(
                meeting.start_at,
              ).toLocaleString()}
            </p>

            <p className="text-sm text-gray-500">
              Status: {meeting.status}
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#FAFAFA] px-4 py-10">
      <div className="mx-auto max-w-2xl">

        <div className="mb-8">
          <p className="text-sm font-medium text-gray-500">
            Persynta
          </p>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-gray-900">
            Change meeting
          </h1>

          <p className="mt-2 text-sm text-gray-500">
            Update the meeting details
            below.
          </p>
        </div>

        <form
          onSubmit={submitChanges}
          className="space-y-6 rounded-2xl border bg-white p-6 shadow-sm"
        >

          {/* Title */}

          <div>
            <label className="text-sm font-medium text-gray-700">
              Title
            </label>

            <input
              value={title}
              onChange={(e) =>
                setTitle(e.target.value)
              }
              required
              className="mt-2 w-full rounded-xl border px-3 py-2.5"
            />
          </div>

          {/* Agenda */}

          <div>
            <label className="text-sm font-medium text-gray-700">
              Agenda
            </label>

            <textarea
              value={agenda}
              onChange={(e) =>
                setAgenda(e.target.value)
              }
              rows={4}
              className="mt-2 w-full rounded-xl border px-3 py-2.5"
            />
          </div>

          {/* Date / time */}

          <div className="grid gap-4 sm:grid-cols-3">

            <div>
              <label className="text-sm font-medium text-gray-700">
                Date
              </label>

              <input
                type="date"
                value={date}
                onChange={(e) =>
                  setDate(e.target.value)
                }
                required
                className="mt-2 w-full rounded-xl border px-3 py-2.5"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700">
                Start
              </label>

              <input
                type="time"
                value={startTime}
                onChange={(e) =>
                  setStartTime(
                    e.target.value,
                  )
                }
                required
                className="mt-2 w-full rounded-xl border px-3 py-2.5"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700">
                End
              </label>

              <input
                type="time"
                value={endTime}
                onChange={(e) =>
                  setEndTime(
                    e.target.value,
                  )
                }
                required
                className="mt-2 w-full rounded-xl border px-3 py-2.5"
              />
            </div>

          </div>

          {/* Location */}

          <div>
            <label className="text-sm font-medium text-gray-700">
              Location
            </label>

            <input
              value={location}
              onChange={(e) =>
                setLocation(
                  e.target.value,
                )
              }
              placeholder="Optional"
              className="mt-2 w-full rounded-xl border px-3 py-2.5"
            />
          </div>

          {/* Guests */}

          <div>
            <div className="flex items-center justify-between">

              <label className="text-sm font-medium text-gray-700">
                Guests
              </label>

              <button
                type="button"
                onClick={addGuest}
                className="text-sm font-medium text-gray-700"
              >
                + Add guest
              </button>

            </div>

            <div className="mt-3 space-y-3">

              {guests.map(
                (guest, index) => (
                  <div
                    key={index}
                    className="grid gap-3 sm:grid-cols-[1fr_1fr_auto]"
                  >

                    <input
                      value={guest.name}
                      onChange={(e) =>
                        updateGuest(
                          index,
                          "name",
                          e.target.value,
                        )
                      }
                      placeholder="Guest name"
                      className="rounded-xl border px-3 py-2.5"
                    />

                    <input
                      type="email"
                      value={guest.email}
                      onChange={(e) =>
                        updateGuest(
                          index,
                          "email",
                          e.target.value,
                        )
                      }
                      placeholder="Guest email"
                      className="rounded-xl border px-3 py-2.5"
                    />

                    <button
                      type="button"
                      onClick={() =>
                        removeGuest(index)
                      }
                      className="rounded-xl border px-3 py-2 text-sm text-gray-500 hover:text-red-600"
                    >
                      Remove
                    </button>

                  </div>
                ),
              )}

            </div>
          </div>

          {/* Error */}

          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Submit */}

          <button
            type="submit"
            disabled={saving}
            className="w-full rounded-xl bg-gray-900 px-4 py-3 text-sm font-medium text-white disabled:opacity-50"
          >
            {saving
              ? "Saving changes..."
              : "Confirm Changes"}
          </button>

        </form>
      </div>
    </main>
  );
}