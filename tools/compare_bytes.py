"""
compare_dumps.py
----------------
Find bytes that consistently differ between two groups of hex dumps.
Addresses start at a given address, for example: (first byte = C000, second = C001, etc.)

Condition for a candidate:
  - All RED dumps agree at that position
  - All WHITE dumps agree at that position
  - RED value != WHITE value
"""

# ---------------------------------------------------------------------------
# Paste your dumps here — space-separated hex bytes
# ---------------------------------------------------------------------------

RED_DUMPS = [
	"78 F0 11 CF 00 00 FF 87 FC BF 00 FF FF FF FF FF FF FF 11 80 BF F3 FF BF FF 3F 00 FF BF 7F FF 9F FF BF FF FF 00 00 BF 77 F3 F1 FF FF FF FF FF FF FF FF FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF F3 41 30 10 90 06 DE 00 E4 E4 78 07 FF 80 FF 00 FF FF FF FF FF FF 3E FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 37 00 FE FF FF FF F8 FF 00 00 00 8F 00 00 FF FF FF FF FF FF FF FF 01 00 00 00 00 00 00 00 00 00 63 9C 10 01 00 00 00 00 00 00 0A 00 3E DE E0 46 3E 28 3D 20 FD C9 00 00 00 00 00 E3 00 10 30 07 78 00 03 01 83 00 00 00 00 67 00 03 08 0D 00 0E 12 01 03 00 00 00 00 FF 03 A6 B0 03 00 44 00 D0 9A 01 04 1E 00 00 00 00 00 00 F1 00 00 00 05 01 00 01 00 00 01 01 01 00 00 22 03 08 C0 57 01 D8 53 01 D0 07 00 00 E8 03 00 00 01 01 00 00 01 00 00 00 00 00 0B 03",
	"78 F0 11 CF 00 00 FF 3C FC BF 00 FF FF FF FF FF FF FF 11 80 BF F3 FF BF FF 3F 00 FF BF 7F FF 9F FF BF FF FF 00 00 BF 77 F3 F1 FF FF FF FF FF FF FF FF FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF F3 41 50 30 90 06 DE 00 E4 E4 60 07 FF 80 FF 00 FF FF FF FF FF FF 3E FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 37 00 FE FF FF FF F8 FF 00 00 00 8F 00 00 FF FF FF FF FF FF FF FF 01 00 00 00 00 00 00 00 00 00 10 1A 02 01 00 00 00 00 00 00 0A 00 3E DE E0 46 3E 28 3D 20 FD C9 00 00 00 00 00 E3 00 30 50 07 60 00 03 01 90 01 00 00 00 97 00 04 10 0D 04 0E 12 03 05 00 00 00 01 FF 03 A6 B0 03 00 51 00 D0 9A 00 02 00 00 00 00 00 00 00 F1 00 00 00 05 01 00 01 00 00 01 01 01 00 00 22 08 07 C0 57 01 D8 53 01 D0 07 00 00 E8 03 00 00 01 01 00 00 01 00 00 00 00 00 0B 03",
	"78 F0 11 CF 00 00 FF 58 FC BF 00 FF FF FF FF FF FF FF 11 80 BF F3 FF BF FF 3F 00 FF BF 7F FF 9F FF BF FF FF 00 00 BF 77 F3 F1 FF FF FF FF FF FF FF FF FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF F3 41 A0 30 90 06 DE 00 E4 E4 78 07 FF 80 FF 00 FF FF FF FF FF FF 3E FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 37 00 FE FF FF FF F8 FF 00 00 00 8F 00 00 FF FF FF FF FF FF FF FF 01 00 00 00 00 00 00 00 00 00 60 9C 14 08 08 00 00 00 00 00 0A 00 3E DE E0 46 3E 28 3D 20 FD C9 00 00 00 00 00 E3 00 30 A0 07 78 00 03 01 DF 00 00 00 00 CF 00 03 08 0D 01 0E 12 03 0A 00 00 00 00 FF 03 A6 B0 03 00 77 00 D0 9A 00 00 00 00 00 00 00 00 00 F1 00 00 00 05 01 00 01 00 00 01 01 01 00 00 22 08 11 C0 57 01 D8 53 01 D0 07 00 00 E8 03 00 00 01 01 00 00 01 00 00 00 00 00 0B 03",
]

