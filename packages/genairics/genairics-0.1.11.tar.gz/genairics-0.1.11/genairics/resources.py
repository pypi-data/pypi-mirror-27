#!/usr/bin/env python
"""
Tasks here prepare resources that are required for some
pipeline tasks, and are generally available from the
resources directory as specified by $GAX_RESOURCES
"""
from datetime import datetime, timedelta
import luigi, os, tempfile, pathlib, glob
from luigi.util import inherits
from plumbum import local, colors
import logging

from genairics import gscripts

resourcedir = os.environ.get('GAX_RESOURCES',os.path.expanduser('~/resources'))
logresources = logging.Logger('genairics.resources')

def requestFiles(urlDir,fileregex,outdir):
    """
    Download a set of files that match fileregex from urlDir
    """
    import requests, re
    link = re.compile(r'href="(.+?)"')
    if fileregex: fileregex = re.compile(fileregex)
    if not urlDir.endswith('/'): urlDir+='/'
    # Download checksums if present
    checksums = requests.get(urlDir+'CHECKSUMS')
    if checksums:
        from io import StringIO
        import pandas as pd
        checksums = pd.read_table(StringIO(checksums.text),sep='\s+',
                                  names=['checksum', 'octets', 'name'],index_col='name')
    else: checksums = None
    # Retrieve index
    r = requests.get(urlDir)
    for l in link.finditer(r.text):
        l = l.groups()[0]
        if not fileregex or fileregex.match(l):
            file_request = requests.get(urlDir+l, stream=True)
            with open(os.path.join(outdir,l),'wb') as outfile:
                for chunk in file_request.iter_content(chunk_size=512):
                    outfile.write(chunk)
            if checksums is not None:
                csum = int(local['cksum']('-o',1,os.path.join(outdir,l)).split()[0])
                if csum != checksums.checksum[l]:
                    logresources.warning('%s checksum did not match url location %s',csum,urlDir)

# Tasks
class InstallDependencies(luigi.Task):
    """
    Installs the genairics dependency programs
    """
    def run(self):
        local[gscripts % 'genairics_dependencies.sh']
    
class RetrieveGenome(luigi.Task):
    """
    Prepares the genome
    """
    genome = luigi.Parameter(default='homo_sapiens',description="genome species name")
    release = luigi.IntParameter(default=91,description="ensembl release number of genome")

    def output(self):
        return luigi.LocalTarget(
            os.path.join(resourcedir,'ensembl',self.genome,'release-{}'.format(self.release))
        )

    def run(self):
        #Make temp dir for data
        local['mkdir']('-p',self.output().path+'_retrieving/dna')
        local['mkdir']('-p',self.output().path+'_retrieving/annotation')
        requestFiles(
            'http://ftp.ensembl.org/pub/release-{release}/fasta/{species}/dna/'.format(
                species=self.genome, release=self.release),
            r'.+.dna.chromosome.+.fa.gz',
            self.output().path+'_retrieving/dna'
        )
        requestFiles(
            'http://ftp.ensembl.org/pub/release-{release}/gtf/{species}/'.format(
                species=self.genome, release=self.release),
            r'.+.{release}.gtf.gz'.format(release=self.release),
            self.output().path+'_retrieving/annotation'
        )
        #Unzip all files
        local['gunzip'](*glob.glob(self.output().path+'_retrieving/*/*.gz'))
        #Rename temp dir to final/expected output dir
        os.rename(self.output().path+'_retrieving',self.output().path)

@inherits(RetrieveGenome)
class STARandRSEMindex(luigi.Task):
    """
    Index that can be used by both STAR aligner and RSEM counter for transcriptomics
    """
    threads = luigi.IntParameter(default=1, description='STAR threads to use to build mapping index')

    def requires(self):
        return self.clone_parent()
    
    def output(self):
        return (
            luigi.LocalTarget(
                os.path.join(resourcedir,'ensembl/{species}/release-{release}/transcriptome_index'.format(
                    species=self.genome,release=self.release))
            ),
            luigi.LocalTarget(
                os.path.join(resourcedir,'ensembl/{species}/release-{release}/transcriptome_index/build_completed'.format(
                    species=self.genome,release=self.release))
            )
        )
    
    def run(self):
        genomeDir = self.input().path
        os.mkdir(self.output()[0].path)
        stdout = local[gscripts % 'buildRSEMindex.sh'](
            *glob.glob(os.path.join(genomeDir,'annotation')+'/*.gtf'),
            self.threads,
            ','.join(glob.glob(os.path.join(genomeDir,'dna')+'/*.fa*')),
            os.path.join(self.output()[0].path, self.genome)
        )
        logresources.info(stdout)
        pathlib.Path(self.output()[1].path).touch()
