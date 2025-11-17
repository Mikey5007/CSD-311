SELECT dept_id, COUNT(*) AS employee_count
FROM employee_salary
GROUP BY dept_id;
