from flask import Flask, request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def trigger_k8s_cronjob():
    cronjob_name = request.args.get('cronjob')
    namespace = request.args.get('namespace')

    config.load_incluster_config()
    # config.load_kube_config()

    batch_v1_api = client.BatchV1Api()
    try:
        cronjob_instance = batch_v1_api.read_namespaced_cron_job(cronjob_name, namespace, pretty=True)
        job_spec_instance = cronjob_instance.spec.job_template.spec
        
        body = client.V1Job(spec=job_spec_instance, metadata=client.V1ObjectMeta(generate_name=cronjob_name))
        batch_v1_api.create_namespaced_job(namespace, body, pretty=False)
        return "OK", 200
    except ApiException as e:
        print("Exception when calling BatchV1Api: %s\n" % e)
        return "Error", 400


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=True)
