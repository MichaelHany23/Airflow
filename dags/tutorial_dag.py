import textwrap
from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    "tutorial",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    # Task 1 — Print date
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    # Task 2 — Sleep
    t2 = BashOperator(
        task_id="sleep",
        bash_command="sleep 5",
        retries=3,
    )

    # Task 3 — Templated
    templated_command = textwrap.dedent(
        """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id="templated",
        bash_command=templated_command,
    )

    t1 >> [t2, t3]
