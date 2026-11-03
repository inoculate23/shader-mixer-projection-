# SQUAAWKE Dome Visual Instrument

A personally owned browser-based audiovisual performance instrument developed for Craig Ellenwood.

Built with original JavaScript, WebGL shaders, and the Web Audio API. No third-party runtime dependencies.

## Features

- Two independently controlled shader decks
- Three original procedural visual patterns
- A/B crossfade
- Audio-reactive color and luminance
- Per-deck speed, scale, color, and audio influence
- Microphone/audio-interface input
- Local audio-file playback
- Silent demo modulation
- Standard 1920 × 1080 projection output
- Circular 180-degree equidistant fisheye dome output
- Separate projection window and fullscreen controls
- Master exposure, blackout, and animation freeze

## Development

Requires Node.js 22 or later.

    npm test
    npm run build
    npm run dev

Open http://localhost:5173.

No dependency installation is required. Microphone access requires localhost or HTTPS.

## Netlify

Build command:

    npm test && npm run build

Publish directory:

    dist

These settings are included in netlify.toml.

A private repository does not make a deployed browser application private. Enable Netlify visitor access protection to restrict access to the application and its source.

## Controls

- Space: freeze procedural animation time
- B: toggle blackout
- Left/right arrows: adjust crossfade
- F: fullscreen output

Audio modulation and manual controls remain active while animation time is frozen.

## Architecture

- src/model.js: state defaults, geometry, and frequency bands
- src/audio.js: audio sources and analysis
- src/renderer.js: shaders and projection rendering
- src/app.js: interface and performance controls
- output.html: separate projection surface

The modular structure supports future preset management and multiple projection surfaces. Preset storage and multi-wall calibration are not implemented in this MVP.

## Testing

Six automated unit tests pass.

An additional cloud EGL/GLES2 integration test validates shader compilation, three visual patterns, both projection modes, crossfade behavior, dome masking, and blackout.

The cloud browser could not create a WebGL context. Browser rendering, full-resolution performance, real audio inputs, and physical dome alignment require testing on the intended performance hardware.

## Ownership

Copyright ©2026 Craig Ellenwood

## License

Copyright © 2026 Craig Ellenwood.

Licensed under the MIT License. See LICENSE.
