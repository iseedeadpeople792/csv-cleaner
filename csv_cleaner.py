"""Чистит CSV с контактами: обрезает пробелы, приводит телефоны к +7XXXXXXXXXX,
email к нижнему регистру, убирает дубли. Плохие строки пишет в отдельный файл.
Запуск: python csv_cleaner.py contacts.csv clean.csv rejected.csv
Ожидаемые колонки: name, phone, email
"""
import csv
import re
import sys

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def norm_phone(raw):
    """Российский номер -> +7XXXXXXXXXX или None."""
    d = re.sub(r"\D", "", raw or "")
    if len(d) == 11 and d[0] in "78":
        d = d[1:]
    return "+7" + d if len(d) == 10 else None


def clean(rows):
    """Возвращает (чистые, отклонённые). Дубль = тот же email или телефон."""
    good, bad, seen = [], [], set()
    for r in rows:
        name = (r.get("name") or "").strip()
        phone = norm_phone(r.get("phone"))
        email = (r.get("email") or "").strip().lower()
        if not name or not phone or not EMAIL.match(email):
            bad.append(r)
            continue
        if email in seen or phone in seen:
            bad.append(r)
            continue
        seen.update((email, phone))
        good.append({"name": name, "phone": phone, "email": email})
    return good, bad


def main(src, dst, rej):
    with open(src, encoding="utf-8", newline="") as f:
        good, bad = clean(list(csv.DictReader(f)))
    for path, data, cols in ((dst, good, ["name", "phone", "email"]), (rej, bad, ["name", "phone", "email"])):
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(data)
    print(f"Чистых: {len(good)}, отклонено: {len(bad)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
