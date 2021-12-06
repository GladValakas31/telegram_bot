import os
import shutil
from config import TEACHER_GIT

def check_student_program(git: str):

    """
    Функция, осуществляющая клонирование репозитория ученика и учителя в одну папку;
    проверяет программу, сделанную учеником через unittest преподавателя.
    Возвращает True, если его программа сделана правильно, False, если неправильно.
    """

    git_student = git
    git_teacher = TEACHER_GIT

    start_dir = os.getcwd()
    try:
        os.chdir('..')
        dir = os.path.join(os.getcwd(), 'TestingStudentProgram')
        os.mkdir('TestingStudentProgram')
        os.mkdir(dir)
    except FileExistsError:
        os.system(f'rd /s /q "{dir}"')
        os.mkdir(dir)

    os.chdir(dir)
    os.system(f'git clone {git_student}')
    student_dir = os.listdir(os.getcwd())[0]
    os.system(f'git clone {git_teacher}')
    for direct in os.listdir(os.getcwd()):
        if direct != student_dir:
            teacher_dir = direct
    way_student = os.path.join(dir, student_dir)
    way_teacher = os.path.join(dir, teacher_dir)
    os.chdir(way_student)
    for file in os.listdir(way_student):
        if '.git' in file or 'README.md' in file:
            continue
        way_student_program = os.path.join(way_student, file)
    os.system(f'rd /s /q "{way_teacher}"\\README.md')
    shutil.move(way_student_program, way_teacher)
    os.chdir(way_teacher)
    finish_test_calc = os.system('python -m unittest main_test.TestCalc.test_calc')
    finish_test_values = os.system('python -m unittest main_test.TestCalc.test_values')
    os.chdir(start_dir)
    if finish_test_values == finish_test_calc == 0:
        return True
    return False
