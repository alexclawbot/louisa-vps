# Sales Call Logger

Internal Android app for tracking sales team calls.

## Features
- ✅ Automatic call detection (incoming, outgoing, missed)
- ✅ Captures: Phone number, timestamp, call duration, call type
- ✅ **Salesperson tracking** — each user enters their name on first launch
- ✅ SQLite local storage
- ✅ Export to CSV (includes salesperson column)
- ✅ API integration ready (hooks included)

## Build Instructions

1. Open in Android Studio
2. Sync Gradle
3. Build → Run on device

## Permissions Required
- `READ_CALL_LOG` - Access call history
- `READ_PHONE_STATE` - Detect call state changes
- `FOREGROUND_SERVICE` - Run background service (Android 9+)
- `POST_NOTIFICATIONS` - Show service notification (Android 13+)

## Important: Foreground Service
The app runs as a **foreground service** (shows persistent notification) to comply with Android 9+ requirements. This is mandatory for call monitoring apps.

## App Structure
```
app/src/main/java/com/advplus/calllogger/
├── MainActivity.java          # Main UI - view/export logs, salesperson setup
├── CallMonitoringService.java # Background call monitor
├── CallLogDatabaseHelper.java # SQLite database operations
├── CallLogAdapter.java        # RecyclerView adapter
├── PrefsManager.java          # SharedPreferences for salesperson name
├── models/CallLogEntry.java   # Data model (includes salesperson)
└── api/ApiClient.java         # API integration (stub - implement later)
```

## API Integration
See `ApiClient.java` - implement your endpoint in `uploadCallLog()`
