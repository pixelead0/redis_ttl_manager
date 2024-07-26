import click
from redis_ttl_manager import RedisTTLManager


def create_manager(
    pattern: str, expiration_month_min: int, cut_key: int, new_token_expire_minutes: int
) -> RedisTTLManager:
    return RedisTTLManager(
        pattern, expiration_month_min, cut_key, new_token_expire_minutes
    )


@click.command()
@click.option(
    "--pattern", required=True, type=str, help="Pattern to search for in Redis keys."
)
@click.option(
    "--expiration_month_min",
    default=3,
    type=int,
    help="Minimum expiration time in months.",
)
@click.option(
    "--cut_key",
    default=50,
    type=int,
    help="Number of characters to show in the truncated key.",
)
@click.option(
    "--new_token_expire_minutes",
    default=60 * 24 * 365,
    type=int,
    help="New TTL for keys in minutes.",
)
def main(
    pattern: str, expiration_month_min: int, cut_key: int, new_token_expire_minutes: int
) -> None:
    manager = create_manager(
        pattern, expiration_month_min, cut_key, new_token_expire_minutes
    )
    manager.run()


if __name__ == "__main__":
    main()
