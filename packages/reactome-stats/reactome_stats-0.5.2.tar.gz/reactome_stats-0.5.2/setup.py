from setuptools import setup, find_packages

setup(name='reactome_stats',
      version='0.5.2',
      python_requires='==2.7.*',
      description='Reactome Metrics and Coverage',
      long_description='''
      ### Metrics and quality coverage at Reactome.

      This project aims to provide metrics on Reactome coverage with respect to other biomolecular data sources. For each of a growing number of analyses, we aim to provide:

      - The algorithm/workflow, to allow easy repeats/updates for new releases
      - Tabular data for spot checks and further analysis
      - High quality visualisations. All analysis focus on Reactome Human unless otherwise stated.''',
      url='https://github.com/corinabioinformatic/Neo4J_at_Reactome/tree/ReactomeStats',
      author='CorinaBioinformatic',
      author_email='corina.bioinformatic@gmail.com',
      license='GNU GPLv3',
      packages=['reactome_stats', 'tests'],
      py_modules=['uniprot', 'kegg', 'goc', 'analysis', 'reactomegraphdb'],
      install_requires=['pandas', 'neo4j_driver', 'matplotlib_venn'],
      keywords = 'reactome pathways metrics kegg uniprot GOC',
      zip_safe=False)