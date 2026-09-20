# Mobile App (`mobile/`)

Owner: Leawi Taddesse

React Native mobile application: image capture/upload, sends the image to
the backend (`../backend/`), displays the corrected text in an editable
interface, and handles saving/exporting the final document.

## Folder layout

```
mobile/
└── src/
    ├── screens/      Top-level app screens
    ├── components/   Reusable UI components
    └── services/     API calls to the backend
```

## Setup

This project has not been initialized with a specific React Native tooling
choice yet (e.g. plain React Native CLI vs. Expo). Once decided, initialize
the project inside this folder and commit the generated `package.json`,
config files, and native project folders as appropriate.

```bash
cd mobile
# e.g. with Expo:
# npx create-expo-app .
# or with React Native CLI:
# npx react-native init AmharicOCRApp
```

## Planned screens

- **Capture/Upload** — camera capture or image upload
- **Review & Edit** — displays recognized + corrected text, editable
- **Export** — save/export the final document

## Status

Scaffold only — the React Native project has not been initialized yet.
