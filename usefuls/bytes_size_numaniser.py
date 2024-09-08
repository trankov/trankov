def humanize_bytes_size(bytes_size: int) -> str:
    return next(
        (
            f"{round(j, 2)} {['bytes', 'KB', 'MB', 'GB', 'TB'][enmrt]}"
            for enmrt, j in enumerate(
                bytes_size / pow(1024, i) for i in range(6, 0, -1)
            )
            if j > 1
        ),
        'Nothing',
    )
