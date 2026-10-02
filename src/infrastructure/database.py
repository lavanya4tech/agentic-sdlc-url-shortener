from dataclasses import dataclass

from datetime import datetime

from typing import Optional

@dataclass

class ShortUrl:

    """

    Domain model representing a shortened URL.

    """

    id: Optional[int]

    original_url: str

    short_code: str

    click_count: int = 0

    created_at: datetime = datetime.utcnow()

    is_active: bool = True

    def record_click(self) -> None:

        self.click_count += 1

    def deactivate(self) -> None:

        self.is_active = False
