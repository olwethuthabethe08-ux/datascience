grades.py


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db_session
from typing import List

router = APIRouter(prefix="/grades", tags=["grades"])

@router.post("/", response_model=schemas.GradeRead, status_code=status.HTTP_201_CREATED)
def create_grade_endpoint(grade_in: schemas.GradeCreate, db: Session = Depends(get_db_session)):
    try:
        grade = crud.create_grade(db, grade_in)
        return grade
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{grade_id}", response_model=schemas.GradeRead)
def get_grade_endpoint(grade_id: int, db: Session = Depends(get_db_session)):
    grade = crud.get_grade(db, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade

@router.get("/", response_model=List[schemas.GradeRead])
def list_grades_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    return crud.list_grades(db, skip=skip, limit=limit)

@router.patch("/{grade_id}", response_model=schemas.GradeRead)
def update_grade_endpoint(grade_id: int, grade_upd: schemas.GradeUpdate, db: Session = Depends(get_db_session)):
    try:
        grade = crud.update_grade(db, grade_id, grade_upd)
        return grade
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade_endpoint(grade_id: int, db: Session = Depends(get_db_session)):
    try:
        crud.delete_grade(db, grade_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None

# reports
@router.get("/reports/student/{student_id}", response_model=schemas.StudentGradesReport)
def student_report_endpoint(student_id: int, db: Session = Depends(get_db_session)):
    student, grades, gpa = crud.student_grades_report(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student": student, "grades": grades, "gpa": gpa}

@router.get("/reports/course/{course_id}", response_model=schemas.CourseGradesReport)
def course_report_endpoint(course_id: int, db: Session = Depends(get_db_session)):
    course, grades, avg = crud.course_grades_report(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"course": course, "grades": grades, "average_score": avg}
