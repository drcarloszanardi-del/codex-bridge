## Summary

Generated a local Spanish voice sample with Chatterbox Multilingual for job `20260525T192345-reels-generate-premium-voice-sample-chatterbox-v1`.

Output audio:
`context/asset_packs/20260525-reels-voice-test/voice_pablo_chatterbox_v1.wav`

Candidate status: `needs_orchestrator_listening`, not final publish audio.

## Coverage Table

| Requirement | Status | Evidence |
|---|---:|---|
| Chatterbox Multilingual Spanish `es` | done | `chatterbox.mtl_tts.ChatterboxMultilingualTTS`, `language_id="es"` |
| No Doctor voice or personal files | done | default bundled Chatterbox conditionals only; no Photos/iCloud/Drive used |
| No external TTS API | done | local model inference after public model download |
| Audio artifact produced | done | `context/asset_packs/20260525-reels-voice-test/voice_pablo_chatterbox_v1.wav` |
| Small enough for bridge repo | done | WAV is about 1.2 MB |
| Pronunciation check for `Pelegrini` | partial | text input uses `Centro Medico Pelegrini`; auditory confirmation remains pending |

## Motor Usado

- Engine: Chatterbox Multilingual TTS.
- Python package: `chatterbox-tts==0.1.7`.
- Backend: `torch==2.6.0`, `torchaudio==2.6.0`.
- Device used: `mps`.
- Language: `es`.
- Voice source: default public Chatterbox conditionals from `ResembleAI/chatterbox`; no private reference audio.

## Version Comando

Generation command:

```bash
HF_HOME=/private/tmp/codex_hf_cache HF_HUB_CACHE=/private/tmp/codex_hf_cache/hub /private/tmp/codex_voice_chatterbox_venv/bin/python /Users/carloszanardi/Documents/Codex/2026-05-24/vos-podrias-comunicarte-con-codex-que/scratch_generate_chatterbox_voice.py
```

Generation metadata:

```json
{
  "device": "mps",
  "duration_seconds": 26.68,
  "generate_seconds": 338.082,
  "load_seconds": 19.343,
  "sample_rate": 24000,
  "samples": 640320,
  "torch_version": "2.6.0",
  "torchaudio_version": "2.6.0",
  "total_seconds": 357.425
}
```

Final WAV container after conversion:

```json
{
  "sample_rate": 24000,
  "frames": 640320,
  "channels": 1,
  "duration_seconds": 26.68,
  "encoding": "PCM_S",
  "bits_per_sample": 16
}
```

## Licencia Asumida

`chatterbox-tts==0.1.7` reports MIT license via `pip show chatterbox-tts`.

Limit: the model-card license for `ResembleAI/chatterbox` was not independently verified from a downloaded README because only model weight/tokenizer patterns were fetched. Treat this as an internal test candidate until the orchestrator confirms the model repository license before publication.

## Duracion

26.68 seconds, mono WAV, 24 kHz, 16-bit PCM.

## Pronuncia Pelegrini

The generation input explicitly used `Centro Medico Pelegrini`, with single `l`, and `language_id="es"`.

Auditory verification remains pending because Pablo did not perform a human listening pass. The orchestrator should listen for `Pelegrini` before attaching it to the reel.

## Riesgos O Defectos Auditivos

- Candidate audio was generated successfully but is not marked final.
- Naturalness, pacing, pauses, emotional tone, and `Pelegrini` pronunciation require human/orchestrator listening.
- Generation forced EOS after an alignment-repetition warning; inspect for abrupt ending or repeated/blurred tail.
- Voice is synthetic and should be rejected if it feels artificial against the CMP visual tone.

## Risks Limits

- No Telegram/Gmail/Drive/Calendar/Photos/iCloud access used.
- No private voice reference or personal media used.
- Public model download was required from Hugging Face; inference was local.
- First local run failed under sandbox DNS restrictions; escalated network produced the model download.
- Second run exposed a `perth` import issue caused by missing `pkg_resources` with `setuptools==82.0.1`; pinned `setuptools<81` in the temp venv and reran successfully.

## Recommendation

Use `voice_pablo_chatterbox_v1.wav` only as a review candidate. The next step is for the orchestrator to place it against the approved video and perform a listening gate for naturalness and exact `Pelegrini` pronunciation.

## Confidence

Medium for technical generation and artifact integrity. Low for final audio quality because no human listening pass occurred on this worker.

## Evidence Paths

- Job: `jobs/20260525T192345-reels-generate-premium-voice-sample-chatterbox-v1.md`
- Claim: `claims/20260525T192345-reels-generate-premium-voice-sample-chatterbox-v1.json`
- Audio: `context/asset_packs/20260525-reels-voice-test/voice_pablo_chatterbox_v1.wav`
- Result: `results/20260525T192345-reels-generate-premium-voice-sample-chatterbox-v1.result.md`
- Cache used for public model: `/private/tmp/codex_hf_cache`
- Temp venv: `/private/tmp/codex_voice_chatterbox_venv`
