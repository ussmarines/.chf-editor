"""Resolve and check a user-supplied native Zstandard library; no downloads."""
import ctypes
import os
from pathlib import Path
import sys


def discover_zstd():
    """Offer existing libraries from explicit environment / Python locations."""
    candidates = []
    configured = os.environ.get("CHF_ZSTD_DLL")
    if configured:
        candidates.append(Path(configured).expanduser())
    for directory in (Path(sys.executable).parent, Path(sys.prefix) / "DLLs",
                      Path(sys.prefix) / "Library" / "bin"):
        candidates.extend(directory / name for name in ("libzstd.dll", "zstd.dll"))
    found = []
    for path in candidates:
        if path.is_file() and path.resolve() not in found:
            found.append(path.resolve())
    return found


def check_zstd(path):
    """Check required API exports and an actual compression/decompression roundtrip."""
    path = Path(path).expanduser()
    if not path.is_file():
        raise ValueError("Select an existing Zstandard DLL, or set CHF_ZSTD_DLL.")
    try:
        lib = ctypes.CDLL(str(path.resolve()))
        lib.ZSTD_versionString.argtypes = ()
        lib.ZSTD_versionString.restype = ctypes.c_char_p
        lib.ZSTD_compressBound.argtypes = (ctypes.c_size_t,)
        lib.ZSTD_compressBound.restype = ctypes.c_size_t
        lib.ZSTD_compress.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                                     ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int)
        lib.ZSTD_compress.restype = ctypes.c_size_t
        lib.ZSTD_decompress.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                                       ctypes.c_void_p, ctypes.c_size_t)
        lib.ZSTD_decompress.restype = ctypes.c_size_t
        lib.ZSTD_isError.argtypes = (ctypes.c_size_t,)
        lib.ZSTD_isError.restype = ctypes.c_uint
        sample = b"CHF Editor native library check"
        source = ctypes.create_string_buffer(sample)
        compressed = ctypes.create_string_buffer(lib.ZSTD_compressBound(len(sample)))
        size = lib.ZSTD_compress(compressed, len(compressed), source, len(sample), 1)
        if lib.ZSTD_isError(size):
            raise ValueError("Zstandard compression self-check failed.")
        output = ctypes.create_string_buffer(len(sample))
        actual = lib.ZSTD_decompress(output, len(sample), compressed, size)
        if lib.ZSTD_isError(actual) or actual != len(sample) or output.raw != sample:
            raise ValueError("Zstandard decompression self-check failed.")
        return {"path": str(path.resolve()), "version": lib.ZSTD_versionString().decode("ascii"),
                "roundtrip": "PASS"}
    except (OSError, AttributeError) as error:
        raise ValueError("This DLL is not a compatible Zstandard library for this Python installation.") from error


def resolve_zstd(explicit=None):
    """An explicit path or configured environment never silently falls back."""
    if explicit:
        path = Path(explicit).expanduser()
    elif os.environ.get("CHF_ZSTD_DLL"):
        path = Path(os.environ["CHF_ZSTD_DLL"]).expanduser()
    else:
        found = discover_zstd()
        if not found:
            raise ValueError("Zstandard DLL not found. Use --zstd-dll or set CHF_ZSTD_DLL.")
        path = found[0]
    check_zstd(path)
    return path.resolve()
