"""
Services package for the application.

To avoid circular imports, import services directly from their respective modules.
For example:
    from .study_buddy import StudyBuddyService
    from .user import UserService
    from .permission import PermissionService
"""

from .exceptions import ResourceNotFoundException, UserPermissionException

__all__ = [
    'ResourceNotFoundException',
    'UserPermissionException'
]

# Note: Other services should be imported directly from their modules
# rather than through this __init__.py to avoid circular dependencies.
# Example:
# from backend.services.user import UserService
# from backend.services.event import EventService
# etc.
