from setuptools import setup

setup(name='reactome_stats',
      version='0.3.1',
      description='Reactome Metrics and Coverage',
      url='https://github.com/corinabioinformatic/Neo4J_at_Reactome/tree/ReactomeStats',
      author='CorinaBioinformatic',
      author_email='corinabioinformatic@gmail.com',
      license='GNU GPLv3',
      packages=['reactome_stats','reactome_stats.uniprot','reactome_stats.reactomegraphdb','reactome_stats.kegg','reactome_stats.goc','reactome_stats.analysis'],
      zip_safe=False)