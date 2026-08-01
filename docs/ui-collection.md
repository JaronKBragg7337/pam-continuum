# UI Collection Protocol

PAM Continuum uses visible browser and desktop-app sessions for AI collection. This is intentional: account context, model availability, refusals, UI behavior, and actual user-facing usage are part of the observation.

## Session sequence

1. Select exactly one returned browser or app window.
2. Verify the session is already signed in without entering credentials.
3. Open or start a fresh conversation.
4. Send only the mission-scoped prompt; keep private workspace material out unless explicitly scoped.
5. Wait for generation to finish.
6. Capture the visible response and mechanical metadata.
7. Classify the result as substantive, refused, unavailable, truncated, deflected, or empty.
8. Store the raw capture locally before synthesis.
9. Close or leave the surface in a neutral state without changing account settings.

## Current surface notes

- Claude desktop session: observed signed in and ready.
- Comet / Perplexity session: observed signed in and ready.
- Gemini: user-confirmed signed-in browser session; verify at capture time.
- Grok: user-confirmed signed-in browser session; verify at capture time.
- Kimi: not yet verified in the current Windows session.
- DeepSeek: not yet verified in the current Windows session.
- Other browser sources: verify on first use.

The public repository records the protocol, not account identifiers or credentials. Local session observations remain private.
