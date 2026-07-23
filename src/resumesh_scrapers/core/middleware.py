import logging
from typing import Callable, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from resumesh_scrapers.exceptions import NetworkError, RateLimitError

logger = logging.getLogger(__name__)


def create_retry_decorator(
    max_attempts: int = 3, min_wait: float = 2.0, max_wait: float = 10.0
) -> Callable:
    """
    Geçici ağ hatalarında veya rate-limit durumlarında kullanılmak üzere
    üstel artan bekleme (exponential backoff) süreli bir retry decorator üretir.
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type((NetworkError, RateLimitError)),
        before_sleep=lambda retry_state: logger.warning(
            f"İşlem başarısız oldu. {retry_state.next_action.sleep} saniye sonra "
            f"yeniden deneniyor... (Deneme: {retry_state.attempt_number}/{max_attempts})"
        ),
        reraise=True,
    )


class RequestMiddleware:
    """
    Scraper isteklerini sarmalayan, loglama ve hata yakalama süreçlerini
    merkezi hale getiren middleware sınıfı.
    """

    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.retry_decorator = create_retry_decorator(max_attempts=max_attempts)

    def execute_with_retry(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Verilen fonksiyonu retry politikası ile sarmalayarak çalıştırır.
        """
        wrapped_func = self.retry_decorator(func)
        try:
            return wrapped_func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"İstek maksimum deneme sınırına ulaştı ve başarısız oldu: {e}"
            )
            raise
