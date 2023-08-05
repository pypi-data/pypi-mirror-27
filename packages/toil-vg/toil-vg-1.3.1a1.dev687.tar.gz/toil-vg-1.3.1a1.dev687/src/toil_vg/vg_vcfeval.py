#!/usr/bin/env python2.7
"""
Thin wrapper for vcfeval, as a convenience to stick a vcfeval output directory
along with the other toil-vg output.  Can be run standalone as well.
"""
from __future__ import print_function
import argparse, sys, os, os.path, random, subprocess, shutil, itertools, glob
import json, time, timeit, errno
from uuid import uuid4
import logging

from toil.common import Toil
from toil.job import Job
from toil_vg.vg_common import *
from toil_vg.context import Context, run_write_info_to_outstore

logger = logging.getLogger(__name__)

def vcfeval_subparser(parser):
    """
    Create a subparser for vcf evaluation.  Should pass in results of subparsers.add_parser()
    """

    # Add the Toil options so the job store is the first argument
    Job.Runner.addToilOptions(parser)

    # General options
    parser.add_argument("call_vcf", type=make_url,
                        help="input vcf (must be bgzipped and have .tbi")
    parser.add_argument("vcfeval_baseline", type=make_url,
                        help="truth vcf (must be bgzipped and have .tbi")
    parser.add_argument("vcfeval_fasta", type=make_url,
                        help="fasta file containing the DNA sequence.  Can be"
                        " gzipped with .gz extension")
    parser.add_argument("out_store",
                            help="output store.  All output written here. Path specified using same syntax as toil jobStore")

    # Add common options shared with everybody
    add_common_vg_parse_args(parser)

    # Add common calling options shared with toil_vg pipeline
    vcfeval_parse_args(parser)

    # Add common docker options shared with toil_vg pipeline
    add_container_tool_parse_args(parser)

def vcfeval_parse_args(parser):
    """ centralize calling parameters here """

    parser.add_argument("--vcfeval_bed_regions", type=make_url,
                        help="BED file of regions to consider")
    parser.add_argument("--vcfeval_opts", type=str,
                        help="Additional options for vcfeval (wrapped in \"\")",
                        default=None)
    parser.add_argument("--vcfeval_cores", type=int,
                        default=1,
                        help="Cores to use for vcfeval")

def validate_vcfeval_options(options):
    """ check some options """
    # we can relax this down the road by optionally doing some compression/indexing
    assert options.vcfeval_baseline.endswith(".vcf.gz")
    assert options.call_vcf.endswith(".vcf.gz")

    
def vcfeval(job, context, work_dir, call_vcf_name, vcfeval_baseline_name,
            sdf_name, outdir_name, bed_name):

    """ create and run the vcfeval command """

    cmd = ['rtg', 'vcfeval', '--calls', call_vcf_name,
           '--baseline', vcfeval_baseline_name,
           '--template', sdf_name, '--output', outdir_name,
           '--threads', str(context.config.vcfeval_cores),
           '--vcf-score-field', 'QUAL']

    if bed_name is not None:
        cmd += ['--evaluation-regions', bed_name]

    if context.config.vcfeval_opts:
        cmd += context.config.vcfeval_opts

    context.runner.call(job, cmd, work_dir=work_dir)

    # get the F1 out of summary.txt
    # expect header on 1st line and data on 3rd and below
    # we take the best F1 found over these lines (which should correspond to best
    # point on quality ROC curve)
    # todo: be more robust
    f1 = None
    with open(os.path.join(work_dir, os.path.basename(outdir_name), "summary.txt")) as sum_file:
        header = sum_file.readline().split()
        assert header[-1] == 'F-measure'        
        line = sum_file.readline()
        for line in sum_file:
            data = line.strip().split()
            assert len(data) == len(header)
            line_f1 = float(data[-1])
            if f1 is None or line_f1 > f1:
                f1 = line_f1
    return f1
    
