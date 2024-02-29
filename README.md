# Tachitatsu

A tool for converting [Tachiyomi](https://tachiyomi.org/) backups into [Kotatsu](https://github.com/KotatsuApp/Kotatsu) backups.

## Requirements

1. Install the relevant modules from the requirements file by running `pip install -r requirements.txt`.
2. Tachiyomi backup (`.tachibk` or `.proto.gz`)

## Usage

Copy your Tachiyomi backup to the folder where you cloned this repo.

Run `python src/main.py <backup)file_name>`.

This should generate an `output` folder with a `.bk` Kotatsu backup file. Copy the file to your desired device and import it from the Kotatsu app.

## Notes

Kotatsu transforms different sources' urls differently. This means each source needs to be supported individually. This tool currently explicitly supports `Mangadex` and `Mangakakalot`. Some other sources may be supported out of the box but I cannot guarantee it.

Feel free to create PRs for other sources if you want to contribute.

This is mainly a pet project, I'm no Python dev so I apologize in advance for the code.
