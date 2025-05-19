```mermaid
---
config:
    look: handDrawn
    theme: dark
---

erDiagram
    USERS ||--|{ ATTENDANCE : have
    ATTENDANCE }|--|| EVENT_INSTANCES: at
    ATTENDANCE }|..|{ ATTENDANCE_TYPES : "are of type(s)"
    EVENT_INSTANCES }|..|| EVENTS : "part of series"
    EVENT_INSTANCES }|..|{ EVENT_TYPES : "with type(s)"
    EVENTS }|..|{ EVENT_TYPES : "with type(s)"
    EVENT_INSTANCES }|--|| ORGS : "belong to"
    EVENT_INSTANCES }|..|| LOCATIONS : "at"
    EVENTS }|--|| ORGS : "belong to"
    EVENTS }|..|| LOCATIONS : "at"
    SLACK_SPACES ||..|| ORGS : "are connected to"
    USERS ||..|{ SLACK_USERS : "have one or more"
    SLACK_USERS }|--|| SLACK_SPACES : "belong to"
    USERS }|..|{ ACHIEVEMENTS : "earn"
    USERS }|..|{ ROLES : "have"
    ROLES ||..|{ PERMISSIONS : "have"
    ROLES }|..|{ ORGS : "in"
    USERS }|..|{ POSITIONS : "hold"
    POSITIONS }|..|{ ORGS : "in"
```