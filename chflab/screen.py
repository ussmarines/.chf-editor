"""Opt-in local game-window capture; no OCR, uploads or visual-validation claims."""
import ctypes
from datetime import datetime, timezone
from ctypes import wintypes
from pathlib import Path
import sys


def game_window():
    if sys.platform != 'win32':
        raise ValueError('Game-window capture requires Windows')
    user = ctypes.WinDLL('user32', use_last_error=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    user.GetForegroundWindow.argtypes = ()
    user.GetForegroundWindow.restype = wintypes.HWND
    user.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
    user.GetWindowThreadProcessId.restype = wintypes.DWORD
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.QueryFullProcessImageNameW.argtypes = (wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD))
    kernel.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.CloseHandle.restype = wintypes.BOOL
    hwnd = user.GetForegroundWindow()
    pid = wintypes.DWORD()
    if not hwnd or not user.GetWindowThreadProcessId(hwnd, ctypes.byref(pid)):
        raise ValueError('No foreground game window')
    process = kernel.OpenProcess(0x1000, False, pid.value)  # QUERY_LIMITED_INFORMATION
    if not process:
        raise ValueError('Cannot identify foreground process')
    try:
        capacity = wintypes.DWORD(32768)
        name = ctypes.create_unicode_buffer(capacity.value)
        if not kernel.QueryFullProcessImageNameW(process, 0, name, ctypes.byref(capacity)):
            raise ValueError('Cannot identify foreground process')
        if Path(name.value).name.lower() != 'starcitizen.exe':
            raise ValueError('Put Star Citizen in the foreground to capture its window')
    finally:
        kernel.CloseHandle(process)
    return hwnd


def capture_game():
    try:
        from PIL import ImageGrab
    except ImportError as error:
        raise ValueError('Install the optional requirements-monitor.txt in this Python environment') from error
    hwnd = game_window()
    method = 'window'
    try:
        frame = ImageGrab.grab(window=hwnd).convert('RGB')
    except (OSError, RuntimeError):
        frame = None
    if not usable_frame(frame):
        # Rendered graphics may not be available through the window capture API.
        frame = visible_game_frame(hwnd)
        method = 'visible_game_area'
    if game_window() != hwnd:
        raise ValueError('Foreground window changed during capture; image discarded')
    if not usable_frame(frame):
        raise ValueError('Window and visible-area captures are empty/uniform; keep BioCorp visible and retry')
    frame.thumbnail((1920, 1080))
    frame.info['capture_method'] = method
    frame.info['capture_time_utc'] = datetime.now(timezone.utc).isoformat()
    return frame


def usable_frame(frame):
    return (frame is not None and frame.width > 0 and frame.height > 0
            and not all(lo == hi for lo, hi in frame.getextrema()))


def client_box(hwnd, user):
    user.GetClientRect.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.RECT))
    user.GetClientRect.restype = wintypes.BOOL
    user.ClientToScreen.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.POINT))
    user.ClientToScreen.restype = wintypes.BOOL
    user.IsIconic.argtypes = (wintypes.HWND,)
    user.IsIconic.restype = wintypes.BOOL
    rect = wintypes.RECT()
    origin = wintypes.POINT(0, 0)
    if user.IsIconic(hwnd) or not user.GetClientRect(hwnd, ctypes.byref(rect)) or not user.ClientToScreen(hwnd, ctypes.byref(origin)):
        raise ValueError('Cannot locate the visible game client area')
    if rect.right <= 0 or rect.bottom <= 0:
        raise ValueError('Game client area is empty')
    return (origin.x, origin.y, origin.x + rect.right, origin.y + rect.bottom)


def visible_game_frame(hwnd):
    from PIL import ImageGrab
    user = ctypes.WinDLL('user32', use_last_error=True)
    user.SetThreadDpiAwarenessContext.argtypes = (wintypes.HANDLE,)
    user.SetThreadDpiAwarenessContext.restype = wintypes.HANDLE
    previous = user.SetThreadDpiAwarenessContext(ctypes.c_void_p(-4))
    if not previous:
        raise ValueError('Cannot enable physical-pixel coordinates for game capture')
    try:
        if game_window() != hwnd:
            raise ValueError('Game lost foreground before visible-area capture')
        box = client_box(hwnd, user)
        frame = ImageGrab.grab(bbox=box, all_screens=True).convert('RGB')
        if game_window() != hwnd or client_box(hwnd, user) != box:
            raise ValueError('Game focus or position changed during capture; image discarded')
        return frame
    finally:
        user.SetThreadDpiAwarenessContext(previous)


def pixel_change(before, after):
    """Whole-window metric includes animation, lighting and UI, not just the face."""
    from PIL import ImageChops, ImageStat
    if before.size != after.size:
        return None
    diff = ImageChops.difference(before.convert('RGB'), after.convert('RGB'))
    return round(sum(ImageStat.Stat(diff).mean) / (3 * 255) * 100, 3)
