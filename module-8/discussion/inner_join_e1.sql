SELECT 
    d.employee_id,
    d.first_name,
    d.last_name,
    d.age,
    s.occupation,
    s.salary
FROM employee_demographics d
INNER JOIN employee_salary s
    ON d.employee_id = s.employee_id;
