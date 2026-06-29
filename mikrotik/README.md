# MikroTik Hotspot Files (RouterOS 7)

The customized hotspot login directory served by the **MikroTik**
(`login.aut.ac.ir`). These files delegate the whole login/status/logout UX to
the FastAPI portal in this repo (`internet.aut.ac.ir`).

## Topology

| Host                  | Role                                                                 |
| --------------------- | ------------------------------------------------------------------- |
| `login.aut.ac.ir`     | The MikroTik. Serves these files and performs the RADIUS auth at `/login`. |
| `internet.aut.ac.ir`  | This FastAPI app. Renders the branded login form + status/logout pages. |

### Flow

1. Unauthenticated client → MikroTik intercepts → `redirect.html` / `rlogin.html`
   / `login.html` issue a **302 to `https://internet.aut.ac.ir/?dst=…`**.
2. The portal renders the login form (`templates/index.html`), whose
   `action` is `login_urls["1"] = https://login.aut.ac.ir/login` — so the
   credentials POST goes **back to the MikroTik**, which authenticates via RADIUS.
3. Success → `alogin.html` 302s to `https://internet.aut.ac.ir/status`.
   Failure → `login.html` 302s back to the portal with `&error=…`.
4. Logout → `logout.html` 302s to `https://internet.aut.ac.ir/logout`.

The login form is therefore **only ever shown on `internet.aut.ac.ir`**; the
MikroTik pages are thin 302 redirect stubs.

## Upgrading from the RouterOS 6 bundle — what changed

- **`api.json`** (new in RouterOS 7): the RFC 8908 captive-portal API.
  `user-portal-url` points at `https://internet.aut.ac.ir/` so OS captive-portal
  detection (iOS/Android/macOS) lands on our portal.
- **`login.html`**: was a full form POSTing to the now-defunct
  `login2.aut.ac.ir`; replaced with a redirect stub to `internet.aut.ac.ir`
  (carrying `dst` + `error`).
- Stock RouterOS 7 assets `css/style.css`, `img/user.svg`, `img/password.svg`
  are intentionally **omitted** — our login UI lives on the portal.

## Secrets — read before deploying

The hotspot HTTPS certificate's **private key is NOT in git** (`.gitignore`
blocks `*.key`). `fullchain.crt` (public) is kept. Import the cert + key onto the
router out-of-band:

```
/certificate import file-name=fullchain.crt
/certificate import file-name=<private-key>
```

## Deploy to the router

Upload the directory to the router's `hotspot/` files (Files → drag, or scp/ftp),
then point the hotspot profile's `html-directory` at it. The `hotspot-v7.zip`
build artifact (also key-free) is for handing to the team.

## Legacy still in this folder (review / prune)

These predate the `internet.aut.ac.ir` portal and reference the old
`slogin.aut.ac.ir` server or are stock MikroTik leftovers — kept for now, safe to
delete if unused:

- `login1.html`, `login2.html`, `rlogin1.html`, `rlogin2.html`, `alogin2.html`
- `slogin/` (old separate portal)
- `lv/` (stock MikroTik Latvian example, incl. a nested `hotspot.zip`)
- `filter.rsc` (a RouterOS **6.37** `/ip firewall` export — not a hotspot page)
