import requests
import csv
import io

def decode_secret_message(url: str):
    try:
        # --- START: LIVE FETCH BLOCK ---
        # This is the line that actually fetches the data from the web.
        response = requests.get(url)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        raw_csv_data = response.text
        # --- END: LIVE FETCH BLOCK ---

        # --- SIMULATION DATA (COMMENTED OUT) ---
        # If running in a restricted environment, use this block instead of the one above.
        # raw_csv_data = """Character,X,Y
        # █,0,0
        # ... (rest of the simulation data)
        # """

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return

    csv_stream = io.StringIO(raw_csv_data)
    reader = csv.reader(csv_stream)

    try:
        next(reader)
    except StopIteration:
        return

    char_positions = {}
    max_x, max_y = 0, 0

    for row in reader:
        if len(row) < 3:
            continue

        char = row[0]
        try:
            x = int(row[1].strip())
            y = int(row[2].strip())
        except ValueError:
            continue

        char_positions[(y, x)] = char if char else ' '
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    grid_width = max_x + 1
    grid_height = max_y + 1

    grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]

    for (y, x), char in char_positions.items():
        if 0 <= y < grid_height and 0 <= x < grid_width:
            grid[y][x] = char

    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    # Ensure this URL is configured for CSV export if it's a Google Sheet,
    # or is the direct public URL for the text content.
    live_url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
    decode_secret_message(live_url)