from kubernetes import client, config
from kubernetes.stream import stream
import json

from kubernetes.watch import Watch


class KubeApi:
    def __init__(self, ):
        # config.load_kube_config("/Users/yuanshengrong/.kube/config")
        config.load_kube_config("ysr-kubeconfig")

    @staticmethod
    def pod_exec(namespace, pod, container, rows, cols):
        """

        :param namespace:
        :param pod:
        :param container:
        :param rows:
        :param cols:
        :return:
        """
        try:
            api_instance = client.CoreV1Api()
            exec_command = [
                "/bin/sh",
                "-c",
                'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
                '&& ([ -x /usr/bin/script ] '
                '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
                '|| exec /bin/sh'
                '&& cp -rp /etc/skel/.bash* /root/'
            ]
            cont_stream = stream(api_instance.connect_get_namespaced_pod_exec,
                                 name=pod,
                                 namespace=namespace,
                                 container=container,
                                 command=exec_command,
                                 stderr=True, stdin=True,
                                 stdout=True, tty=True,
                                 _preload_content=False
                                 )
            cont_stream.write_channel(4, json.dumps({"Height": int(rows), "Width": int(cols)}))
            return cont_stream
        except Exception as e:
            print(str(e))
            print("您没有访问该资源的权限，请联系管理员")

    @staticmethod
    def pod_log(namespace, pod, container, tails):
        """

        :param namespace:
        :param pod:
        :param container:
        :param tails:
        :return:
        """
        api_instance = client.CoreV1Api()
        w = Watch()
        cont_stream = w.stream(api_instance.read_namespaced_pod_log,
                               name=pod,
                               namespace=namespace,
                               container=container,
                               pretty=True,
                               follow=True,
                               tail_lines=tails,
                               previous=False,
                               insecure_skip_tls_verify_backend=True,
                               _preload_content=False)

        return cont_stream
