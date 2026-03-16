# Sharing Media in Support Requests

When reporting a bug or requesting help, attaching a recording or screenshot greatly speeds up diagnosis. This page explains how to share media effectively.

---

## Preferred Recording Formats

| Format | Notes |
|--------|-------|
| **MP4** (H.264) | Preferred — universally playable and produces small files |
| **WebM** (VP8/VP9) | Acceptable — native output of many browser screen-recorders |

**Maximum recommended file size:** 50 MB.  
If your recording exceeds 50 MB, use one of the hosting alternatives below.

### Hosting Alternatives (for large files)

- **YouTube (Unlisted):** Upload the recording, set visibility to *Unlisted*, and share the link in your issue. Unlisted videos are not discoverable by search but are accessible to anyone with the link.
- **Google Drive:** Upload the file, right-click → *Share* → *Anyone with the link can view*, then paste the link in your issue.
- **GitHub Gist / Paste:** For short log snippets, a plain-text gist is preferred over a recording.

---

## Privacy Guidance

Before sharing any recording or screenshot, review it for sensitive information:

- **Blur or redact personally identifiable information (PII):** full names, national ID numbers, phone numbers, addresses, and case reference numbers.
- **Blur authentication tokens and API keys:** JWT tokens, bearer tokens, `Authorization` header values, and any `.env` secrets visible in a terminal or browser DevTools.
- **Blur email addresses:** both in the UI and in any network request/response bodies shown in DevTools.
- **Crop or cut out** anything unrelated to the bug that may reveal personal details.

Tools such as [Kap](https://getkap.co/) (macOS), the built-in Windows Snipping Tool, [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve) (free, cross-platform), or [Shotcut](https://shotcut.org/) (free, cross-platform) make blurring easy.

---

## What to Capture for UI Debugging

To help reproduce and fix a bug quickly, include all of the following in your recording:

### 1. Browser Network Tab
1. Open **DevTools** (`F12` or `Ctrl+Shift+I` / `Cmd+Option+I`).
2. Go to the **Network** tab.
3. Check **Preserve log** so requests are not cleared on navigation.
4. Reproduce the issue.
5. Highlight the failing request and show its **Headers**, **Payload** (request body), and **Response** panels.

### 2. Browser Console
1. Stay in **DevTools** and click the **Console** tab.
2. Ensure the filter is set to **All** (not just Errors) so warnings are visible.
3. Reproduce the issue — scroll to show any red error messages or stack traces.

### 3. Backend Logs
If you have access to the server terminal (local development):

1. Start the FastAPI backend with logging visible:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```
2. Reproduce the issue in the browser.
3. Copy the relevant log lines from the terminal — look for lines prefixed with `ERROR`, `WARNING`, or Python tracebacks.
4. Paste the log output as a fenced code block in your issue (preferred over a screenshot of the terminal).

### 4. Reproduction Steps in the Recording
Begin the recording *before* you start the action that triggers the bug, and include:

- The URL visible in the address bar.
- Any form inputs you fill in (redact sensitive values).
- The exact button or action that causes the error.
- The error message or unexpected behaviour that results.

---

## Quick Checklist Before Attaching

- [ ] Recording is MP4 or WebM, ≤ 50 MB (or hosted link provided).
- [ ] PII, tokens, and emails are blurred or redacted.
- [ ] Network tab is open and the failing request is visible.
- [ ] Console tab shows any error messages.
- [ ] Backend log excerpt is included (if applicable).
- [ ] Steps to reproduce are clear from the recording.
