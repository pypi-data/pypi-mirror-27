import subprocess


def build(img):
    subprocess.call(['docker', 'build', '-t', img, '.'])


def publish(img):
    subprocess.call(['docker', 'push', img])
