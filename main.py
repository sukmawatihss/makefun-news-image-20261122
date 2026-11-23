"""THE FIELD WIRE — halaman kabar lapangan untuk @sukmawatihss (Akun 15).

Skrip rilis NI22 Wave 7: memeriksa berkas gambar di folder ini lalu
menyalinnya utuh ke direktori keluaran yang ditentukan harness.
Catatan lapangan: tidak ada byte yang diubah selama penyalinan.
"""

import hashlib
import os
import struct
import sys

CONCEPT = "THE FIELD WIRE"
ACCOUNT = "@sukmawatihss"
ACCOUNT_LABEL = "Akun 15"
BOUNTY = "news-image-20261122"
STORIES = 36
MAX_SIDE = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        return fail("entry.png tidak ditemukan di sebelah main.py")

    with open(source, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33:
        return fail("header PNG terlalu pendek untuk diperiksa")
    if header[:8] != PNG_SIGNATURE:
        return fail("signature PNG tidak sah")
    if header[12:16] != b"IHDR":
        return fail("chunk pertama bukan IHDR")
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail(f"dimensi {width}x{height} melampaui batas {MAX_SIDE}")

    with open(source, "rb") as handle:
        payload = handle.read()
    size = len(payload)
    digest = hashlib.sha256(payload).hexdigest()

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(payload)

    with open(target, "rb") as handle:
        copied = handle.read()
    if len(copied) != size or hashlib.sha256(copied).hexdigest() != digest:
        return fail("salinan keluaran tidak sama persis dengan sumber")

    print(f"Concept: {CONCEPT}")
    print(f"Account: {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty: {BOUNTY}")
    print("File: entry.png")
    print(f"Size: {size} bytes")
    print(f"Dim: {width}x{height}")
    print(f"SHA256: {digest}")
    print(f"Stories: {STORIES}")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
