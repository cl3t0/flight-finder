from datetime import date, timedelta
from typing import Generator


def date_range(
    start_date: date, end_date: date, step: int = 1
) -> Generator[date, None, None]:
    """
    Generates a range of dates between a start and end date with a specified step size.

    Args:
    - start_date (date): Start of the date range.
    - end_date (date): End of the date range.
    - step (int, optional): Step size for the range, by default 1.

    Yields:
    - date: The next date in the range.

    Example:
    ```
    for date in date_range(date(2023, 2, 1), date(2023, 2, 5)):
        print(date)
    # Output:
    # 2023-02-01
    # 2023-02-02
    # 2023-02-03
    # 2023-02-04
    ```
    """
    for n in range(0, int((end_date - start_date).days), step):
        yield start_date + timedelta(n)
