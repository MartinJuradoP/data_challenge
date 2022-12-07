select department_id, departments, hired
from (select employee.department_id,
             departments,
             count(departments)                                                 as hired,

             (select AVG(hired) as avg
              from (select employee.department_id, departments, count(departments) as hired

                    from hired_employees.hired_employees as employee
                             LEFT JOIN hired_employees.departments as departments
                                       on employee.department_id = departments.id
                    where hired_date > '2020-12-31'
                      and hired_date < '2022-01-01'
                      and departments is not null
                    group by employee.department_id, departments) as query_avg) as const_avr

      from hired_employees.hired_employees as employee
               LEFT JOIN hired_employees.departments as departments
                         on employee.department_id = departments.id
      where hired_date > '2020-12-31'
        and hired_date < '2022-01-01'
        and departments is not null
      group by employee.department_id, departments) as query
where query.hired > query.const_avr
order by query.hired DESC;