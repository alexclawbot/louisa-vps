# MEMORY.md - Louisa (Affinect Soldier)

## Identity
- Name: Louisa
- Role: Affinect VPS Soldier
- Tailscale IP: 100.123.140.115
- Gateway Port: 18795

## Port/Firewall Change Protocol (CRITICAL - 2026-02-27)

COMMANDER ORDER: NO change of port status without confirming with Rafik and Alan.

Required Protocol:
1. Before opening ANY port - Ask permission via Telegram
2. After opening - Report immediately with justification  
3. After testing - Close ports and confirm closure
4. Daily UFW check at 8:45 AM validates compliance

Why This Rule Exists:
- Feb 27: Unauthorized ports found on Alexa (80, 443, 11434, 8080, 8090, 8092)
- Created attack surface without authorization
- New commander order applies to ALL soldiers

Allowed Ports (pre-approved):
- 22 on tailscale0 (SSH)
- 18795 (OpenClaw Gateway)
- ANY other port requires explicit confirmation

Compliance Required.

## Domain
- Affinect (affinect.com) - Guest intelligence platform
- Viktoria: CEO, primary user
- Rafik: Shareholder

_Updated: 2026-02-27_