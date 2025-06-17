
# Wit - מערכת ניהול גרסאות (Version Control System)

Wit היא מערכת ניהול גרסאות בסגנון Git, שנועדה לאפשר מעקב אחר קבצים וגרסאות בפרויקטים, כולל תמיכה בפקודות `init`, `add`, `commit`, `log`, `status`, `checkout`, `push`, ואינטגרציה עם CodeGuard להצגת גרפים וסטטיסטיקות על הקומיטים.

---

## 🚀 תכונות עיקריות

- `wit init` — אתחול מאגר (repository) במבנה `.wit` במיקום הנוכחי.
- `wit add <file|folder>` — הוספת קבצים/תיקיות למעקב ב־Wit.
- `wit commit-m-message "<message>"` — שמירת מצב הפרויקט תחת גרסה חדשה.
- `wit log` — תצוגת היסטוריית הקומיטים.
- `wit status` — תצוגה של קבצים שנמצאים במצב Staging.
- `wit check-out <commit_id>` — חזרה לגרסה ספציפית לפי מזהה קומיט.
- `wit push` — שליחת כל הקומיטים שטרם נשלחו לשרת CodeGuard להצגת גרפים וניתוח.

---

## 🧰 מבנה קבצים

```text
project/
│
├── .wit/
│   ├── commit/
│   │   ├── <commit_folder>/
│   ├── stagingArea/
│   └── Issue tracking.json
│
├── your_project_files/
```

---

## 📦 התקנה והרצה

1. ודא ש־Python 3 מותקן אצלך.
2. התקן את התלויות (כגון `click`, `requests`, `matplotlib`, `Pillow`).
3. הרץ את הקובץ הראשי:
```bash
python main.py <command>
```

---

## 📘 דוגמת שימוש

```bash
wit init
wit add my_file.py
wit commit-m-message "first commit"
wit status
wit log
wit push
```

---

## 📡 אינטגרציה עם CodeGuard

בעת הפעלת `wit push`, התיקיות מהקומיטים שטרם נשלחו נדחסות ונשלחות דרך HTTP אל שרת CodeGuard.

- בקשה ל־`/alerts` מחזירה מידע על התראות אבטחה בקוד.
- בקשה ל־`/analyze` מחזירה גרף גרפי (תמונה) המציג מידע על תכולת הקומיטים.

הקוד גם מטפל בתצוגת הגרף באמצעות `matplotlib` ו־`Pillow`.

---

## 🧾 repository_data.json

קובץ זה מכיל את כל המידע על הקומיטים שלך:

```json
{
  "repository_data": [
    {
      "path": "C:\Your\Path\.wit",
      "version_hash_code": "2025-06-17 code-1",
      "commit": {
        "0": {
          "message": "first commit",
          "name": "2025-06-17 code-0",
          "push": true
        },
        ...
      }
    }
  ]
}
```

---

## ❗ חריגות נתמכות

הקוד תומך במערכת חריגות מותאמות אישית:

- `FileExistsError` — כאשר `.wit` כבר קיים.
- `witNotExistsError` — אין תיקיית `.wit` בפרויקט.
- `notValidPathSpec` — נתיב לא חוקי לקובץ/תיקייה.
- `InvalidFileExtension` — קובץ עם סיומת לא תקינה.
- `InvalidCommitId` — מזהה קומיט לא חוקי.

---

## 🧪 בדיקות

תוכל לבדוק את תקינות המערכת על־ידי ביצוע הרצף הבא:

```bash
wit init
wit add test.py
wit commit-m-message "added test.py"
wit log
wit push
```

---

## 📍 יוצרים

פרויקט זה פותח במסגרת פרויקט אישי לניהול גרסאות, בהשראת Git אך בשפה פשוטה וברורה ללמידה והדגמה.
