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

## Development Roadmap

SQUAAWKE Dome Visual Instrument is an actively developed, browser-based audiovisual performance system designed for live electronic music, immersive installations, and fulldome projection.

The following features are planned for future development and are not yet implemented in the current MVP.

### 1. Video Input Support

- Import and play local video files.

- Use video sources independently on either mixer deck.

- Support live camera and capture-device input.

- Apply shaders and visual effects to video sources.

- Crossfade between video, procedural shaders, and mixed content.

- Add playback speed, looping, seeking, and transport controls.

- Support common browser-compatible video formats.

### 2. Recording and Export

- Record the final mixed audiovisual output.

- Capture synchronized audio and video.

- Export recordings in browser-supported formats.

- Provide configurable recording resolution and frame rate.

- Support 16:9 standard video and 180-degree fisheye dome recording.

- Add start, stop, pause, and recording-status controls.

- Support high-resolution output for post-production workflows.

### 3. Live Streaming

- Stream live audiovisual performances.

- Integrate with OBS Studio and compatible broadcast software.

- Explore WebRTC and browser-based streaming protocols.

- Provide a dedicated clean video output without interface controls.

- Support configurable stream resolution and frame rate.

- Add stream monitoring, connection status, and error reporting.

- Maintain synchronization between audio and visual output.

### 4. Projection Mapping, Blending, and Calibration

- Add projection alignment grids and calibration test patterns.

- Implement four-corner geometry adjustment and keystone correction.

- Support mesh-based warping for irregular projection surfaces.

- Implement adjustable edge-blending zones for overlapping projectors.

- Add blend feathering, gamma adjustment, and brightness matching.

- Support multiple projectors and independent output surfaces.

- Provide configurable multi-wall projection layouts.

- Save and recall venue-specific calibration profiles.

- Support immersive four-wall installations and panoramic projection.

- Develop calibration tools for fulldome and curved projection surfaces.

### 5. Preset and Performance Management

- Save and recall shader configurations.

- Create performance-ready preset banks.

- Support transitions between saved visual scenes.

- Add MIDI and OSC control mapping.

- Provide timeline-based automation and cue triggering.

- Support external audio synchronization and beat detection.

### 6. Performance and Reliability

- Optimize GPU rendering for high-resolution projection.

- Improve performance with multiple simultaneous video sources.

- Add automatic recovery from media-input and rendering errors.

- Provide performance monitoring for frame rate and GPU load.

- Test on multiple operating systems and graphics configurations.

- Validate projector alignment and blending on physical hardware.

## Development Priorities

| Phase | Focus | Status |

|-------|-------|--------|

| 1 | Dual-deck shader mixer and audio reactivity | Implemented |

| 2 | Standard and 180-degree fisheye projection | Implemented |

| 3 | Video input and live capture | Planned |

| 4 | Recording and audiovisual export | Planned |

| 5 | Live streaming and OBS integration | Planned |

| 6 | Projection calibration and edge blending | Planned |

| 7 | Multi-projector and four-wall output | Planned |

| 8 | Preset management, MIDI, and OSC | Planned |

| 9 | Hardware validation and performance optimization | Planned |

## Project Direction

The long-term goal is a modular, real-time audiovisual performance environment capable of supporting conventional screens, multi-projector immersive installations, and 180-degree fulldome presentations.

The system is being developed as an independent creative coding project, with future capabilities including live video processing, recording, streaming, spatial projection calibration, and advanced performance control.

Development will prioritize modular architecture

## Ownership

Copyright ©2026 Craig Ellenwood

## License

Copyright © 2026 Craig Ellenwood.

Licensed under the MIT License. See LICENSE.
