from setuptools import setup, find_packages

with open('VERSION') as f:
    version = f.read().strip()

setup(
    name='anon-ai-toolbelt',
    url='https://github.com/anon-ai/toolbelt',
    author='Anon AI',
    author_email='info@anon.ai',
    version=version,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3',
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'anon = anon_ai_toolbelt.command:main',
        ],
    },
)
