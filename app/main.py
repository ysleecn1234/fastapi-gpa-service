from fastapi import FastAPI, HTTPException
from app.models import Student, StudentSummary
from fastapi.responses import JSONResponse

app = FastAPI()  

grade_to_score = {
    "A+": 4.5, "A": 4.0, "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0,
}

@app.post("/score")
def calculate_gpa(student: Student):
    total_score = 0.0
    total_credits = 0

    for course in student.courses:
        score = grade_to_score.get(course.grade)
        if score is None:
            raise HTTPException(status_code=400, detail=f"Invalid grade: {course.grade}")
        total_score += score * course.credits
        total_credits += course.credits

    if total_credits == 0:
        raise HTTPException(status_code=400, detail="No valid credits provided")

    gpa = round(total_score / total_credits + 1e-8, 2)
    result = {
        "student_summary": StudentSummary(
            student_id=student.student_id,
            name=student.name,
            gpa=gpa,
            total_credits=total_credits
        )
    }
    return JSONResponse(content={"student_summary": result["student_summary"].dict()})