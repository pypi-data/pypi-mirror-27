from setuptools import setup

setup(name='reactome_stats',
      version='0.5',
      description='Reactome Metrics and Coverage',
      url='https://github.com/corinabioinformatic/Neo4J_at_Reactome/tree/ReactomeStats',
      author='CorinaBioinformatic',
      author_email='corina.bioinformatic@gmail.com',
      license='GNU GPLv3',
      packages=['reactome_stats'],
      py_modules=['uniprot', 'kegg', 'goc', 'analysis', 'reactomegraphdb'],
      install_requires=['pandas', 'neo4j_driver', 'matplotlib_venn'],
      zip_safe=False)