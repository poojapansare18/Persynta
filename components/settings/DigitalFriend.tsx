"use client";

import { useState } from "react";
import {
  Phone,
  Copy,
  Check,
  Globe,
  RefreshCw,
  Clock,
} from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function DigitalFriend() {
  const [copied, setCopied] = useState(false);

  const [settings, setSettings] = useState({
    language: "English",
    retryCalls: true,
    maxRetries: "3",
    retryInterval: "5",
  });

  const phoneNumber = "+91 XXXXX XXXXX";

  const copyNumber = async () => {
    try {
      await navigator.clipboard.writeText(phoneNumber);
      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);
    } catch {
      setCopied(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Digital Friend
        </h1>

        <p className="mt-1 text-sm text-muted-foreground">
          Configure how your Digital Friend calls and interacts with you.
        </p>
      </div>

      {/* Number */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Your Digital Friend number
          </CardTitle>
        </CardHeader>

        <CardContent>
          <div className="rounded-xl border bg-muted/20 p-5">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-full bg-black text-white">
                  <Phone className="h-5 w-5" />
                </div>

                <div>
                  <p className="text-lg font-semibold">
                    {phoneNumber}
                  </p>

                  <div className="mt-1 flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-green-500" />

                    <span className="text-xs text-muted-foreground">
                      Active
                    </span>
                  </div>
                </div>
              </div>

              <Button
                variant="outline"
                onClick={copyNumber}
              >
                {copied ? (
                  <>
                    <Check className="mr-2 h-4 w-4" />
                    Copied
                  </>
                ) : (
                  <>
                    <Copy className="mr-2 h-4 w-4" />
                    Copy number
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Language */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Conversation language
          </CardTitle>
        </CardHeader>

        <CardContent>
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg border bg-muted/40">
              <Globe className="h-5 w-5" />
            </div>

            <div className="flex-1">
              <p className="text-sm font-medium">
                Preferred language
              </p>

              <p className="mt-1 text-xs text-muted-foreground">
                Persynta will use this language during calls.
              </p>
            </div>

            <select
              value={settings.language}
              onChange={(e) =>
                setSettings((current) => ({
                  ...current,
                  language: e.target.value,
                }))
              }
              className="h-10 rounded-md border bg-background px-3 text-sm"
            >
              <option>English</option>
              <option>Hindi</option>
              <option>Hinglish</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Retry behavior */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Call retry behavior
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-5">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm font-medium">
                Retry unanswered calls
              </p>

              <p className="mt-1 text-xs text-muted-foreground">
                Persynta can call again when you don&apos;t answer.
              </p>
            </div>

            <button
              type="button"
              onClick={() =>
                setSettings((current) => ({
                  ...current,
                  retryCalls: !current.retryCalls,
                }))
              }
              className={`relative h-6 w-11 rounded-full transition ${
                settings.retryCalls ? "bg-black" : "bg-muted"
              }`}
            >
              <span
                className={`absolute top-1 h-4 w-4 rounded-full bg-white transition ${
                  settings.retryCalls ? "left-6" : "left-1"
                }`}
              />
            </button>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <label className="text-sm font-medium">
                Maximum attempts
              </label>

              <select
                value={settings.maxRetries}
                disabled={!settings.retryCalls}
                onChange={(e) =>
                  setSettings((current) => ({
                    ...current,
                    maxRetries: e.target.value,
                  }))
                }
                className="h-10 w-full rounded-md border bg-background px-3 text-sm"
              >
                <option value="1">1 attempt</option>
                <option value="2">2 attempts</option>
                <option value="3">3 attempts</option>
                <option value="4">4 attempts</option>
                <option value="5">5 attempts</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">
                Retry interval
              </label>

              <select
                value={settings.retryInterval}
                disabled={!settings.retryCalls}
                onChange={(e) =>
                  setSettings((current) => ({
                    ...current,
                    retryInterval: e.target.value,
                  }))
                }
                className="h-10 w-full rounded-md border bg-background px-3 text-sm"
              >
                <option value="2">2 minutes</option>
                <option value="5">5 minutes</option>
                <option value="10">10 minutes</option>
                <option value="15">15 minutes</option>
              </select>
            </div>
          </div>

          <div className="rounded-lg bg-muted/50 p-4">
            <div className="flex gap-3">
              <RefreshCw className="mt-0.5 h-4 w-4 shrink-0" />

              <p className="text-xs leading-5 text-muted-foreground">
                Example: if you don&apos;t answer the first call,
                Persynta can retry after 5 minutes, up to the
                configured maximum attempts.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quiet hours */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            Quiet hours
          </CardTitle>
        </CardHeader>

        <CardContent>
          <div className="flex items-start gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border bg-muted/40">
              <Clock className="h-5 w-5" />
            </div>

            <div>
              <p className="text-sm font-medium">
                Respect quiet hours
              </p>

              <p className="mt-1 text-xs leading-5 text-muted-foreground">
                Persynta should avoid non-urgent calls during your
                configured quiet period.
              </p>

              <Badge variant="outline" className="mt-3">
                10:00 PM – 7:00 AM
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save */}
      <div className="flex justify-end">
        <Button>Save preferences</Button>
      </div>
    </div>
  );
}