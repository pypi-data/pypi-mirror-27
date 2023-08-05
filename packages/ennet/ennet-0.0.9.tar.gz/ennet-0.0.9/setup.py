from distutils.core import setup
setup(name='ennet',
    version='0.0.9',
    description='Whole genome sequencing technology has facilitated the discovery of a large number of Somatic Mutations in Enhancers (SMEs), whereas the utility of SMEs in tumorigenesis has not been fully explored. Here we present Ennet, a method to comprehensively investigate SMEs enriched networks (SME-networks) in cancer by integrating SMEs, enhancer-gene interactions and gene-gene interactions.',
    author='Ya Cui',
    author_email='cui_ya@163.com',
    url='http://bigdata.ibp.ac.cn/ennet/',
    install_requires = ['networkx>=1.11'],
    py_modules=['runEnnet','escore','draw','enNet','load','__init__'],
)
