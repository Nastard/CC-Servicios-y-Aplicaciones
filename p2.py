from datetime import timedelta
from textwrap import dedent
from airflow import DAG # The DAG object; we'll need this to instantiate a DAG
from airflow.operators.bash import BashOperator # Operators; we need this to operate!
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'David Sanchez',
    'depends_on_past': False,
    'email': ['davidsm93@correo.ugr.es'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
with DAG(
    'Practica_2_CC',
    default_args=default_args,
    description='Despliegue de un servicio Cloud Native',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2), # Hace 2 dias empezo, siempre se ejecuta
    tags=['practica'],
) as dag:

	preparar_entorno = BashOperator(
		task_id='crear_carpeta_temporal',
		bash_command='[ -d /tmp/workflow ] || mkdir -p /tmp/workflow/arima_model; mkdir -p /tmp/workflow/ar_model; mkdir -p /tmp/workflow/appv1; mkdir -p /tmp/workflow/appv2',
	)
	descargar_temp = BashOperator(
		task_id='descargar_temperatura',
		bash_command='wget -O /tmp/workflow/temperature.zip https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',
	)
	descargar_hum = BashOperator(
		task_id='descargar_humedad',
		bash_command='wget -O /tmp/workflow/humidity.zip https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',
	)
	descomprimir= BashOperator(
		task_id='descomprimir_zips',
		bash_command='unzip -o \'/tmp/workflow/*.zip\' -d /tmp/workflow/',
	)
	temperatura_san_francisco= BashOperator(
		task_id='temperatura_san_francisco',
		bash_command='cut -d, -f1,4 /tmp/workflow/temperature.csv > /tmp/workflow/temp_SF.csv',
	)
	humedad_san_francisco= BashOperator(
		task_id='humedad_san_francisco',
		bash_command='cut -d, -f1,4 /tmp/workflow/humidity.csv > /tmp/workflow/hum_SF.csv',
	)
	unir_temp_hum= BashOperator(
		task_id='unir_temperatura_humedad',
		bash_command='join -t, /tmp/workflow/temp_SF.csv /tmp/workflow/hum_SF.csv > /tmp/workflow/SF.csv',
	)
	eliminar_vacios= BashOperator(
		task_id='eliminar_campos_vacios',
		bash_command='sed \'/,$/d\' /tmp/workflow/SF.csv > /tmp/workflow/SF_clean.csv',
	)
	coger_muestra= BashOperator(
		task_id='coger_muestra',
		bash_command='sed -e \'1d;2001q\' /tmp/workflow/SF_clean.csv > /tmp/workflow/SF_sample.csv',
	)
	descargar_mongo= BashOperator(
		task_id='descargar_contenedor_mongo',
		bash_command='docker pull mongo',
	)
	iniciar_mongo= BashOperator(
		task_id='iniciar_contenedor_mongo',
		bash_command='docker run -p 27017:27017 -d --name mongop2 mongo --noauth --bind_ip=0.0.0.0',
	)
	copiar_csv= BashOperator(
		task_id='copiar_csv_a_mongo',
		bash_command='docker cp /tmp/workflow/SF_sample.csv mongop2:/SF_sample.csv',
	)
	guardar_datos= BashOperator(
		task_id='guardar_csv_en_mongo',
		bash_command='docker exec -it mongop2 mongoimport --type csv -d practica2 -c san_francisco -f fecha,temperatura,humedad --file /SF_sample.csv',
	)
	descargar_arima = BashOperator(
		task_id='descargar_modelo_arima',
		bash_command='wget -O /tmp/workflow/arima_model/arima.py https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/arima_model/arima.py; wget -O /tmp/workflow/arima_model/Dockerfile https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/arima_model/Dockerfile; wget -O /tmp/workflow/arima_model/requirements.txt https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/arima_model/requirements.txt',
	)
	descargar_ar = BashOperator(
		task_id='descargar_modelo_ar',
		bash_command='wget -O /tmp/workflow/ar_model/ar.py https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/ar_model/ar.py; wget -O /tmp/workflow/ar_model/Dockerfile https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/ar_model/Dockerfile; wget -O /tmp/workflow/ar_model/requirements.txt https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/ar_model/requirements.txt',
	)
	iniciar_arima= BashOperator(
		task_id='iniciar_contenedor_arima',
		bash_command='docker build -t arima /tmp/workflow/arima_model/',
	)
	iniciar_ar= BashOperator(
		task_id='iniciar_contenedor_ar',
		bash_command='docker build -t ar /tmp/workflow/ar_model/',
	)
	ejecutar_arima= BashOperator(
		task_id='ejecutar_contenedor_arima',
		bash_command='docker run -it --rm --net=host --name model_arima arima',
	)
	ejecutar_ar= BashOperator(
		task_id='ejecutar_contenedor_ar',
		bash_command='docker run -it --rm --net=host --name model_ar ar',
	)
	descargar_appv1 = BashOperator(
		task_id='descargar_appv1',
		bash_command='wget -O /tmp/workflow/appv1/app.py https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv1/app.py; wget -O /tmp/workflow/appv1/test.py https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv1/test.py; wget -O /tmp/workflow/appv1/Dockerfile https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv1/Dockerfile; wget -O /tmp/workflow/appv1/requirements.txt https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv1/requirements.txt',
	)
	descargar_appv2 = BashOperator(
		task_id='descargar_appv2',
		bash_command='wget -O /tmp/workflow/appv2/app.py https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv2/app.py; wget -O /tmp/workflow/appv2/test.py https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv2/test.py; wget -O /tmp/workflow/appv2/Dockerfile https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv2/Dockerfile; wget -O /tmp/workflow/appv2/requirements.txt https://raw.githubusercontent.com/Nastard/CC-Servicios-y-Aplicaciones/main/appv2/requirements.txt',
	)
	iniciar_appv1= BashOperator(
		task_id='iniciar_contenedor_appv1',
		bash_command='docker build -t appv1 /tmp/workflow/appv1/',
	)
	iniciar_appv2= BashOperator(
		task_id='iniciar_contenedor_appv2',
		bash_command='docker build -t appv2 /tmp/workflow/appv2/',
	)
	test_appv1= BashOperator(
		task_id='testear_appv1',
		bash_command='docker run -it --rm --net=host --name flask_ppv1 appv1 python3 test.py',
	)
	test_appv2= BashOperator(
		task_id='testear_appv2',
		bash_command='docker run -it --rm --net=host --name flask_ppv2 appv2 python3 test.py',
	)
	desplegar_appv1= BashOperator(
		task_id='desplegar_appv1',
		bash_command='docker run -d -it --rm --net=host --name flask_appv1 appv1',
	)
	desplegar_appv2= BashOperator(
		task_id='desplegar_appv2',
		bash_command='docker run -d -it --rm --net=host --name flask_appv2 appv2',
	)

	preparar_entorno >> [descargar_temp, descargar_hum] >> descomprimir >> [temperatura_san_francisco, humedad_san_francisco] >> unir_temp_hum >> eliminar_vacios >> coger_muestra
	preparar_entorno >> [descargar_arima, descargar_ar]
	preparar_entorno >> [descargar_appv1, descargar_appv2]
	descargar_mongo >> iniciar_mongo
	[coger_muestra, iniciar_mongo] >> copiar_csv >> guardar_datos
	[descargar_arima, guardar_datos] >> iniciar_arima >> ejecutar_arima
	[descargar_ar, guardar_datos] >> iniciar_ar >> ejecutar_ar
	[ejecutar_arima, descargar_appv1] >> iniciar_appv1 >> test_appv1 >> desplegar_appv1
	[ejecutar_ar, descargar_appv2] >> iniciar_appv2 >> test_appv2 >> desplegar_appv2
