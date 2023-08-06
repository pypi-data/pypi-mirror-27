#-*- coding: utf-8 -*-

__version__ = "1.4.35"

import six
import warnings
import requests
import fire
import tarfile
import os
import sys
import kubernetes.client as kubeclient
from kubernetes.client.rest import ApiException
import kubernetes.config as kubeconfig
import yaml
import json
from pprint import pprint
import subprocess
from datetime import timedelta
import jinja2
import boto3


if sys.version_info.major == 3:
    from urllib3 import disable_warnings
    disable_warnings()

class PipelineCli(object):

    # Deprecated
    _kube_deploy_registry = {'jupyter': (['jupyterhub-deploy.yaml'], []),
                            'jupyterhub': (['jupyterhub-deploy.yaml'], []),
                            'spark': (['spark-master-deploy.yaml'], ['spark-worker', 'metastore']),
                            'spark-worker': (['spark-worker-deploy.yaml'], []),
                            'metastore': (['metastore-deploy.yaml'], ['mysql']),
                            'hdfs': (['namenode-deploy.yaml'], []),
                            'redis': (['redis-master-deploy.yaml'], []),
                            'presto': (['presto-master-deploy.yaml',
                                        'presto-worker-deploy.yaml'], ['metastore']),
                            'presto-ui': (['presto-ui-deploy.yaml'], ['presto']),
                            'airflow': (['airflow-deploy.yaml'], ['mysql', 'redis']),
                            'mysql': (['mysql-master-deploy.yaml'], []),
                            #'web-home': (['web/home-deploy.yaml'], []),
                            'zeppelin': (['zeppelin-deploy.yaml'], []),
                            #'zookeeper': (['zookeeper-deploy.yaml'], []),
                            'elasticsearch': (['elasticsearch-2-3-0-deploy.yaml'], []),
                            'kibana': (['kibana-4-5-0-deploy.yaml'], ['elasticsearch'], []), 
                            #'kafka': (['stream/kafka-0.11-deploy.yaml'], ['zookeeper']),
                            'cassandra': (['cassandra-deploy.yaml'], []),
                            'jenkins': (['jenkins-deploy.yaml'], []),
                            #'turbine': (['dashboard/turbine-deploy.yaml'], []),
                            #'hystrix': (['dashboard/hystrix-deploy.yaml'], []),
                           }

    # Deprecated
    _kube_svc_registry = {'jupyter': (['jupyterhub-svc.yaml'], []),
                         'jupyterhub': (['jupyterhub-svc.yaml'], []),
                         'spark': (['spark-master-svc.yaml'], ['spark-worker', 'metastore']), 
                         'spark-worker': (['spark-worker-svc.yaml'], []),
                         'metastore': (['metastore-svc.yaml'], ['mysql']),
                         'hdfs': (['namenode-svc.yaml'], []),
                         'redis': (['redis-master-svc.yaml'], []),
                         'presto': (['presto-master-svc.yaml',
                                     'presto-worker-svc.yaml'], ['metastore']),
                         'presto-ui': (['presto-ui-svc.yaml'], ['presto']),
                         'airflow': (['airflow-svc.yaml'], ['mysql', 'redis']),
                         'mysql': (['mysql-master-svc.yaml'], []),
                         #'web-home': (['web/home-svc.yaml'], []),
                         'zeppelin': (['zeppelin-svc.yaml'], []),
                         #'zookeeper': (['zookeeper/zookeeper-svc.yaml'], []),
                         'elasticsearch': (['elasticsearch-2-3-0-svc.yaml'], []),
                         'kibana': (['kibana-4-5-0-svc.yaml'], ['elasticsearch'], []),
                         #'kafka': (['stream/kafka-0.11-svc.yaml'], ['zookeeper']),
                         'cassandra': (['cassandra-svc.yaml'], []),
                         #'jenkins': (['jenkins-svc.yaml'], []),
                         #'turbine': (['dashboard/turbine-svc.yaml'], []),
                         #'hystrix': (['dashboard/hystrix-svc.yaml'], []),
                        }

    _Dockerfile_template_registry = {
                                     'predict-server': (['predict-server-local-dockerfile.template'], []),
                                     'train-server': (['train-server-local-dockerfile.template'], []),
                                    }
    _kube_router_deploy_template_registry = {'predict-router-split': (['predict-router-split-deploy.yaml.template'], [])}
    _kube_router_ingress_template_registry = {'predict-router-split': (['predict-router-split-ingress.yaml.template'], [])}
    _kube_router_svc_template_registry = {'predict-router-split': (['predict-router-split-svc.yaml.template'], [])}
    _kube_router_routerules_template_registry = {'predict-router-split': (['predict-router-split-routerules.yaml.template'], [])}
    _kube_router_autoscale_template_registry = {'predict-router-split': (['predict-router-split-autoscale.yaml.template'], [])}

    _kube_cluster_autoscale_template_registry = {'predict-cluster': (['predict-cluster-autoscale.yaml.template'], [])}
    _kube_cluster_deploy_template_registry = {'predict-cluster': (['predict-cluster-deploy.yaml.template'], [])}
    _kube_cluster_svc_template_registry = {'predict-cluster': (['predict-cluster-svc.yaml.template'], [])}

    _train_kube_template_registry = {
                                             'train-cluster': (['train-cluster.yaml.template'], []),
                                            }
    _pipeline_api_version = 'v1'
    _default_pipeline_templates_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'templates'))
    _default_pipeline_services_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'services'))
    _default_image_registry_url = 'docker.io'
    _default_image_registry_repo = 'pipelineai'
    _default_image_registry_train_namespace = 'train'
    _default_image_registry_predict_namespace = 'predict' 
    _default_image_registry_base_tag = '1.4.0'
    _default_model_chip = 'cpu'
    _default_build_type = 'docker'
    _default_build_context_path = '.'
    _default_cluster_namespace = 'default'
 
    def version(self):
        print('')
        print('cli_version: %s' % __version__)
        print('api_version: %s' % PipelineCli._pipeline_api_version)
        print('')
        print('default build type: %s' % PipelineCli._default_build_type)

        build_context_path = os.path.expandvars(PipelineCli._default_build_context_path)
        build_context_path = os.path.expanduser(build_context_path)
        build_context_path = os.path.abspath(build_context_path)
        build_context_path = os.path.normpath(build_context_path)

        print('default build context path: %s => %s' % (PipelineCli._default_build_context_path, build_context_path))
        print('')
        print('default train base image: %s/%s/%s-%s:%s' % (PipelineCli._default_image_registry_url, PipelineCli._default_image_registry_repo, PipelineCli._default_image_registry_train_namespace, PipelineCli._default_model_chip, PipelineCli._default_image_registry_base_tag))
        print('default predict base image: %s/%s/%s-%s:%s' % (PipelineCli._default_image_registry_url, PipelineCli._default_image_registry_repo, PipelineCli._default_image_registry_predict_namespace, PipelineCli._default_model_chip, PipelineCli._default_image_registry_base_tag))
        print('')
        print('capabilities enabled: %s' % ['train-server', 'train-kube', 'train-sage', 'predict-server', 'predict-kube', 'predict-sage'])
        print('capabilities available: %s' % ['optimize', 'jupyter', 'spark', 'airflow', 'kafka'])
        print('')
        print('Email upgrade@pipeline.ai to enable additional capabilities.')
        print('')


    def _templates_path(self):
        print("")
        print("templates path: %s" % PipelineCli._default_pipeline_templates_path)
        print("")


    def _get_default_model_runtime(self,
                                   model_type):
        model_runtime = 'python'

        if model_type in ['keras', 'python', 'scikit']:
           model_runtime = 'python'
         
        if model_type in ['java', 'pmml', 'spark', 'xgboost']:
           model_runtime = 'jvm'

        if model_type in ['tensorflow']:
           model_runtime = 'tfserving'

        return model_runtime


    def _validate_and_prep_model_tag(self,
                                    model_tag):
        model_tag = str(model_tag)
        model_tag = model_tag.lower()
        return model_tag


    def _validate_and_prep_model_weight_list(self,
                                            model_weight_list):
        model_weight_total = 0
        for idx in range(len(model_weight_list)):
            model_weight = int(model_weight_list[idx])
            model_weight_total += model_weight

        if model_weight_total != 100:
            raise ValueError("Total of '%s' for weights '%s' does not equal 100 as expected." % (model_weight_total, model_weight_list))
            
        return 


    def predict_kube_connect(self,
                                model_name,
                                model_tag,
                                model_type,
                                model_runtime=None,
                                model_chip=None,
                                local_port=None,
                                service_port=None,
                                cluster_namespace=None,
                                image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)
 
        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_connect(service_name=service_name,
                              cluster_namespace=cluster_namespace,
                              local_port=local_port,
                              service_port=service_port)


    def _service_connect(self,
                         service_name,
                         cluster_namespace=None,
                         local_port=None,
                         service_port=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        pod = self._get_pod_by_service_name(service_name=service_name)
        if not pod:
            print("")
            print("Service '%s' is not running." % service_name)
            print("")
            return
        if not service_port:
            svc = self._get_svc_by_service_name(service_name=service_name)
            if not svc:
                print("")
                print("Service '%s' proxy port cannot be found." % service_name)
                print("")
                return
            service_port = svc.spec.ports[0].target_port

        if not local_port:
            print("")
            print("Proxying local port '<randomly-chosen>' to app '%s' port '%s' using pod '%s'." % (service_port, service_name, pod.metadata.name))
            print("")
            print("Use 'http://127.0.0.1:<randomly-chosen>' to access app '%s' on port '%s'." % (service_name, service_port))
            print("")
            print("If you break out of this terminal, your proxy session will end.")
            print("")
            cmd = 'kubectl port-forward %s :%s' % (pod.metadata.name, service_port)
            print("Running command...")
            print(cmd)
            print("")
            subprocess.call(cmd, shell=True)
            print("")
        else:
            print("")
            print("Proxying local port '%s' to app '%s' port '%s' using pod '%s'." % (local_port, service_port, service_name, pod.metadata.name))
            print("")
            print("Use 'http://127.0.0.1:%s' to access app '%s' on port '%s'." % (local_port, service_name, service_port))
            print("")
            print("If you break out of this terminal, your proxy session will end.")
            print("")
            subprocess.call('kubectl port-forward %s %s:%s' % (pod.metadata.name, local_port, service_port), shell=True)
            print("")


    def _environment_resources(self):
        subprocess.call("kubectl top node", shell=True)

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                              pretty=True)
            deployments = response.items
            for deployment in deployments:
                self._service_resources(deployment.metadata.name)


    def _service_resources(self,
                           service_name):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                                 pretty=True)
            pods = response.items
            for pod in pods: 
                if (service_name in pod.metadata.name):
                    subprocess.call('kubectl top pod %s' % pod.metadata.name, shell=True)
        print("")


    def _create_predict_server_Dockerfile(self,
                                          model_name,
                                          model_tag,
                                          model_type,
                                          model_runtime,
                                          model_chip,
                                          model_path,
                                          input_stream_url,
                                          input_stream_topic,
                                          output_stream_url,
                                          output_stream_topic,
                                          image_registry_url,
                                          image_registry_repo,
                                          image_registry_namespace,
                                          image_registry_base_tag,
                                          image_registry_base_chip,
                                          pipeline_templates_path,
                                          build_context_path):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        context = {
                   'PIPELINE_MODEL_NAME': model_name,
                   'PIPELINE_MODEL_TAG': model_tag,
                   'PIPELINE_MODEL_TYPE': model_type,
                   'PIPELINE_MODEL_RUNTIME': model_runtime,
                   'PIPELINE_MODEL_CHIP': model_chip,
                   'PIPELINE_MODEL_PATH': model_path,
                   'PIPELINE_INPUT_STREAM_URL': input_stream_url,
                   'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
                   'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
                   'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
                   'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
                   'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
                   'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
                   'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag
                  }

        model_predict_cpu_Dockerfile_templates_path = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._Dockerfile_template_registry['predict-server'][0][0]))
        path, filename = os.path.split(model_predict_cpu_Dockerfile_templates_path)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_Dockerfile = os.path.normpath('%s/.pipeline-generated-%s-%s-%s-Dockerfile' % (build_context_path, image_registry_namespace, model_name, model_tag))
        with open(rendered_Dockerfile, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'." % (filename, rendered_Dockerfile))

        return rendered_Dockerfile


    def _predict_server_describe(self,
                                model_name,
                                model_tag):
        pass        


    def predict_server_build(self,
                             model_name,
                             model_tag,
                             model_type,
                             model_path,
                             model_runtime=None,
                             model_chip=None,
                             input_stream_url=None,
                             input_stream_topic=None,
                             output_stream_url=None,
                             output_stream_topic=None,
                             build_type=None,
                             build_context_path=None,
                             image_registry_url=None,
                             image_registry_repo=None,
                             image_registry_namespace=None,
                             image_registry_base_tag=None,
                             image_registry_base_chip=None,
                             pipeline_templates_path=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not build_type:
            build_type = PipelineCli._default_build_type

        if not build_context_path: 
            build_context_path = PipelineCli._default_build_context_path

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        if not image_registry_base_tag:
            image_registry_base_tag = PipelineCli._default_image_registry_base_tag

        if not image_registry_base_chip:
            image_registry_base_chip = PipelineCli._default_model_chip

        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        build_context_path = os.path.expandvars(build_context_path)
        build_context_path = os.path.expanduser(build_context_path)
        build_context_path = os.path.abspath(build_context_path)
        build_context_path = os.path.normpath(build_context_path)

        pipeline_templates_path = os.path.expandvars(pipeline_templates_path)
        pipeline_templates_path = os.path.expanduser(pipeline_templates_path)
        pipeline_templates_path = os.path.abspath(pipeline_templates_path)
        pipeline_templates_path = os.path.normpath(pipeline_templates_path)
        pipeline_templates_path = os.path.relpath(pipeline_templates_path, build_context_path)
        pipeline_templates_path = os.path.normpath(pipeline_templates_path)

        model_path = os.path.expandvars(model_path)
        model_path = os.path.expanduser(model_path)
        model_path = os.path.abspath(model_path)
        model_path = os.path.normpath(model_path)
        model_path = os.path.relpath(model_path, build_context_path)
        model_path = os.path.normpath(model_path)

        if build_type == 'docker':
            generated_Dockerfile = self._create_predict_server_Dockerfile(model_name=model_name,
                                                                          model_tag=model_tag, 
                                                                          model_type=model_type, 
                                                                          model_path=model_path,
                                                                          model_runtime=model_runtime,
                                                                          model_chip=model_chip,
                                                                          input_stream_url=input_stream_url,
                                                                          input_stream_topic=input_stream_topic,
                                                                          output_stream_url=output_stream_url,
                                                                          output_stream_topic=output_stream_topic,
                                                                          image_registry_url=image_registry_url,
                                                                          image_registry_repo=image_registry_repo,
                                                                          image_registry_namespace=image_registry_namespace,
                                                                          image_registry_base_tag=image_registry_base_tag,
                                                                          image_registry_base_chip=image_registry_base_chip,
                                                                          pipeline_templates_path=pipeline_templates_path,
                                                                          build_context_path=build_context_path)

            cmd = 'docker build -t %s/%s/%s-%s:%s -f %s %s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag, generated_Dockerfile, build_context_path)

            print(cmd)
            print("")
            process = subprocess.call(cmd, shell=True)
        else:
            print("Build type '%s' not found." % build_type)


    def _create_predict_kube_Kubernetes_yaml(self,
                                                model_name,
                                                model_tag,
                                                model_type,
                                                model_runtime=None,
                                                model_chip=None,
                                                input_stream_url=None,
                                                input_stream_topic=None,
                                                output_stream_url=None,
                                                output_stream_topic=None,
                                                memory_limit='2Gi',
                                                core_limit='1000m',
                                                target_core_util_percentage='50',
                                                min_replicas='1',
                                                max_replicas='2',
                                                cluster_namespace=None,
                                                image_registry_url=None,
                                                image_registry_repo=None,
                                                image_registry_namespace=None,
                                                image_registry_base_tag=None,
                                                image_registry_base_chip=None,
                                                pipeline_templates_path=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        if not image_registry_base_tag:
            image_registry_base_tag = PipelineCli._default_image_registry_base_tag

        if not image_registry_base_chip:
            image_registry_base_chip = PipelineCli._default_model_chip

        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        pipeline_templates_path = os.path.expandvars(pipeline_templates_path)
        pipeline_templates_path = os.path.expanduser(pipeline_templates_path)
        pipeline_templates_path = os.path.abspath(pipeline_templates_path)
        pipeline_templates_path = os.path.normpath(pipeline_templates_path)

        context = {
                   'PIPELINE_MODEL_NAME': model_name,
                   'PIPELINE_MODEL_TAG': model_tag,
                   'PIPELINE_MODEL_TYPE': model_type,
                   'PIPELINE_MODEL_RUNTIME': model_runtime,
                   'PIPELINE_MODEL_CHIP': model_chip,
                   'PIPELINE_INPUT_STREAM_URL': input_stream_url,
                   'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
                   'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
                   'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
                   'PIPELINE_CORE_LIMIT': core_limit,
                   'PIPELINE_MEMORY_LIMIT': memory_limit,
                   'PIPELINE_TARGET_CORE_UTIL_PERCENTAGE': target_core_util_percentage,
                   'PIPELINE_MIN_REPLICAS': min_replicas,
                   'PIPELINE_MAX_REPLICAS': max_replicas,
                   'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
                   'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
                   'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
                   'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag,
                  }

        rendered_filenames = []

        model_router_deploy_yaml_templates_path = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._kube_router_deploy_template_registry['predict-router-split'][0][0]))
        path, filename = os.path.split(model_router_deploy_yaml_templates_path)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = os.path.normpath('.pipeline-generated-%s-%s-%s-router-split-deploy.yaml' % (image_registry_namespace, model_name, model_tag))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'" % (filename, rendered_filename))
            rendered_filenames += [rendered_filename]

        model_router_ingress_yaml_templates_path = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._kube_router_ingress_template_registry['predict-router-split'][0][0]))
        path, filename = os.path.split(model_router_ingress_yaml_templates_path)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = os.path.normpath('.pipeline-generated-%s-%s-router-split-ingress.yaml' % (image_registry_namespace, model_name))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'" % (filename, rendered_filename))
            rendered_filenames += [rendered_filename]

        model_router_svc_yaml_templates_path = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._kube_router_svc_template_registry['predict-router-split'][0][0]))
        path, filename = os.path.split(model_router_svc_yaml_templates_path)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = os.path.normpath('.pipeline-generated-%s-%s-router-split-svc.yaml' % (image_registry_namespace, model_name))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'" % (filename, rendered_filename))
            rendered_filenames += [rendered_filename]

        model_router_autoscale_yaml_templates_path = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._kube_router_autoscale_template_registry['predict-router-split'][0][0]))
        path, filename = os.path.split(model_router_autoscale_yaml_templates_path)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = os.path.normpath('.pipeline-generated-%s-%s-%s-router-split-autoscale.yaml' % (image_registry_namespace, model_name, model_tag))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'" % (filename, rendered_filename))
            rendered_filenames += [rendered_filename]

        return rendered_filenames


    def predict_server_shell(self,
                             model_name,
                             model_tag,
                             model_type,
                             model_runtime=None,
                             model_chip=None,
                             image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        cmd = 'docker exec -it %s bash' % container_name 
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)


    def predict_server_push(self,
                            model_name,
                            model_tag,
                            model_type,
                            model_runtime=None,
                            model_chip=None,
                            image_registry_url=None,
                            image_registry_repo=None,
                            image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        cmd = 'docker push %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)


    def predict_server_pull(self,
                            model_name,
                            model_tag,
                            model_type,
                            model_runtime=None,
                            model_chip=None,
                            image_registry_url=None,
                            image_registry_repo=None,
                            image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        cmd = 'docker pull %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)


    def predict_server_start(self,
                             model_name,
                             model_tag,
                             model_type,
                             model_runtime=None,
                             model_chip=None,
                             input_stream_url=None,
                             input_stream_topic=None,
                             output_stream_url=None,
                             output_stream_topic=None,
                             image_registry_url=None,
                             image_registry_repo=None,
                             image_registry_namespace=None,
                             predict_port='8080',
                             prometheus_port='9090',
                             grafana_port='3000',
                             memory_limit='2G'):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        # Note: We added `serve` to mimic AWS SageMaker and encourage ENTRYPOINT vs CMD as detailed here:  
        #       https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-inference-code.html
        cmd = 'docker run -itd -p %s:8080 -p %s:9090 -p %s:3000 -e PIPELINE_INPUT_STREAM_URL=%s -e PIPELINE_INPUT_STREAM_TOPIC=%s -e PIPELINE_OUTPUT_STREAM_URL=%s -e PIPELINE_OUTPUT_STREAM_TOPIC=%s --name=%s -m %s %s/%s/%s-%s:%s serve' % (predict_port, prometheus_port, grafana_port, input_stream_url, input_stream_topic, output_stream_url, output_stream_topic, container_name, memory_limit, image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)
        print("")
        print("container name: '%s'" % container_name)
        print("predict port: '%s'" % predict_port)
        print("prometheus port: '%s'" % prometheus_port)
        print("grafana port: '%s'" % grafana_port)
        print("")


    def predict_server_stop(self,
                            model_name,
                            model_tag,
                            model_type,
                            model_runtime=None,
                            model_chip=None,
                            image_registry_namespace=None): 

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        cmd = 'docker rm -f %s' % container_name
        print(cmd)
        print("")

        process = subprocess.call(cmd, shell=True)


    def predict_server_logs(self,
                            model_name,
                            model_tag,
                            model_type,
                            model_runtime=None,
                            model_chip=None,
                            image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        cmd = 'docker logs -f -%s' % container_name 
        print(cmd)
        print("")

        process = subprocess.call(cmd, shell=True)


    def _service_rollout(self,
                         service_name,
                         service_image,
                         service_tag):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                               pretty=True)
            found = False
            deployments = response.items
            for deployment in deployments:
                if service_name in deployment.metadata.name:
                    found = True
                    break
            if found:
                print("")
                print("Upgrading service '%s' using Docker image '%s:%s'." % (deployment.metadata.name, service_image, service_tag))
                print("")
                cmd = "kubectl set image deploy %s %s=%s:%s" % (deployment.metadata.name, deployment.metadata.name, service_image, service_tag)
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
                cmd = "kubectl rollout status deploy %s" % deployment.metadata.name
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
                cmd = "kubectl rollout history deploy %s" % deployment.metadata.name
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
            else:
                print("")
                print("Service '%s' is not running." % service_name)
                print("")


    def _service_history(self,
                         service_name):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                              pretty=True)
            found = False
            deployments = response.items
            for deployment in deployments:
                if service_name in deployment.metadata.name:
                    found = True
                    break
            if found:
                print("")
                cmd = "kubectl rollout status deploy %s" % deployment.metadata.name
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
                cmd = "kubectl rollout history deploy %s" % deployment.metadata.name
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
            else:
                print("")
                print("Service '%s' is not running." % service_name)
                print("")


    def _service_rollback(self,
                          service_name,
                          revision=None):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                              pretty=True)
            found = False
            deployments = response.items
            for deployment in deployments:
                if service_name in deployment.metadata.name:
                    found = True
                    break
            if found:
                print("")
                if revision:
                    print("Rolling back app '%s' to revision '%s'." % deployment.metadata.name, revision)
                    cmd = "kubectl rollout undo deploy %s --to-revision=%s" % (deployment.metadata.name, revision)
                else:
                    print("Rolling back app '%s'." % deployment.metadata.name)
                    cmd = "kubectl rollout undo deploy %s" % deployment.metadata.name
                print("")
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
                cmd = "kubectl rollout status deploy %s" % deployment.metadata.name
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
                cmd = "kubectl rollout history deploy %s" % deployment.metadata.name
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
            else:
                print("")
                print("Service '%s' is not running." % service_name)
                print("")


    def _filter_tar(self,
                    tarinfo):
        ignore_list = []
        for ignore in ignore_list:
            if ignore in tarinfo.name:
                return None

        return tarinfo


    def _tar(self,
             model_name,
             model_tag,
             model_type,
             model_runtime,
             model_chip,
             model_path,
             tar_path='.',
             filemode='w',
             compression='gz'):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        model_path = os.path.expandvars(model_path)
        model_path = os.path.expanduser(model_path)
        model_path = os.path.abspath(model_path)
        model_path = os.path.normpath(model_path)

        tar_path = os.path.expandvars(tar_path)
        tar_path = os.path.expanduser(tar_path)
        tar_path = os.path.abspath(tar_path)
        tar_path = os.path.normpath(tar_path)
    
        tar_filename = '%s-%s.tar.gz' % (model_name, model_tag)
        tar_path = os.path.join(tar_path, tar_filename) 
 
        print("")
        print("Compressing model_path '%s' into tar_path '%s'." % (model_path, tar_path))

        with tarfile.open(tar_path, '%s:%s' % (filemode, compression)) as tar:
            tar.add(model_path, arcname='.', filter=self._filter_tar)
        
        return tar_path


    def predict_kube_start(self,
                              model_name,
                              model_tag,
                              model_type,
                              model_runtime=None,
                              model_chip=None,
                              input_stream_url=None,
                              input_stream_topic=None,
                              output_stream_url=None,
                              output_stream_topic=None,
                              memory_limit='2Gi',
                              core_limit='1000m',
                              target_core_util_percentage='75',
                              min_replicas='1',
                              max_replicas='1',
                              cluster_namespace=None,
                              image_registry_url=None,
                              image_registry_repo=None,
                              image_registry_namespace=None,
                              image_registry_base_tag=None,
                              image_registry_base_chip=None,
                              pipeline_templates_path=None,
                              timeout=1200):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        if not image_registry_base_tag:
            image_registry_base_tag = PipelineCli._default_image_registry_base_tag

        if not image_registry_base_chip:
            image_registry_base_chip = PipelineCli._default_model_chip

        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        rendered_yamls = self._create_predict_kube_Kubernetes_yaml(
                                          model_name=model_name,
                                          model_tag=model_tag,
                                          model_type=model_type,
                                          model_runtime=model_runtime,
                                          model_chip=model_chip,
                                          input_stream_url=input_stream_url,
                                          input_stream_topic=input_stream_topic,
                                          output_stream_url=output_stream_url,
                                          output_stream_topic=output_stream_topic,
                                          memory_limit=memory_limit,
                                          core_limit=core_limit,
                                          target_core_util_percentage=target_core_util_percentage,
                                          min_replicas=min_replicas,
                                          max_replicas=max_replicas,
                                          image_registry_url=image_registry_url,
                                          image_registry_repo=image_registry_repo,
                                          image_registry_namespace=image_registry_namespace,
                                          image_registry_base_tag=image_registry_base_tag,
                                          image_registry_base_chip=image_registry_base_chip,
                                          pipeline_templates_path=pipeline_templates_path)

        for rendered_yaml in rendered_yamls:
            # For now, only handle '-deploy' and '-svc' and '-ingress' (not autoscale or routerules)
            if '-deploy' in rendered_yaml or '-svc' in rendered_yaml or '-ingress' in rendered_yaml:
                self._istio_apply(yaml_path=rendered_yaml,
                                  cluster_namespace=cluster_namespace)


    def _predict_server_deploy(self,
                                model_name,
                                model_tag,
                                model_type,
                                model_runtime,
                                model_chip,
                                model_path,
                                deploy_server_url,
                                timeout=1200):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        model_path = os.path.expandvars(model_path)
        model_path = os.path.expanduser(model_path)
        model_path = os.path.abspath(model_path)
        model_path = os.path.normpath(model_path)

        tar_path = self._tar(model_type=model_type,
                             model_name=model_name,
                             model_tag=model_tag,
                             model_runtime=model_runtime,
                             model_chip=model_chip,
                             model_path=model_path,
                             tar_path='.',
                             filemode='w',
                             compression='gz')

        upload_key = 'file'
        upload_value = tar_path 

        full_model_deploy_url = "%s/api/%s/model/deploy/%s/%s/%s/%s/%s" % (deploy_server_url.rstrip('/'), PipelineCli._pipeline_api_version, model_name, model_tag, model_type, model_runtime, model_chip) 

        with open(tar_path, 'rb') as fh:
            files = [(upload_key, (upload_value, fh))]
            print("")
            print("Deploying model tar.gz '%s' to '%s'." % (tar_path, full_model_deploy_url))
            headers = {'Accept': 'application/json'}
            try:
                response = requests.post(url=full_model_deploy_url, 
                                         headers=headers, 
                                         files=files, 
                                         timeout=timeout)

                if response.status_code != requests.codes.ok:
                    if response.text:
                        print("")
                        pprint(response.text)

                if response.status_code == requests.codes.ok:
                    print("")
                    print("Success!")
                    print("")
                else:
                    response.raise_for_status()
                    print("")
            except requests.exceptions.HTTPError as hte:
                print("Error while deploying model.\nError: '%s'" % str(hte))
                print("")
            except IOError as ioe:
                print("Error while deploying model.\nError: '%s'" % str(ioe))
                print("")
 
        if (os.path.isfile(tar_path)):
            print("")
            print("Cleaning up temporary file tar '%s'..." % tar_path)
            print("")
            os.remove(tar_path)


    def _optimize_predict(self,
                 model_name,
                 model_tag,
                 model_type,
                 model_runtime,
                 model_chip,
                 model_path,
                 input_path,
                 input_host_path,
                 output_path,
                 output_host_path,
                 optimize_type,
                 optimize_params):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        model_path = os.path.expandvars(model_path)
        model_path = os.path.expanduser(model_path)
        model_path = os.path.abspath(model_path)
        model_path = os.path.normpath(model_path)


    def _optimize_train(self,
                 model_name,
                 model_tag,
                 model_type,
                 model_runtime,
                 model_chip,
                 model_path,
                 input_path,
                 input_host_path,
                 output_path,
                 output_host_path,
                 optimize_type,
                 optimize_params):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        model_path = os.path.expandvars(model_path)
        model_path = os.path.expanduser(model_path)
        model_path = os.path.abspath(model_path)
        model_path = os.path.normpath(model_path)


    def predict_server_test(self,
                            model_endpoint_url,
                            test_request_path,
                            model_name=None,
                            model_tag=None,
                            model_type=None,
                            model_runtime=None,
                            model_chip=None,
                            test_request_concurrency=1,
                            test_request_mime_type='application/json',
                            test_response_mime_type='application/json',
                            test_request_timeout_seconds=15):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=test_request_concurrency) as executor:
            for _ in range(test_request_concurrency):
                executor.submit(self._test_single_prediction_http(
                                              model_endpoint_url=model_endpoint_url,
                                              test_request_path=test_request_path,
                                              model_name=model_name,
                                              model_tag=model_tag,
                                              model_type=model_type,
                                              model_runtime=model_runtime,
                                              model_chip=model_chip,
                                              test_request_mime_type=test_request_mime_type,
                                              test_response_mime_type=test_response_mime_type,
                                              test_request_timeout_seconds=test_request_timeout_seconds))


    def predict_kube_test(self,
                             model_name,
                             test_request_path,
                             model_tag=None,
                             model_type=None,
                             model_runtime=None,
                             model_chip=None,
                             image_registry_namespace=None,
                             cluster_namespace=None,
                             test_request_concurrency=1,
                             test_request_mime_type='application/json',
                             test_response_mime_type='application/json',
                             test_request_timeout_seconds=15):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        model_endpoint_url = self._get_cluster_ingress(model_name=model_name,
                                                       image_registry_namespace=image_registry_namespace,
                                                       cluster_namespace=cluster_namespace)

        model_endpoint_url = 'http://%s' % model_endpoint_url

        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=test_request_concurrency) as executor:
            for _ in range(test_request_concurrency):
                executor.submit(self._test_single_prediction_http(
                                              model_endpoint_url=model_endpoint_url,
                                              test_request_path=test_request_path,
                                              model_name=model_name,
                                              model_tag=model_tag,
                                              model_type=model_type,
                                              model_runtime=model_runtime,
                                              model_chip=model_chip,
                                              test_request_mime_type=test_request_mime_type,
                                              test_response_mime_type=test_response_mime_type,
                                              test_request_timeout_seconds=test_request_timeout_seconds))


    def predict_kafka_test(self,
                           input_stream_url,
                           input_stream_topic,
                           output_stream_url,
                           output_stream_topic,
                           test_request_path,
                           model_name=None,
                           model_tag=None,
                           model_typ=None,
                           model_runtime=None,
                           model_chip=None,
                           test_request_concurrency=1,
                           test_request_mime_type='application/json',
                           test_response_mine_type='application/json',
                           test_request_timeout_seconds=15):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip
    
        pass


    def _test_single_prediction_http(self,
                                     model_endpoint_url,
                                     test_request_path,
                                     model_name=None,
                                     model_tag=None,
                                     model_type=None,
                                     model_runtime=None,
                                     model_chip=None,
                                     test_request_mime_type='application/json',
                                     test_response_mime_type='application/json',
                                     test_request_timeout_seconds=15):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        test_request_path = os.path.expandvars(test_request_path)
        test_request_path = os.path.expanduser(test_request_path)
        test_request_path = os.path.abspath(test_request_path)
        test_request_path = os.path.normpath(test_request_path)

        full_model_endpoint_url = "%s/invocations" % model_endpoint_url.rstrip('/')
        print("")
        print("Predicting with file '%s' using '%s'" % (test_request_path, full_model_endpoint_url))
        print("")

        with open(test_request_path, 'rb') as fh:
            model_input_binary = fh.read()

        headers = {'Content-type': test_request_mime_type, 'Accept': test_response_mime_type} 
        from datetime import datetime 

        begin_time = datetime.now()
        response = requests.post(url=full_model_endpoint_url, 
                                 headers=headers, 
                                 data=model_input_binary, 
                                 timeout=test_request_timeout_seconds)
        end_time = datetime.now()

        if response.text:
            print("")
            pprint(response.text)

        if response.status_code == requests.codes.ok:
            print("")
            print("Success!")

        total_time = end_time - begin_time
        print("")
        print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
        print("")


    def predict_sage_test(self,
                          model_name,
                          test_request_path,
                          model_tag=None,
                          model_type=None,
                          model_runtime=None,
                          model_chip=None,
                          test_request_concurrency=1,
                          test_request_mime_type='application/json',
                          test_response_mime_type='application/json',
                          test_request_timeout_seconds=15):

        from concurrent.futures import ThreadPoolExecutor, as_completed

        with ThreadPoolExecutor(max_workers=test_request_concurrency) as executor:
            for _ in range(test_request_concurrency):
                executor.submit(self._test_single_prediction_sage(
                                              model_name=model_name,
                                              test_request_path=test_request_path,
                                              model_tag=model_tag,
                                              model_type=model_type,
                                              model_runtime=model_runtime,
                                              model_chip=model_chip,
                                              test_request_mime_type=test_request_mime_type,
                                              test_response_mime_type=test_response_mime_type,
                                              test_request_timeout_seconds=test_request_timeout_seconds))


    def _test_single_prediction_sage(self,
                                     model_name,
                                     test_request_path,
                                     model_tag=None,
                                     model_type=None,
                                     model_runtime=None,
                                     model_chip=None,
                                     image_registry_namespace=None,
                                     test_request_mime_type='application/json',
                                     test_response_mime_type='application/json',
                                     test_request_timeout_seconds=15):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        test_request_path = os.path.expandvars(test_request_path)
        test_request_path = os.path.expanduser(test_request_path)
        test_request_path = os.path.abspath(test_request_path)
        test_request_path = os.path.normpath(test_request_path)

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        print("")
        print("Predicting with file '%s' using endpoint '%s-%s'" % (test_request_path, image_registry_namespace, model_name))
        print("")

        with open(test_request_path, 'rb') as fh:
            model_input_binary = fh.read()

        from datetime import datetime

        begin_time = datetime.now()
        body = model_input_binary.decode('utf-8')

        sagemaker_client = boto3.client('runtime.sagemaker')
        response = sagemaker_client.invoke_endpoint(
                                              EndpointName='%s-%s' % (image_registry_namespace, model_name),
                                              Body=model_input_binary,
                                              ContentType=test_request_mime_type,
                                              Accept=test_response_mime_type)
        end_time = datetime.now()

        if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("")
            print("Variant: '%s'" % response['InvokedProductionVariant'])
            print("")
            pprint(response['Body'].read().decode('utf-8'))
       
            print("")
            print("Success!")
            print("")
        else:
            exit(1)

        total_time = end_time - begin_time
        print("")
        print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
        print("")


    def train_kube_status(self):
        self._cluster_status()


    def predict_kube_status(self):
        self._cluster_status()


    def _cluster_status(self):
        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        print("")
        print("Versions")
        print("********")
        self.version()

        print("")
        print("Nodes")
        print("*****")
        self._get_all_nodes()

        self._environment_volumes()

        print("")
        print("Environment Resources")
        print("*********************")        
        self._environment_resources()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_service_for_all_namespaces(watch=False,
                                                                     pretty=True)
            services = response.items
            for svc in services:
                self._service_resources(service_name=svc.metadata.name)

        print("")
        print("Service Descriptions")
        print("********************")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_service_for_all_namespaces(watch=False,
                                                                     pretty=True)
            services = response.items
            for svc in services:
                self._service_describe(service_name=svc.metadata.name)

        print("")
        print("DNS Internal (Public)")
        print("*********************")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_service_for_all_namespaces(watch=False, 
                                                                     pretty=True)
            services = response.items
            for svc in services:
                ingress = 'Not public' 
                if svc.status.load_balancer.ingress and len(svc.status.load_balancer.ingress) > 0:
                    if (svc.status.load_balancer.ingress[0].hostname):
                        ingress = svc.status.load_balancer.ingress[0].hostname
                    if (svc.status.load_balancer.ingress[0].ip):
                        ingress = svc.status.load_balancer.ingress[0].ip               
                print("%s (%s)" % (svc.metadata.name, ingress))

        print("")
        print("Deployments")
        print("***********")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                              pretty=True)
            deployments = response.items
            for deployment in deployments:
                print("%s (Available Replicas: %s)" % (deployment.metadata.name, deployment.status.available_replicas))

        print("")
        print("Pods")
        print("****")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                                 pretty=True)
            pods = response.items
            for pod in pods:
                print("%s (%s)" % (pod.metadata.name, pod.status.phase))

        print("")
        print("Note:  If you are using Minikube, use 'minikube service list'.")
        print("")

        #print("")
        #print("Ingress")
        #print("*******")
        #self._get_ingress_urls()


    def _get_pod_by_service_name(self,
                                 service_name):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        found = False 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, pretty=True)
            pods = response.items
            for pod in pods:
                if service_name in pod.metadata.name:
                    found = True
                    break
        if found:
            return pod
        else:
            return None


    def _get_svc_by_service_name(self,
                                 service_name):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        found = False
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_service_for_all_namespaces(watch=False, 
                                                                     pretty=True)
            services = response.items
            for svc in services:
                if service_name in svc.metadata.name:
                    found = True
                    break
        if found:
            return svc 
        else:
            return None


    def _get_all_available_services(self):

        available_services = list(PipelineCli._kube_deploy_registry.keys())
        available_services.sort()
        for service in available_services:
            print(service)


    def _get_all_nodes(self):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_node(watch=False, pretty=True)
            nodes = response.items
            for node in nodes:
                print("%s" % node.metadata.labels['kubernetes.io/hostname'])


    def predict_kube_shell(self,
                              model_name,
                              model_tag,
                              model_type,
                              model_runtime=None,
                              model_chip=None,
                              cluster_namespace=None,
                              image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip: 
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_shell(service_name=service_name,
                            cluster_namespace=cluster_namespace)


    def _service_shell(self,
                       service_name,
                       cluster_namespace=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                                 pretty=True)
            pods = response.items
            for pod in pods:
                if service_name in pod.metadata.name:
                    break
            print("")
            print("Connecting to '%s'" % pod.metadata.name)      
            print("")
            subprocess.call("kubectl exec -it %s bash" % pod.metadata.name, shell=True)
        print("")


    def predict_kube_logs(self,
                             model_name,
                             model_tag,
                             model_type,
                             model_runtime=None,
                             model_chip=None,
                             cluster_namespace=None,
                             image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_logs(service_name=service_name,
                           cluster_namespace=cluster_namespace)


    def _service_logs(self,
                      service_name,
                      cluster_namespace=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                                 pretty=True)
            found = False
            pods = response.items
            for pod in pods:
                if service_name in pod.metadata.name:
                    found = True
                    break
            if found:
                print("")
                print("Tailing logs on '%s'." % pod.metadata.name)
                print("")
                subprocess.call("kubectl logs -f %s" % pod.metadata.name, shell=True)
                print("")
            else:
                print("")
                print("Service '%s' is not running." % service_name)
                print("")


    def _service_describe(self,
                          service_name):

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_pod_for_all_namespaces(watch=False,
                                                                 pretty=True)
            pods = response.items
            for pod in pods:
                if service_name in pod.metadata.name:
                    break
            print("")
            print("Connecting to '%s'" % pod.metadata.name)
            print("")
            subprocess.call("kubectl describe pod %s" % pod.metadata.name, shell=True)
        print("")


    def predict_kube_scale(self,
                           model_name,
                           model_tag,
                           model_type,
                           replicas,
                           model_runtime=None,
                           model_chip=None,
                           cluster_namespace=None,
                           image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_scale(service_name=service_name,
                            replicas=replicas,
                            cluster_namespace=cluster_namespace)


    # TODO:  See https://github.com/istio/istio/tree/master/samples/helloworld
    #             for more details on how istio + autoscaling work
    def predict_kube_autoscale(self,
                                  model_name,
                                  model_tag,
                                  model_type,
                                  cpu_percent,
                                  min_replicas,
                                  max_replicas,
                                  model_runtime=None,
                                  model_chip=None,
                                  cluster_namespace=None,
                                  image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        # TODO:  make sure resources/requests/cpu has been set to something in the yaml
        #        ie. istioctl kube-inject -f helloworld.yaml -o helloworld-istio.yaml
        #        then manually edit as follows:
        #
        #  resources:
        #    requests:
        #      cpu: 100m

        cmd = "kubectl autoscale deployment %s-%s-%s --cpu-percent=%s --min=%s --max=%s" % (image_registry_namespace, model_name, model_tag, cpu_percent, min_replicas, max_replicas)
        print("")
        print("Running '%s'." % cmd)
        print("")
        subprocess.call(cmd, shell=True)
        cmd = "kubectl get hpa"
        print("")
        print("Running '%s'." % cmd)
        print("")
        subprocess.call(cmd, shell=True)
        print("")


    def _service_scale(self,
                       service_name,
                       replicas,
                       cluster_namespace=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        # TODO:  Filter by namespace
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False, 
                                                                              pretty=True)
            found = False
            deployments = response.items
            for deploy in deployments:
                if service_name in deploy.metadata.name:
                    found = True
                    break
            if found:
                print("")
                print("Scaling service '%s' to '%s' replicas." % (deploy.metadata.name, replicas))
                print("")
                cmd = "kubectl scale deploy %s --replicas=%s --namespace=%s" % (deploy.metadata.name, replicas, cluster_namespace)
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
            else:
                print("")
                print("Service '%s' is not running." % service_name)
                print("") 


    def _environment_volumes(self):

        print("")
        print("Volumes")
        print("*******")
        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_persistent_volume(watch=False,
                                                            pretty=True)
            claims = response.items
            for claim in claims:
                print("%s" % (claim.metadata.name))

        print("")
        print("Volume Claims")
        print("*************")
        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_persistent_volume_claim_for_all_namespaces(watch=False,
                                                                                     pretty=True)
            claims = response.items
            for claim in claims:
                print("%s" % (claim.metadata.name))


    def _get_deploy_yamls(self, 
                          service_name):
        try:
            (deploy_yamls, dependencies) = PipelineCli._kube_deploy_registry[service_name]
        except:
            dependencies = []
            deploy_yamls = []

        if len(dependencies) > 0:
            for dependency in dependencies:
                deploy_yamls = deploy_yamls + self._get_deploy_yamls(service_name=dependency)

        return deploy_yamls 


    def _get_svc_yamls(self, 
                       service_name):
        try:
            (svc_yamls, dependencies) = PipelineCli._kube_svc_registry[service_name]
        except:
            dependencies = []
            svc_yamls = []
       
        if len(dependencies) > 0:
            for dependency_service_name in dependencies:
                svc_yamls = svc_yamls + self._get_svc_yamls(service_name=dependency_service_name)

        return svc_yamls


    def _kube_apply(self,
                    yaml_path,
                    cluster_namespace=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        yaml_path = os.path.normpath(yaml_path)

        cmd = "kubectl apply --namespace %s -f %s" % (cluster_namespace, yaml_path)
        self._kube(cmd=cmd)


    def _kube_create(self,
                     yaml_path,
                     cluster_namespace=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        yaml_path = os.path.normpath(yaml_path)

        cmd = "kubectl create --namespace %s -f %s --save-config --record" % (cluster_namespace, yaml_path)
        self._kube(cmd=cmd)


    def _kube_delete(self,
                     yaml_path,
                     cluster_namespace=None):

        yaml_path = os.path.normpath(yaml_path)

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        cmd = "kubectl delete --namespace %s -f %s" % (cluster_namespace, yaml_path)
        self._kube(cmd=cmd) 
   
 
    def _kube(self, cmd):
        print("")
        print("Running '%s'." % cmd)
        print("")
        subprocess.call(cmd, shell=True)
        print("")


    def predict_kube_describe(self):
        print("")
        print("Traffic Ingress")
        print("***************")
        cmd = "kubectl get ingress -o wide --all-namespaces"
        subprocess.call(cmd, shell=True)

        print("")
        print("Traffic Route Rules")
        print("********************")
        cmd = "kubectl get routerules -o wide --all-namespaces"
        subprocess.call(cmd, shell=True)

        print("")
        cmd = "kubectl describe routerules --all-namespaces"
        subprocess.call(cmd, shell=True)
        print("")


    def _get_cluster_ingress(self,
                             model_name,
                             cluster_namespace=None,
                             image_registry_namespace=None):
    
        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        ingress_name = '%s-%s' % (image_registry_namespace, model_name)

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        ingress = kubeclient_v1_beta1.read_namespaced_ingress(ingress_name, 
                                                               cluster_namespace)
        endpoint = None 
        if ingress.status.load_balancer.ingress and len(ingress.status.load_balancer.ingress) > 0:
            if (ingress.status.load_balancer.ingress[0].hostname):
                endpoint = ingress.status.load_balancer.ingress[0].hostname
            if (ingress.status.load_balancer.ingress[0].ip):
                endpoint = ingress.status.load_balancer.ingress[0].ip
        
        return endpoint


    def _istio_apply(self,
                     yaml_path,
                     cluster_namespace=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        yaml_path = os.path.normpath(yaml_path)

        cmd = "istioctl kube-inject -f %s" % yaml_path
        print("")
        print("Running '%s'." % cmd)
        print("")
        new_yaml_bytes = subprocess.check_output(cmd, shell=True)
        new_yaml_path = '%s-istio' % yaml_path
        with open(new_yaml_path, 'wt') as fh:
            fh.write(new_yaml_bytes.decode('utf-8'))
            print("'%s' => '%s'" % (yaml_path, new_yaml_path))
        print("")

        cmd = "kubectl apply --namespace %s -f %s" % (cluster_namespace, new_yaml_path)
        print("")
        print("Running '%s'." % cmd)
        print("")
        subprocess.call(cmd, shell=True)
        print("")


    def predict_kube_route(self,
                              model_name,
                              model_type,
                              model_tag_list,
                              model_weight_list,
                              model_runtime=None,
                              model_chip=None,
                              traffic_type='split',
                              pipeline_templates_path=None,
                              image_registry_namespace=None,
                              cluster_namespace=None):

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip
 
        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        if len(model_tag_list) != len(model_weight_list):
            print("`model_tag_list` and `model_weight_list` must be the same length.  The `model_weight_list` should consist of integers or floats between 0 and 100.  All weights should total 100.  Please use brackets when specifying each list as follows:\n\t--model-tag-list=[a,b,...] and --model-weight-list=[35,65,...]")
            print("")
            exit(1)

        self._validate_and_prep_model_weight_list(model_weight_list)

        model_tag_list = [ self._validate_and_prep_model_tag(model_tag) for model_tag in model_tag_list ]

        context = {'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
                   'PIPELINE_MODEL_NAME': model_name,
                   'PIPELINE_MODEL_TYPE': model_type,
                   'PIPELINE_MODEL_RUNTIME': model_runtime,
                   'PIPELINE_MODEL_CHIP': model_chip,
                   'PIPELINE_MODEL_TAG_LIST': model_tag_list,
                   'PIPELINE_MODEL_WEIGHT_LIST': model_weight_list,
                   'PIPELINE_MODEL_NUM_TAGS_AND_WEIGHTS': len(model_tag_list)}

        model_router_routerules_yaml_templates_path = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._kube_router_routerules_template_registry['predict-router-split'][0][0]))
        path, filename = os.path.split(model_router_routerules_yaml_templates_path)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        tag_weight_filename_snippet = '' 
        for idx in range(len(model_tag_list)):
            tag_weight_filename_snippet = '%s-%s-%s' % (tag_weight_filename_snippet, model_tag_list[idx], model_weight_list[idx])

        tag_weight_filename_snippet = tag_weight_filename_snippet.lstrip('-')
        tag_weight_filename_snippet = tag_weight_filename_snippet.rstrip('-')

        rendered_filename = os.path.normpath('.pipeline-generated-%s-%s-%s-router-split-routerules.yaml' % (image_registry_namespace, model_name, tag_weight_filename_snippet))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'." % (filename, rendered_filename))

        self._kube_apply(rendered_filename, cluster_namespace)


    def predict_sage_route(self,
                           model_name,
                           model_type,
                           model_tag_list,
                           model_weight_list,
                           model_runtime=None,
                           model_chip=None,
                           router_type='split',
                           pipeline_templates_path=None,
                           image_registry_namespace=None):

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        if len(model_tag_list) != len(model_weight_list):
            print("`model_tag_list` and `model_weight_list` must be the same length.  The `model_weight_list` should consist of integers or floats between 0 and 100.  All weights should total 100.  Please use brackets when specifying each list as follows:\n\t--model-tag-list=[a,b,...] and --model-weight-list=[35,65,...]")
            print("")
            exit(1)

        self._validate_and_prep_model_weight_list(model_weight_list)

        model_tag_list = [ self._validate_and_prep_model_tag(model_tag) for model_tag in model_tag_list ]

        tag_weight_dict_list = [] 

        for idx in range(len(model_tag_list)):
            tag_weight_dict = {
                    'VariantName': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag_list[idx]),
                    'DesiredWeight': model_weight_list[idx],
                    'DesiredInstanceCount': 1
                }

            tag_weight_dict_list += tag_weight_dict

        sagemaker_admin_client = boto3.client('sagemaker')

        from datetime import datetime

        begin_time = datetime.now()

        response = client.update_endpoint_weights_and_capacities(
            EndpointName='%s-%s' % (image_registry_namespace, model_name),
            DesiredWeightsAndCapacities=tag_weight_dict_list,
        )

        total_time = end_time - begin_time

        if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("")
            print("EndpointArn: '%s'" % response['EndpointArn'])
            print("")
            print("Success!")
            print("")
        else:
            exit(1)

        print("")
        print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
        print("")


#(Enterprise) pipeline experiment-add              <-- Add Cluster to Experiment
#             pipeline experiment-start            <-- Start Experiment
#             pipeline experiment-status           <-- Experiment Status (Bandit-based Rewards)
#             pipeline experiment-stop             <-- Stop Experiment
#             pipeline experiment-update           <-- Update Experiment (Bandit-based Routing)

#    def _experiment_start(self,
#                         experiment_name,
#                         experiment_tag,
#                         experiment_type):
#
#        pass


    def _service_start(self,
                       service_name,
                       pipeline_services_path=None,
                       cluster_namespace=None):

        if not pipeline_services_path:
            pipeline_services_path = PipelineCli._default_pipeline_services_path

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        deploy_yaml_filenames = []
        svc_yaml_filenames = []

        deploy_yaml_filenames = deploy_yaml_filenames + self._get_deploy_yamls(service_name=service_name)
        deploy_yaml_filenames = ['%s/%s' % (pipeline_services_path, deploy_yaml_filename) for deploy_yaml_filename in deploy_yaml_filenames]
        print("Using '%s'" % deploy_yaml_filenames)
 
        svc_yaml_filenames = svc_yaml_filenames + self._get_svc_yamls(service_name=service_name)
        svc_yaml_filenames = ['%s/%s' % (pipeline_services_path, svc_yaml_filename) for svc_yaml_filename in svc_yaml_filenames]
        print("Using '%s'" % svc_yaml_filenames)

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        print("")
        print("Starting service '%s'." % service_name)
        print("")
        print("Kubernetes Deployments:")
        print("")
        for deploy_yaml_filename in deploy_yaml_filenames:
            deploy_yaml_filename = os.path.normpath(deploy_yaml_filename)
            cmd = "kubectl apply -f %s" % deploy_yaml_filename
            print("Running '%s'." % cmd)
            print("")
            subprocess.call(cmd, shell=True)
            print("")
        print("")
        print("Kubernetes Services:")
        print("")
        for svc_yaml_filename in svc_yaml_filenames:
            svc_yaml_filename = os.path.normpath(svc_yaml_filename)
            cmd = "kubectl apply -f %s" % svc_yaml_filename
            print("Running '%s'." % cmd)
            print("")
            subprocess.call(cmd, shell=True)
            print("")
        print("")


    def predict_kube_stop(self,
                             model_name,
                             model_tag,
                             model_type,
                             model_runtime=None,
                             model_chip=None,
                             cluster_namespace=None,
                             image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)
        self._service_stop(service_name=service_name, 
                           cluster_namespace=cluster_namespace)


    def _service_stop(self,
                      service_name,
                      cluster_namespace=None):

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False, pretty=True)
            found = False
            deployments = response.items
            for deploy in deployments:
                if service_name in deploy.metadata.name:
                    found = True
                    break
            if found:
                print("")
                print("Deleting service '%s'." % deploy.metadata.name)
                print("")
                cmd = "kubectl delete deploy %s --namespace %s" % (deploy.metadata.name, cluster_namespace)
                print("Running '%s'." % cmd)
                print("")
                subprocess.call(cmd, shell=True)
                print("")
            else:
                print("")
                print("Service '%s' is not running." % service_name)
                print("")


    def train_server_pull(self,
                          model_name,
                          model_tag,
                          model_type,
                          model_runtime=None,
                          model_chip=None,
                          image_registry_url=None,
                          image_registry_repo=None,
                          image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        cmd = 'docker pull %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)


    def train_server_push(self,
                          model_name,
                          model_tag,
                          model_type,
                          model_runtime=None,
                          model_chip=None,
                          image_registry_url=None,
                          image_registry_repo=None,
                          image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        cmd = 'docker push %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)


    def train_server_logs(self,
                          model_name,
                          model_tag,
                          model_type,
                          model_runtime=None,
                          model_chip=None,
                          image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        cmd = 'docker logs -f %s' % container_name

        print(cmd)
        print("")

        process = subprocess.call(cmd, shell=True)


    def train_server_shell(self,
                           model_name,
                           model_tag,
                           model_type,
                           model_runtime=None,
                           model_chip=None,
                           image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        cmd = 'docker exec -it %s bash' % container_name 
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)


    def _create_train_server_Dockerfile(self,
                                        model_name,
                                        model_tag,
                                        model_type,
                                        model_runtime,
                                        model_chip,
                                        model_path,
                                        build_context_path,
                                        input_stream_url,
                                        input_stream_topic,
                                        output_stream_url,
                                        output_stream_topic,
                                        image_registry_url,
                                        image_registry_repo,
                                        image_registry_namespace,
                                        image_registry_base_tag,
                                        image_registry_base_chip,
                                        pipeline_templates_path):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        print("")
        print("Using templates in '%s'." % pipeline_templates_path)
        print("(Specify --pipeline-templates-path if the templates live elsewhere.)")
        print("")

        context = {
                   'PIPELINE_MODEL_NAME': model_name,
                   'PIPELINE_MODEL_TAG': model_tag,
                   'PIPELINE_MODEL_TYPE': model_type,
                   'PIPELINE_MODEL_RUNTIME': model_runtime,
                   'PIPELINE_MODEL_CHIP': model_chip,
                   'PIPELINE_MODEL_PATH': model_path,
                   'PIPELINE_INPUT_STREAM_URL': input_stream_url,
                   'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
                   'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
                   'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
                   'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
                   'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
                   'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
                   'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag
                  }

        model_train_cpu_Dockerfile_templates_path = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._Dockerfile_template_registry['train-server'][0][0]))
        path, filename = os.path.split(model_train_cpu_Dockerfile_templates_path)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = os.path.normpath('%s/.pipeline-generated-%s-%s-%s-Dockerfile' % (build_context_path, image_registry_namespace, model_name, model_tag))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'." % (filename, rendered_filename))

        return rendered_filename


    def train_server_build(self,
                           model_name,
                           model_tag,
                           model_type,
                           model_path,
                           model_runtime=None,
                           model_chip=None,
                           input_stream_url=None,
                           input_stream_topic=None,
                           output_stream_url=None,
                           output_stream_topic=None,
                           build_type=None,
                           build_context_path=None,
                           image_registry_url=None,
                           image_registry_repo=None,
                           image_registry_namespace=None,
                           image_registry_base_tag=None,
                           image_registry_base_chip=None,
                           pipeline_templates_path=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip: 
            model_chip = PipelineCli._default_model_chip

        if not build_type:
            build_type = PipelineCli._default_build_type

        if not build_context_path:
            build_context_path = PipelineCli._default_build_context_path

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        if not image_registry_base_tag:
            image_registry_base_tag = PipelineCli._default_image_registry_base_tag

        if not image_registry_base_chip:
            image_registry_base_chip = PipelineCli._default_model_chip

        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        build_context_path = os.path.normpath(build_context_path)
        build_context_path = os.path.expandvars(build_context_path)
        build_context_path = os.path.expanduser(build_context_path)
        build_context_path = os.path.normpath(build_context_path)
        build_context_path = os.path.abspath(build_context_path)
        build_context_path = os.path.normpath(build_context_path)
        print(build_context_path)

        pipeline_templates_path = os.path.normpath(pipeline_templates_path)
        pipeline_templates_path = os.path.expandvars(pipeline_templates_path)
        pipeline_templates_path = os.path.expanduser(pipeline_templates_path)
        pipeline_templates_path = os.path.abspath(pipeline_templates_path)
        pipeline_templates_path = os.path.normpath(pipeline_templates_path)
        pipeline_templates_path = os.path.relpath(pipeline_templates_path, build_context_path)
        pipeline_templates_path = os.path.normpath(pipeline_templates_path)
        print(pipeline_templates_path)

        model_path = os.path.normpath(model_path)
        model_path = os.path.expandvars(model_path)
        model_path = os.path.expanduser(model_path)
        model_path = os.path.abspath(model_path)
        model_path = os.path.normpath(model_path)
        model_path = os.path.relpath(model_path, build_context_path)
        model_path = os.path.normpath(model_path)
        print(model_path)

        if build_type == 'docker':
            generated_Dockerfile = self._create_train_server_Dockerfile(model_name=model_name,
                                                                        model_tag=model_tag,
                                                                        model_type=model_type,
                                                                        model_runtime=model_runtime,
                                                                        model_chip=model_chip,
                                                                        model_path=model_path,
                                                                        input_stream_url=input_stream_url,
                                                                        input_stream_topic=input_stream_topic,
                                                                        output_stream_url=output_stream_url,
                                                                        output_stream_topic=output_stream_topic,
                                                                        build_context_path=build_context_path,
                                                                        image_registry_url=image_registry_url,
                                                                        image_registry_repo=image_registry_repo,
                                                                        image_registry_namespace=image_registry_namespace,
                                                                        image_registry_base_tag=image_registry_base_tag,
                                                                        image_registry_base_chip=image_registry_base_chip,
                                                                        pipeline_templates_path=pipeline_templates_path)

            cmd = 'docker build -t %s/%s/%s-%s:%s -f %s %s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag, generated_Dockerfile, build_context_path)

            print(cmd)
            print("")
            process = subprocess.call(cmd, shell=True)
        else:
            print("Build type '%s' not found." % build_type)


    def train_server_start(self,
                           model_name,
                           model_tag,
                           model_type,
                           model_runtime=None,
                           model_chip=None,
                           input_path=None,
                           output_path=None,
                           input_stream_url=None,
                           input_stream_topic=None,
                           output_stream_url=None,
                           output_stream_topic=None,
                           train_args='',
                           memory_limit='2G',
                           core_limit='1000m',
                           image_registry_url=None,
                           image_registry_repo=None,
                           image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if input_path:
            input_path = os.path.expandvars(input_path)
            input_path = os.path.expanduser(input_path)
            input_path = os.path.abspath(input_path)
            input_path = os.path.normpath(input_path)

        if output_path:
            output_path = os.path.expandvars(output_path)
            output_path = os.path.expanduser(output_path)
            output_path = os.path.abspath(output_path)
            output_path = os.path.normpath(output_path)

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        # environment == local, task type == worker, and no cluster definition
        tf_config_local_run = '\'{\"environment\": \"local\", \"task\":{\"type\": \"worker\"}}\''

        # Note:  We added `train` to mimic AWS SageMaker and encourage ENTRYPOINT vs CMD per https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html
        # /opt/ml/input/data/{training|validation|testing} per https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        cmd = 'docker run -itd -p 2222:2222 -p 6006:6006 -e PIPELINE_INPUT_STREAM_URL=%s -e PIPELINE_INPUT_STREAM_TOPIC=%s -e PIPELINE_OUTPUT_STREAM_URL=%s -e PIPELINE_OUTPUT_STREAM_TOPIC=%s -e TF_CONFIG=%s -e PIPELINE_MODEL_TRAIN_ARGS=%s -v %s:/opt/ml/input/ -v %s:/opt/ml/output/ --name=%s -m %s %s/%s/%s-%s:%s train' % (input_stream_url, input_stream_topic, output_stream_url, output_stream_topic, tf_config_local_run, train_args, input_path, output_path, image_registry_namespace, container_name, memory_limit, image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
        print(cmd)
        print("")
        process = subprocess.call(cmd, shell=True)

        print("")
        print("container name: '%s'" % container_name)


    def train_server_stop(self,
                          model_name,
                          model_tag,
                          model_type,
                          model_runtime=None,
                          model_chip=None,
                          image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        cmd = 'docker rm -f %s' % container_name 

        print(cmd)
        print("")

        process = subprocess.call(cmd, shell=True)


    def _create_train_kube_yaml(self,
                                model_name,
                                model_tag,
                                model_type,
                                model_runtime,
                                model_chip,
                                input_path,
                                output_path,
                                input_stream_url,
                                input_stream_topic,
                                output_stream_url,
                                output_stream_topic,
                                master_replicas,
                                ps_replicas,
                                worker_replicas,
                                train_args,
                                image_registry_url,
                                image_registry_repo,
                                image_registry_namespace,
                                image_registry_base_tag,
                                image_registry_base_chip,
                                pipeline_templates_path,
                                cluster_namespace,
                                worker_memory_limit,
                                worker_core_limit):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        context = {
                   'PIPELINE_MODEL_NAME': model_name,
                   'PIPELINE_MODEL_TAG': model_tag,
                   'PIPELINE_MODEL_TYPE': model_type,
                   'PIPELINE_MODEL_RUNTIME': model_runtime,
                   'PIPELINE_MODEL_CHIP': model_chip,
                   'PIPELINE_INPUT_HOST_PATH': input_path,
                   'PIPELINE_OUTPUT_HOST_PATH': output_path,
                   'PIPELINE_INPUT_STREAM_URL': input_stream_url,
                   'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
                   'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
                   'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
                   'PIPELINE_MODEL_TRAIN_ARGS': train_args,
                   'PIPELINE_WORKER_CORE_LIMIT': worker_core_limit,
                   'PIPELINE_WORKER_MEMORY_LIMIT': worker_memory_limit,
                   'PIPELINE_MASTER_REPLICAS': int(master_replicas),
                   'PIPELINE_PS_REPLICAS': int(ps_replicas),
                   'PIPELINE_WORKER_REPLICAS': int(worker_replicas),
                   'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
                   'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
                   'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
                   'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag,
                   }

        predict_clustered_template = os.path.normpath(os.path.join(pipeline_templates_path, PipelineCli._train_kube_template_registry['train-cluster'][0][0]))
        path, filename = os.path.split(predict_clustered_template)
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = os.path.normpath('.pipeline-generated-%s-%s-%s.yaml' % (image_registry_namespace, model_name, model_tag))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
        print("'%s' => '%s'." % (filename, rendered_filename))

        return rendered_filename


    def train_kube_connect(self,
                              model_name,
                              model_tag,
                              model_type,                            
                              model_runtime=None,
                              model_chip=None,
                              local_port=None,
                              service_port=None,
                              cluster_namespace=None,
                              image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_connect(service_name=service_name,
                              cluster_namespace=cluster_namespace,
                              local_port=local_port,
                              service_port=service_port)


    def train_kube_describe(self,
                               model_name,
                               model_tag,
                               model_type,
                               model_runtime=None,
                               model_chip=None,
                               cluster_namespace=None,
                               image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_describe(service_name=service_name)

    
    def train_kube_shell(self,
                            model_name,
                            model_tag,
                            model_type,
                            model_runtime=None,
                            model_chip=None,
                            cluster_namespace=None,
                            image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelienCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_shell(service_name=service_name,
                            cluster_namespace=cluster_namespace)


    def train_kube_start(self,
                         model_name,
                         model_tag,
                         model_type,
                         input_path,
                         output_path,
                         master_replicas,
                         ps_replicas,
                         worker_replicas,
                         model_runtime=None,
                         model_chip=None,
                         input_stream_url=None,
                         input_stream_topic=None,
                         output_stream_url=None,
                         output_stream_topic=None,                            
                         train_args='',
                         image_registry_url=None,
                         image_registry_repo=None,
                         image_registry_namespace=None,
                         image_registry_base_tag=None,
                         image_registry_base_chip=None,
                         pipeline_templates_path=None,
                         cluster_namespace=None,
                         worker_memory_limit=None,
                         worker_core_limit=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if input_path:
            input_path = os.path.expandvars(input_path)
            input_path = os.path.expanduser(input_path)
            input_path = os.path.abspath(input_path)
            input_path = os.path.normpath(input_path)

        if output_path:
            output_path = os.path.expandvars(output_path)
            output_path = os.path.expanduser(output_path)
            output_path = os.path.abspath(output_path)
            output_path = os.path.normpath(output_path)

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        if not image_registry_base_tag:
            image_registry_base_tag = PipelineCli._default_image_registry_base_tag

        if not image_registry_base_chip:
            image_registry_base_chip = PipelineCli._default_model_chip

        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        pipeline_templates_path = os.path.expandvars(pipeline_templates_path)
        pipeline_templates_path = os.path.expanduser(pipeline_templates_path)
        pipeline_templates_path = os.path.abspath(pipeline_templates_path)
        pipeline_templates_path = os.path.normpath(pipeline_templates_path)

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        generated_yaml_path = self._create_train_kube_yaml(
                                                           model_name=model_name,
                                                           model_tag=model_tag,
                                                           model_type=model_type,
                                                           model_runtime=model_runtime,
                                                           model_chip=model_chip,
                                                           input_path=input_path,
                                                           output_path=output_path,
                                                           master_replicas=master_replicas,
                                                           ps_replicas=ps_replicas,
                                                           worker_replicas=worker_replicas,
                                                           input_stream_url=input_stream_url,
                                                           input_stream_topic=input_stream_topic,
                                                           output_stream_url=output_stream_url,
                                                           output_stream_topic=output_stream_topic,
                                                           train_args=train_args,
                                                           image_registry_url=image_registry_url,
                                                           image_registry_repo=image_registry_repo,
                                                           image_registry_namespace=image_registry_namespace,
                                                           image_registry_base_tag=image_registry_base_tag,
                                                           image_registry_base_chip=image_registry_base_chip,
                                                           pipeline_templates_path=pipeline_templates_path,
                                                           cluster_namespace=cluster_namespace,
                                                           worker_memory_limit=worker_memory_limit,
                                                           worker_core_limit=worker_core_limit)

        generated_yaml_path = os.path.normpath(generated_yaml_path)

        # For now, only handle '-deploy' and '-svc' yaml's
        self._kube_apply(yaml_path=generated_yaml_path,
                         cluster_namespace=cluster_namespace)


    # TODO:  Fix this
    def train_kube_stop(self,
                           model_name,
                           model_tag,
                           model_type,
                           model_runtime=None,
                           model_chip=None,
                           cluster_namespace=None,
                           image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_stop(service_name=service_name,
                           cluster_namespace=cluster_namespace)


    # TODO:  Fix this
    def train_kube_logs(self,
                           model_name,
                           model_tag,
                           model_type,
                           model_runtime=None,
                           model_chip=None,
                           cluster_namespace=None,
                           image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_logs(service_name=service_name,
                           cluster_namespace=cluster_namespace)


    # TODO:  Fix this
    def train_kube_scale(self,
                            model_name,
                            model_tag,
                            model_type,
                            replicas,
                            model_runtime=None,
                            model_chip=None,
                            cluster_namespace=None,
                            image_registry_namespace=None):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_train_namespace

        service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

        self._service_scale(service_name=service_name,
                            replicas=replicas,
                            cluster_namespace=cluster_namespace)


    def predict_sage_start(self,
                           model_name,
                           model_tag,
                           model_type,
                           aws_iam_arn,
                           aws_instance_type,
                           model_runtime=None,
                           model_chip=None,
                           input_stream_url=None,
                           input_stream_topic=None,
                           output_stream_url=None,
                           output_stream_topic=None,
                           memory_limit='2Gi',
                           core_limit='1000m',
                           target_core_util_percentage='75',
                           min_replicas='1',
                           max_replicas='1',
                           cluster_namespace=None,
                           image_registry_url=None,
                           image_registry_repo=None,
                           image_registry_namespace=None,
                           image_registry_base_tag=None,
                           image_registry_base_chip=None,
                           pipeline_templates_path=None,
                           timeout=1200):

        model_tag = self._validate_and_prep_model_tag(model_tag)

        if not model_runtime:
            model_runtime = self._get_default_model_runtime(model_type)

        if not model_chip:
            model_chip = PipelineCli._default_model_chip

        if not cluster_namespace:
            cluster_namespace = PipelineCli._default_cluster_namespace

        if not image_registry_url:
            image_registry_url = PipelineCli._default_image_registry_url

        if not image_registry_repo:
            image_registry_repo = PipelineCli._default_image_registry_repo

        if not image_registry_namespace:
            image_registry_namespace = PipelineCli._default_image_registry_predict_namespace

        if not image_registry_base_tag:
            image_registry_base_tag = PipelineCli._default_image_registry_base_tag

        if not image_registry_base_chip:
            image_registry_base_chip = PipelineCli._default_model_chip

        if not pipeline_templates_path:
            pipeline_templates_path = PipelineCli._default_pipeline_templates_path

        # Create Model
        from datetime import datetime

        begin_time = datetime.now()

        sagemaker_admin_client = boto3.client('sagemaker')
        response = sagemaker_admin_client.create_model(
            ModelName='%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
            PrimaryContainer={
                'ContainerHostname': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
                'Image': '%s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag),
                'Environment': {
                }
            },
            SupplementalContainers=[],
            ExecutionRoleArn='%s' % aws_iam_arn,
            Tags=[
                {
                    'Key': 'PIPELINE_MODEL_NAME',
                    'Value': '%s' % model_name
                },
                {
                    'Key': 'PIPELINE_MODEL_TAG',
                    'Value': '%s' % model_tag
                },
                {
                    'Key': 'PIPELINE_MODEL_TYPE',
                    'Value': '%s' % model_type
                },
                {
                    'Key': 'PIPELINE_MODEL_RUNTIME',
                    'Value': '%s' % model_runtime
                },
                {
                    'Key': 'PIPELINE_MODEL_CHIP',
                    'Value': '%s' % model_chip
                },
            ]
        )

        if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("")
            print("ModelArn: '%s'" % response['ModelArn'])
            print("")
            print("Success!")
            print("")
        else:
            exit(1)

        # Create Endpoint Configuration
        response = sagemaker_admin_client.create_endpoint_config(
            EndpointConfigName='%s-%s' % (image_registry_namespace, model_name),
            ProductionVariants=[
                {
                    'VariantName': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
                    'ModelName': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
                    'InitialInstanceCount': 1,
                    'InstanceType': '%s' % aws_instance_type,
                     # 'ml.c4.2xlarge'|'ml.c4.8xlarge'|'ml.c4.xlarge'|'ml.c5.2xlarge'|'ml.c5.9xlarge'|'ml.c5.xlarge'|'ml.m4.xlarge'|'ml.p2.xlarge'|'ml.p3.2xlarge'|'ml.t2.medium',
                    'InitialVariantWeight': 100
                },
            ],
            Tags=[
                {
                    'Key': 'PIPELINE_MODEL_NAME',
                    'Value': '%s' % model_name
                },
                {
                    'Key': 'PIPELINE_MODEL_TAG',
                    'Value': '%s' % model_tag
                },
                {
                    'Key': 'PIPELINE_MODEL_TYPE',
                    'Value': '%s' % model_type
                },
                {
                    'Key': 'PIPELINE_MODEL_RUNTIME',
                    'Value': '%s' % model_runtime
                },
                {
                    'Key': 'PIPELINE_MODEL_CHIP',
                    'Value': '%s' % model_chip
                },
            ]
        )

        if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("")
            print("EndpointConfigArn: '%s'" % response['EndpointConfigArn'])
            print("")
            print("Success!")
            print("")
        else:
            exit(1)

        # Create Endpoint (Models + Endpoint Configuration)
        response = sagemaker_admin_client.create_endpoint(
            EndpointName='%s-%s' % (image_registry_namespace, model_name),
            EndpointConfigName='%s-%s' % (image_registry_namespace, model_name),
            Tags=[
                {
                    'Key': 'PIPELINE_MODEL_NAME',
                    'Value': '%s' % model_name
                },
                {
                    'Key': 'PIPELINE_MODEL_TAG',
                    'Value': '%s' % model_tag
                },
                {
                    'Key': 'PIPELINE_MODEL_TYPE',
                    'Value': '%s' % model_type
                },
                {
                    'Key': 'PIPELINE_MODEL_RUNTIME',
                    'Value': '%s' % model_runtime
                },
                {
                    'Key': 'PIPELINE_MODEL_CHIP',
                    'Value': '%s' % model_chip
                },
            ]
        )

        if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("")
            print("EndpointArn: '%s'" % response['EndpointArn'])
            print("")
            print("Success!")
            print("")
        else:
            exit(1)

        end_time = datetime.now()
        total_time = end_time - begin_time
        print("")
        print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
        print("")


    # TODO:  Fix this
    def _image_to_json(self,
                      image_path,
                      image_format):

        image_path = os.path.expandvars(image_path)
        image_path = os.path.expanduser(image_path)
        image_path = os.path.abspath(image_path)
        image_path = os.path.normpath(image_path)

        print('image_path: %s' % image_path)
        print('image_format: %s' % image_format)

        #image = Image.open(image_path)
        #image_str = BytesIO()
        #image.save(image_str, format=image_format)
        #return json.dumps(str(image_str.getvalue()))
    #    import numpy as np
    #    img = Image.open("input.png")
    #    arr = np.array(img)
    #    return arr


    def _image_to_numpy(self,
                       image_path):
        """Convert image to np array.
        Returns:
            Numpy array of size (1, 28, 28, 1) with MNIST sample images.
        """
        image_as_numpy = np.zeros((1, 28, 28))
        print(image_as_numpy.shape)
        for idx, image_path in enumerate(image_path):
            image_read = skimage.io.imread(fname=image_path, as_grey=True)
            print(image_read.shape)
            image_as_numpy[idx, :, :] = image_read

        return json.dumps(list(image_as_numpy.flatten()))


def main():
    fire.Fire(PipelineCli)


if __name__ == '__main__':
    main()
