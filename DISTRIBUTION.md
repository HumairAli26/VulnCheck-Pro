# SecureAudit — Path to Public Distribution

This covers everything from "I have a packaged app" to "it's on the app stores."
Costs and accounts below are things only you can create (they require your legal
identity/payment method) — I can't sign up on your behalf.

## 0. Prerequisites (do these first, they gate everything else)

| Need | Cost | Notes |
|---|---|---|
| App icon (.ico, .icns, .png @ 1024×1024) | free–$ | No icon exists in the repo yet — add one under `assets/` |
| Apple Developer Program account | $99/yr | Required to sign + notarize macOS builds, required for Mac App Store |
| Microsoft Partner Center account | $19 one-time (individual) | Required to publish to Microsoft Store |
| A public GitHub repo (or similar) | free | Needed for the CI workflow below to run |

## 1. Build the packages (automated)

I've generated `secureaudit.spec` and `.github/workflows/build.yml`. Steps:

1. Add an `assets/icon.ico` and `assets/icon.icns` to the repo.
2. Push the repo to GitHub.
3. `git tag v0.4.0 && git push --tags` — this triggers builds on real Windows,
   macOS, and Linux runners and attaches zipped apps to a GitHub Release automatically.

At this point you already have something people can download and run — the
"send a link to friends" stage. Getting further requires signing.

## 2. Code signing (required before wide distribution)

- **Windows**: buy an OV/EV code-signing certificate (DigiCert, SSL.com, ~$70–300/yr)
  or get one via Microsoft Store submission (Store apps are signed by Microsoft
  automatically, which sidesteps buying your own cert).
- **macOS**: use your Apple Developer cert to `codesign` the `.app`, then submit
  it to Apple's `notarytool` for notarization — Gatekeeper blocks unnotarized
  apps from opening on other people's Macs by default.
- **Linux**: no OS-level signing requirement; distros/AppImage/Flatpak use their
  own trust models instead (see §4).

## 3. Store submission

### Microsoft Store
1. Convert the PyInstaller output into an **MSIX** package (`msix-packaging-tool`
   or the `pyinstaller` output + `MakeAppx.exe` from the Windows SDK).
2. Create a listing in Partner Center: description, screenshots, privacy policy URL,
   age rating.
3. Submit — automated + occasional manual review, typically 1–3 days.
4. **Flag for this app specifically**: SecureAudit reads firewall/BitLocker/process
   state. Declare the relevant capabilities in the MSIX manifest (e.g. no special
   restricted capability is needed for read-only queries via `netsh`/WMI, but be
   explicit in your store description that this is read-only auditing, not a
   system-modifying tool) — this avoids review friction.

### Mac App Store
1. Xcode (or `altool`/`notarytool`) to upload the signed, sandboxed `.app`.
2. macOS App Sandbox is mandatory for Mac App Store apps. SecureAudit's providers
   shell out to `socketfilterfw`, `fdesetup`, `softwareupdate` — **sandboxed apps
   cannot freely spawn arbitrary subprocesses**, so this is the biggest real
   engineering task, not a formality. You'll likely need to scope entitlements
   carefully or offer a "Direct Download" build (outside sandbox, notarized only)
   as the primary distribution path and treat the Mac App Store as a lighter,
   reduced-functionality version.
3. App Review focuses on: clear privacy policy, no misleading security claims,
   stable UI. Typical review time 1–3 days.

### Linux
No single store. Realistic options, roughly in order of effort:
- **Direct .zip/tarball download** (what the CI already produces) — works today.
- **AppImage** — single portable file, no install step, no distro review.
- **Flatpak (Flathub)** — closest thing Linux has to an "app store"; free, has a
  review process, good discoverability.

## 4. A real download page

App stores aren't the only "like WhatsApp" experience — WhatsApp's own site also
just offers direct downloads. A simple landing page linking to the GitHub Release
assets (Windows `.exe`, macOS `.dmg`, Linux `AppImage`) gets you 90% of the "people
can download and use it" goal without waiting on any store review. I can build
that page (HTML) anytime you want it.

## Suggested order of operations
1. Add icons, push to GitHub, tag a release → you have downloadable builds today.
2. Set up a simple download landing page.
3. Get Apple + Microsoft developer accounts (they take a few days to verify).
4. Sign + notarize the macOS build; publish direct-download version first.
5. Package MSIX, submit to Microsoft Store.
6. Solve the sandbox/subprocess issue for Mac App Store, or ship "Direct Download"
   as primary and Mac App Store as a lighter companion build later.