def run_vcfeval(job, context, sample, vcf_tbi_id_pair, vcfeval_baseline_id, vcfeval_baseline_tbi_id, 
                fasta_path, fasta_id, bed_id):                
    """ run vcf_eval, return f1 score """

    # make a local work directory
    work_dir = job.fileStore.getLocalTempDir()

    # download the vcf
    call_vcf_id, call_tbi_id = vcf_tbi_id_pair[0], vcf_tbi_id_pair[1]
    call_vcf_name = "calls.vcf.gz"
    job.fileStore.readGlobalFile(vcf_tbi_id_pair[0], os.path.join(work_dir, call_vcf_name))
    job.fileStore.readGlobalFile(vcf_tbi_id_pair[1], os.path.join(work_dir, call_vcf_name + '.tbi'))

    # and the truth vcf
    vcfeval_baseline_name = 'truth.vcf.gz'
    job.fileStore.readGlobalFile(vcfeval_baseline_id, os.path.join(work_dir, vcfeval_baseline_name))
    job.fileStore.readGlobalFile(vcfeval_baseline_tbi_id, os.path.join(work_dir, vcfeval_baseline_name + '.tbi'))    
    
    # download the fasta (make sure to keep input extension)
    fasta_name = "fa_" + os.path.basename(fasta_path)
    job.fileStore.readGlobalFile(fasta_id, os.path.join(work_dir, fasta_name))

    # download the bed regions
    bed_name = "bed_regions.bed" if bed_id else None
    if bed_id:
        job.fileStore.readGlobalFile(bed_id, os.path.join(work_dir, bed_name))

    # sample name is optional
    if sample:
        out_tag = '{}_vcfeval_output'.format(sample)
    else:
        out_tag = 'vcfeval_output'
        
    # output directory
    out_name = out_tag
    # indexed sequence
    sdf_name = fasta_name + ".sdf"
    
    # make an indexed sequence (todo: allow user to pass one in)
    context.runner.call(job, ['rtg', 'format',  fasta_name, '-o', sdf_name], work_dir=work_dir)    

    # run the vcf_eval command
    f1 = vcfeval(job, context, work_dir, call_vcf_name, vcfeval_baseline_name,
                 sdf_name, out_name, bed_name)

    # copy results to the output store
    # 1) vcfeval_output_f1.txt (used currently by tests script)
    f1_path = os.path.join(work_dir, "f1.txt")    
    with open(f1_path, "w") as f:
        f.write(str(f1))
    context.write_output_file(job, f1_path, out_store_path = '{}_f1.txt'.format(out_tag))
        
    # 2) vcfeval_output_summary.txt
    context.write_output_file(job, os.path.join(work_dir, out_tag, 'summary.txt'),
                              out_store_path = '{}_summary.txt'.format(out_tag))

    # 3) vcfeval_output.tar.gz -- whole shebang
    context.runner.call(job, ['tar', 'czf', out_tag + '.tar.gz', out_tag], work_dir = work_dir)
    context.write_output_file(job, os.path.join(work_dir, out_tag + '.tar.gz'))

    # 4) truth VCF
    context.write_output_file(job, os.path.join(work_dir, vcfeval_baseline_name))

    return f1

def vcfeval_main(context, options):
    """ command line access to toil vcf eval logic"""

    # check some options
    validate_vcfeval_options(options)
    
    # How long did it take to run the entire pipeline, in seconds?
    run_time_pipeline = None
        
    # Mark when we start the pipeline
    start_time_pipeline = timeit.default_timer()

    with context.get_toil(options.jobStore) as toil:
        if not toil.options.restart:
            start_time = timeit.default_timer()
            
            # Upload local files to the remote IO Store
            vcfeval_baseline_id = toil.importFile(options.vcfeval_baseline)
            call_vcf_id = toil.importFile(options.call_vcf)
            vcfeval_baseline_tbi_id = toil.importFile(options.vcfeval_baseline + '.tbi')
            call_tbi_id = toil.importFile(options.call_vcf + '.tbi')            
            fasta_id = toil.importFile(options.vcfeval_fasta)
            bed_id = toil.importFile(options.vcfeval_bed_regions) if options.vcfeval_bed_regions is not None else None

            end_time = timeit.default_timer()
            logger.info('Imported input files into Toil in {} seconds'.format(end_time - start_time))

            # Make a root job
            root_job = Job.wrapJobFn(run_vcfeval, context, None,
                                     (call_vcf_id, call_tbi_id),
                                     vcfeval_baseline_id, vcfeval_baseline_tbi_id,
                                     options.vcfeval_fasta, fasta_id, bed_id,
                                     cores=context.config.vcfeval_cores, memory=context.config.vcfeval_mem,
                                     disk=context.config.vcfeval_disk)

            # Init the outstore
            init_job = Job.wrapJobFn(run_write_info_to_outstore, context)
            init_job.addFollowOn(root_job)            

            # Run the job
            f1 = toil.start(init_job)
        else:
            f1 = toil.restart()

        print("F1 Score : {}".format(f1))
                
    end_time_pipeline = timeit.default_timer()
    run_time_pipeline = end_time_pipeline - start_time_pipeline
 
    print("All jobs completed successfully. Pipeline took {} seconds.".format(run_time_pipeline))
    
    
