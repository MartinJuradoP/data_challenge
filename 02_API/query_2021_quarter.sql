select departments, job, sum (case quarter when 'Q1'then 1 else 0 end) as Q1, sum (case quarter when 'Q2'then 1 else 0 end) as Q2,
sum (case quarter when 'Q3'then 1 else 0 end) as Q3, sum (case quarter when 'Q4'then 1 else 0 end) as Q4
       from (select departments, job ,'Q1' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date > '2020-12-31'
              and hired_date < '2021-04-01' and departments is not null and job is not null

            union all

            select departments, job ,'Q2' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date >= '2021-04-01'
              and hired_date < '2021-07-01' and departments is not null and job is not null
            union all

            select departments, job ,'Q3' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date >= '2021-07-01'
              and hired_date < '2021-10-01' and departments is not null and job is not null
            union all

            select departments, job ,'Q4' as quarter
            from hired_employees.hired_employees as employee
                     LEFT JOIN hired_employees.departments as departments
                               on employee.department_id = departments.id
                     LEFT JOIN hired_employees.jobs job on employee.job_id = job.id
            where hired_date >= '2021-10-01'
              and hired_date < '2022-01-01' and departments is not null and job is not null
            ) as quarter group by departments, job order by departments ASC, job;