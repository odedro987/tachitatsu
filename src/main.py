import json
import sys
import tachiyomi.core as tachi
import convert.core as convert


if __name__ == "__main__":
    n = len(sys.argv)
    if n < 2:
        print("Not enough arguments")
        exit(1)

    tachiyomi_backup = tachi.TachiyomiBackup(sys.argv[1])
    kotatsu_backup, failed = convert.to_kotatsu_backup(tachiyomi_backup)
    kotatsu_backup.create_backup()
    with open("output/failed.json", encoding="utf-8", mode="w") as f:
        f.write(json.dumps(failed))
