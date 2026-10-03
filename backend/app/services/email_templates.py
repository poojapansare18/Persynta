from datetime import datetime


def meeting_confirmation_email(
    *,
    title: str,
    agenda: str | None,
    start_at: datetime,
    end_at: datetime,
    meeting_url: str | None,
    confirmation_url: str,
    change_url: str | None = None,
    cancel_url: str | None = None,
) -> tuple[str, str]:
    """
    Build the confirmation email for a Persynta meeting.

    Returns:
        (html, text)
    """

    date_text = start_at.strftime("%A, %d %B %Y")
    start_text = start_at.strftime("%I:%M %p")
    end_text = end_at.strftime("%I:%M %p")

    agenda_html = ""
    agenda_text = ""

    if agenda:
        agenda_html = f"""
        <p style="margin: 0 0 20px 0;">
            <strong>Agenda:</strong><br>
            {agenda}
        </p>
        """

        agenda_text = f"Agenda: {agenda}\n\n"

    meeting_link_html = ""
    meeting_link_text = ""

    if meeting_url:
        meeting_link_html = f"""
        <p>
            <a href="{meeting_url}"
               style="
                   display: inline-block;
                   padding: 10px 16px;
                   background: #111827;
                   color: #ffffff;
                   text-decoration: none;
                   border-radius: 8px;
               ">
                Open Google Meet
            </a>
        </p>
        """

        meeting_link_text = f"Google Meet: {meeting_url}\n\n"

    change_html = ""

    if change_url:
        change_html = f"""
        <a href="{change_url}"
           style="
               display: inline-block;
               padding: 10px 16px;
               border: 1px solid #d1d5db;
               color: #111827;
               text-decoration: none;
               border-radius: 8px;
               margin-left: 8px;
           ">
            Change
        </a>
        """

    cancel_html = ""

    if cancel_url:
        cancel_html = f"""
        <a href="{cancel_url}"
           style="
               display: inline-block;
               padding: 10px 16px;
               border: 1px solid #d1d5db;
               color: #6b7280;
               text-decoration: none;
               border-radius: 8px;
               margin-left: 8px;
           ">
            Cancel
        </a>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Confirm your Persynta meeting</title>
</head>

<body style="
    margin: 0;
    padding: 40px 20px;
    background: #f7f7f8;
    font-family: Arial, sans-serif;
    color: #111827;
">

<div style="
    max-width: 560px;
    margin: 0 auto;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 32px;
">

    <p style="
        margin: 0 0 24px 0;
        font-size: 14px;
        color: #6b7280;
    ">
        Persynta
    </p>

    <h1 style="
        margin: 0 0 12px 0;
        font-size: 24px;
        color: #111827;
    ">
        Confirm your meeting
    </h1>

    <p style="
        margin: 0 0 24px 0;
        color: #4b5563;
    ">
        Please review the meeting details before scheduling it.
    </p>

    <div style="
        padding: 20px;
        background: #f9fafb;
        border-radius: 10px;
        margin-bottom: 24px;
    ">

        <h2 style="
            margin: 0 0 16px 0;
            font-size: 18px;
        ">
            {title}
        </h2>

        <p style="margin: 0 0 10px 0;">
            <strong>Date:</strong> {date_text}
        </p>

        <p style="margin: 0 0 10px 0;">
            <strong>Time:</strong> {start_text} – {end_text}
        </p>

        {agenda_html}

    </div>

    <div style="margin-bottom: 24px;">

        <a href="{confirmation_url}"
           style="
               display: inline-block;
               padding: 11px 18px;
               background: #111827;
               color: #ffffff;
               text-decoration: none;
               border-radius: 8px;
           ">
            Confirm &amp; Schedule
        </a>

        {change_html}
        {cancel_html}

    </div>

    {meeting_link_html}

    <p style="
        margin: 28px 0 0 0;
        font-size: 12px;
        color: #9ca3af;
    ">
        This message was sent by Persynta.
        If you did not request this meeting, you can ignore this email.
    </p>

</div>

</body>
</html>
"""

    text = (
        "PERSYNTA\n\n"
        "Confirm your meeting\n\n"
        f"Title: {title}\n"
        f"Date: {date_text}\n"
        f"Time: {start_text} – {end_text}\n\n"
        f"{agenda_text}"
        f"Confirm & Schedule: {confirmation_url}\n"
    )

    if change_url:
        text += f"Change: {change_url}\n"

    if cancel_url:
        text += f"Cancel: {cancel_url}\n"

    text += f"\n{meeting_link_text}"

    return html, text