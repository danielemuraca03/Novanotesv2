"""
NovaNotes — Demo data populator.

"""

import os
import random
import bcrypt
import db

DEMO_FILES_DIR = os.path.join(os.path.dirname(__file__), "static", "demo_files")


DEMO_USERS = [
    ("maria.silva@novasbe.pt",     "Maria Silva"),
    ("joao.santos@novasbe.pt",     "João Santos"),
    ("ana.costa@novasbe.pt",       "Ana Costa"),
    ("pedro.ferreira@novasbe.pt",  "Pedro Ferreira"),
    ("beatriz.oliveira@novasbe.pt","Beatriz Oliveira"),
    ("tiago.martins@novasbe.pt",   "Tiago Martins"),
    ("carolina.pereira@novasbe.pt","Carolina Pereira"),
    ("diogo.rodrigues@novasbe.pt", "Diogo Rodrigues"),
    ("ines.sousa@novasbe.pt",      "Inês Sousa"),
    ("rafael.almeida@novasbe.pt",  "Rafael Almeida"),
    ("mariana.carvalho@novasbe.pt","Mariana Carvalho"),
    ("miguel.lopes@novasbe.pt",    "Miguel Lopes"),
]

COURSES = [
    ("Microeconomics I",     "Prof. Santos"),
    ("Microeconomics II",    "Prof. Santos"),
    ("Macroeconomics I",     "Prof. Mendes"),
    ("Statistics",           "Prof. Ferreira"),
    ("Econometrics",         "Prof. Ferreira"),
    ("Financial Accounting", "Prof. Costa"),
    ("Managerial Accounting","Prof. Costa"),
    ("Marketing",            "Prof. Oliveira"),
    ("Corporate Finance",    "Prof. Rodrigues"),
    ("Investments",          "Prof. Rodrigues"),
    ("Strategy",             "Prof. Pereira"),
    ("Operations Management","Prof. Martins"),
]

NOTE_TEMPLATES = [
    ("{course} — Midterm Summary",     "Comprehensive summary of the first half of the semester. Covers all key concepts, formulas, and worked examples from lectures."),
    ("{course} — Final Cheat Sheet",   "Condensed one-pager for the final exam. All the must-know formulas and definitions in a single reference."),
    ("{course} — Full Lecture Notes",  "Detailed notes from every lecture this semester. Includes diagrams, examples, and side annotations from the practical sessions."),
    ("{course} — Past Exam Solutions", "Worked solutions for the last three years of final exams. Step-by-step explanations for the trickier problems."),
    ("{course} — Practice Problems",   "Curated practice set with solutions. Good for self-testing the week before the exam."),
    ("{course} — Key Concepts Recap",  "Short, high-level recap of the chapters the professor flagged as most likely to appear on the exam."),
]

REVIEW_TEMPLATES = [
    "Solid course. The professor explains concepts clearly and the practical sessions really help. Workload is fair if you keep up weekly.",
    "Tough course but rewarding. Don't underestimate the problem sets — they take more time than expected.",
    "Great professor, very approachable during office hours. Slides could be a bit more detailed but lectures fill the gap.",
    "Honestly one of my favourite courses so far. Practical examples make abstract ideas click.",
    "Heavy reading load. Make sure to attend lectures — the textbook alone isn't enough.",
    "Well-structured course. Midterm was fair, final was a bit harder than past papers suggested.",
    "Professor is enthusiastic and clearly passionate about the subject. Grading is strict but consistent.",
    "Good intro to the topic. Could use more case studies but overall a positive experience.",
    "Challenging but fair. Group project was the highlight — really applied what we learned in class.",
    "Lectures are dense, so review weekly or you'll fall behind. Worth the effort though.",
    "Excellent prof. Exams emphasize understanding over memorization, which I appreciated.",
    "Decent course but the textbook is essential. Don't skip the recommended exercises.",
]

SEMESTERS = ["Fall 2024", "Spring 2025", "Fall 2025"]


def _demo_content_exists(user_ids):
    """True if any demo user already owns notes — used to skip the content phase on re-run."""
    return any(db.get_notes_by_user(uid) for uid in user_ids)


def _available_demo_pdfs():
    """Relative paths (from app root) to PDFs bundled in static/demo_files/."""
    if not os.path.isdir(DEMO_FILES_DIR):
        return []
    return sorted(
        os.path.join("static", "demo_files", f)
        for f in os.listdir(DEMO_FILES_DIR)
        if f.lower().endswith(".pdf")
    )


def populate():
    print("Upserting demo users...")
    pw_hash = bcrypt.hashpw(b"demo1234", bcrypt.gensalt()).decode()
    user_ids = []
    for email, name in DEMO_USERS:
        existing = db.get_user_by_email(email)
        if existing:
            user_ids.append(existing["id"])
            continue
        uid = db.create_user(
            email=email,
            username=name,
            password_hash=pw_hash,
            initial_points=random.randint(20, 250),
        )
        user_ids.append(uid)
    print(f"  {len(user_ids)} users ready.")

    if _demo_content_exists(user_ids):
        print("Demo notes/ratings/reviews already exist. Skipping content phase.")
        return

    demo_pdfs = _available_demo_pdfs()
    if not demo_pdfs:
        print(f"No PDFs found in {DEMO_FILES_DIR}.")
        print("Drop at least one .pdf there so demo downloads work in production, then re-run.")
        return
    print(f"Using {len(demo_pdfs)} bundled PDF(s) for demo notes.")

    print("Creating notes...")
    note_ids = []
    for _ in range(7):
        course, prof = random.choice(COURSES)
        title_tpl, desc = random.choice(NOTE_TEMPLATES)
        nid = db.save_note(
            user_id=random.choice(user_ids),
            title=title_tpl.format(course=course),
            course=course,
            professor=prof,
            year=random.choice([2023, 2024, 2025]),
            description=desc,
            file_path=random.choice(demo_pdfs),
            file_type="pdf",
        )
        note_ids.append(nid)
    print(f"  {len(note_ids)} notes created.")

    print("Creating ratings...")
    rating_count = 0
    for _ in range(10):
        try:
            db.add_rating(
                user_id=random.choice(user_ids),
                note_id=random.choice(note_ids),
                stars=random.choices([3, 4, 5], weights=[1, 3, 4])[0],
            )
            rating_count += 1
        except Exception:
            pass
    print(f"  {rating_count} ratings inserted (duplicates upsert).")

    print("Creating reviews...")
    for _ in range(6):
        course, prof = random.choice(COURSES)
        db.create_review(
            user_id=random.choice(user_ids),
            course=course,
            professor=prof,
            semester=random.choice(SEMESTERS),
            text=random.choice(REVIEW_TEMPLATES),
            stars=random.choices([3, 4, 5], weights=[1, 3, 4])[0],
        )
    print("  6 reviews created.")

    print("\nDone. Refresh the Streamlit app to see the populated demo.")


if __name__ == "__main__":
    populate()
