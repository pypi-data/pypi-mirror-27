import json
import os
import subprocess

def cancel(name):
    subprocess.call(['mp-compiler', '-f', '.metaparticle/spec.json', '--delete'])

def logs(name):
    subprocess.call(['mp-compiler', '-f', '.metaparticle/spec.json', '--deploy=false', '--attach=true'])

def makeShardedService(img, name, options):
    return {}

def makeReplicatedService(img, name, options):
    return {}

def ports(portArray):
    result = []
    for port in portArray:
        result.append({
            'number': port,
            'protocol': 'TCP'
        })
    return result

def run(img, name, options):
    svc =  {
        "name": name,
        "guid": 1234567, 
        "services": [ 
            {
                "name": name,
                "replicas": options.get('replicas', None),
                "shardSpec": options.get('shardSpec', None),
                "containers": [
                    { "image": img }
                ],
                "ports": ports(options.get('ports', []))
            }
        ],
        "serve": {
            "name": name,
        }
    }
    if not os.path.exists('.metaparticle'):
        os.makedirs('.metaparticle')

    with open('.metaparticle/spec.json', 'w') as out:
        json.dump(svc, out)
    
    subprocess.call(['mp-compiler', '-f', '.metaparticle/spec.json'])