WHITE_DUMPS = [
	"78 F0 11 CF 00 00 FF 0B FF BF 00 FF FF FF FF FF FF FF 11 80 BF F3 FF BF FF 3F 00 FF BF 7F FF 9F FF BF FF FF 00 00 BF 77 F3 F1 FF FF FF FF FF FF FF FF FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF E3 41 30 60 90 06 DE 00 E4 E4 90 07 FF 80 FF 00 FF FF FF FF FF FF 3E FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 37 00 FE FF FF FF F8 FF 00 00 00 8F 00 00 FF FF FF FF FF FF FF FF 01 00 00 00 00 00 00 00 00 00 00 1D 14 08 08 00 00 00 00 00 12 00 3E DE E0 46 3E 28 3D 20 FD C9 00 00 00 00 00 E3 00 60 30 07 90 00 03 01 94 00 00 00 00 B8 00 02 00 0D 00 0E 12 06 03 00 00 00 00 FF 03 A6 B0 03 00 2C 00 D0 9A 00 00 00 00 00 00 00 00 00 6A 00 01 00 05 01 00 01 00 00 01 01 01 00 00 22 0C 07 C0 57 01 9F 86 01 D0 07 00 00 E8 03 00 00 01 01 00 00 01 00 00 00 00 00 0B 03",
	"78 F0 11 CF 00 00 FF AA FF BF 00 FF FF FF FF FF FF FF 11 80 BF F3 FF BF FF 3F 00 FF BF 7F FF 9F FF BF FF FF 00 00 BF 77 F3 F1 FF FF FF FF FF FF FF FF FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF F3 41 50 30 90 06 DE 00 E4 E4 60 07 FF 80 FF 00 FF FF FF FF FF FF 3E FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 37 00 FE FF FF FF F8 FF 00 00 00 8F 00 00 FF FF FF FF FF FF FF FF 01 00 00 00 00 00 00 00 00 00 12 1A 02 09 09 00 00 00 00 00 12 00 3E DE E0 46 3E 28 3D 20 FD C9 00 00 00 00 00 E3 00 30 50 07 60 00 03 01 01 01 00 00 00 54 00 03 10 0D 04 0E 12 03 05 00 00 00 01 FF 03 A6 B0 03 00 04 00 D0 9A 00 02 00 00 00 00 00 00 00 6A 00 01 00 05 01 00 01 00 00 01 01 01 00 00 22 09 07 C0 57 01 9F 86 01 D0 07 00 00 E8 03 00 00 01 01 00 00 01 00 00 00 00 00 0B 03",
	"78 F0 11 CF 00 00 FF 3A FF BF 00 FF FF FF FF FF FF FF 11 80 BF F3 FF BF FF 3F 00 FF BF 7F FF 9F FF BF FF FF 00 00 BF 77 F3 F1 FF FF FF FF FF FF FF FF FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF 00 FF E3 41 20 30 90 06 DE 00 E4 E4 90 07 FF 80 FF 00 FF FF FF FF FF FF 3E FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 37 00 FE FF FF FF F8 FF 00 00 00 8F 00 00 FF FF FF FF FF FF FF FF 01 00 00 00 00 00 00 00 00 00 46 19 0C 09 09 00 00 00 00 00 12 00 3E DE E0 46 3E 28 3D 20 FD C9 00 00 00 00 00 E3 00 30 20 07 90 00 03 01 1E 00 00 00 00 80 00 01 00 0D 04 0E 12 03 02 00 00 00 03 FF 03 A6 B0 03 00 B2 00 86 98 01 01 00 01 00 00 00 00 00 6A 00 01 00 05 01 00 01 00 00 01 01 01 00 00 22 08 07 C0 57 01 9F 86 01 D0 07 00 00 E8 03 00 00 01 01 00 00 01 00 00 00 00 00 0B 03"
]

# Starting address of the dump (first byte = this address)
START_ADDR = 0xFF00

# ---------------------------------------------------------------------------
# Logic — no need to edit below this line
# ---------------------------------------------------------------------------

def parse(raw: str) -> list[int]:
    return [int(b, 16) for b in raw.split()]


def compare(group_a: list[list[int]], group_b: list[list[int]]) -> None:
    lengths = [len(d) for d in group_a + group_b]
    min_len = min(lengths)
    max_len = max(lengths)
    if min_len != max_len:
        print(f"[!] Dumps differ in length (min={min_len}, max={max_len}).")
        print(f"    Comparing only the first {min_len} bytes.\n")

    candidates = []
    for pos in range(min_len):
        vals_a = [d[pos] for d in group_a]
        vals_b = [d[pos] for d in group_b]

        if len(set(vals_a)) == 1 and len(set(vals_b)) == 1 and vals_a[0] != vals_b[0]:
            addr = START_ADDR + pos
            candidates.append((addr, vals_a[0], vals_b[0]))

    # ── output ──────────────────────────────────────────────────────────────
    print("=" * 60)
    print(f"  {len(candidates)} candidate(s) found  "
          f"(range 0x{START_ADDR:04X}–0x{START_ADDR + min_len - 1:04X})")
    print("=" * 60)

    if not candidates:
        print("\n  No consistent differences found.")
        print("  Make sure dumps were taken at equivalent game states.")
        return

    na = len(group_a)
    nb = len(group_b)
    a_hdr = "  ".join(f"R{i+1}" for i in range(na))
    b_hdr = "  ".join(f"W{i+1}" for i in range(nb))
    print(f"\n  {'Address':<12} {'Red':<8} {'White':<8}  [{a_hdr}]  [{b_hdr}]")
    print(f"  {'-'*12} {'-'*8} {'-'*8}  {'-'*len(a_hdr)}  {'-'*len(b_hdr)}")

    for addr, a_val, b_val in candidates:
        pos     = addr - START_ADDR
        a_bytes = "  ".join(f"{d[pos]:02X}" for d in group_a)
        b_bytes = "  ".join(f"{d[pos]:02X}" for d in group_b)
        print(f"  0x{addr:04X}        {a_val:02X}      {b_val:02X}      "
              f"[{a_bytes}]  [{b_bytes}]")

    # Plain address list for easy copy-paste
    print("\n  Candidate addresses:")
    print("  " + ", ".join(f"0x{addr:04X}" for addr, *_ in candidates))


if __name__ == "__main__":
    red   = [parse(d) for d in RED_DUMPS]
    white = [parse(d) for d in WHITE_DUMPS]
    compare(red, white)
