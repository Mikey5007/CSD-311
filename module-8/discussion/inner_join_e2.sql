SELECT 
    s.employee_id,
    s.first_name,
    s.last_name,
    s.occupation,
    s.salary,
    p.department_name
FROM employee_salary s
INNER JOIN parks_departments p
    ON s.dept_id = p.department_id;
