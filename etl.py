import zstandard
import io
import csv
from chess import pgn
import time

DATA_PATH = 'raw/lichess_db_standard_rated_2025-12.pgn.zst'
CSV_PATH = 'raw/lichess_db_standard_rated_2025-12-full.csv'

def iter_pgn_games_from_zst(path: str):
    """
    Iterate over PGNs of chess games stored with ZST compression.

    :param path: Path to PGN file to iterate over.
    :return: Generator of PGNs.
    """
    with open(path, 'rb') as f:
        decompression_context = zstandard.ZstdDecompressor()

        with decompression_context.stream_reader(f) as reader:
            text_stream = io.TextIOWrapper(reader, encoding='utf-8', errors='replace', newline='')

            while True:
                game = pgn.read_game(text_stream)

                if game is None:
                    break

                yield game


def safe_cast_to_int(x):
    """
    Cast to int if possible.

    :param x: Value to cast.
    :return: Integer value or None.
    """
    try:
        return int(x)
    except Exception:
        return None


def current_time() -> str:
    hours = time.gmtime(time.time()).tm_hour
    minutes = time.gmtime(time.time()).tm_min
    seconds = time.gmtime(time.time()).tm_sec
    curr_time = f"{hours}:{minutes}:{seconds}"
    return curr_time


fields = [
    "Event", "Site", "UTCDate", "UTCTime", "White", "Black", "Result",
    "WhiteElo", "BlackElo", "TimeControl", "Termination", "PlyCount",
    "MoveCount"
]

with open(CSV_PATH, "w", newline="", encoding="utf-8") as output:
    """
    Write the headers of the chess games into a CSV file.
    """
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()

    print(f"{current_time()}: Beginning to parse PGN headers...")

    for i, game in enumerate(iter_pgn_games_from_zst(DATA_PATH), start=1):
        headers = game.headers

        row = {field: headers.get(field, "") for field in fields}

        row["WhiteElo"] = safe_cast_to_int(row["WhiteElo"])
        row["BlackElo"] = safe_cast_to_int(row["BlackElo"])

        ply = safe_cast_to_int(headers.get("PlyCount"))
        row["PlyCount"] = ply
        if ply is None:
            ply = sum(1 for _ in game.mainline_moves())
            row["PlyCount"] = ply
            row["MoveCount"] = (ply + 1) // 2

        writer.writerow(row)

        if i % 10_000 == 0:
            print(f"{current_time()}: Parsed {i:,} games...")

    print(f"{current_time()}: Finished parsing PGN headers.")