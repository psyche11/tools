#!/usr/bin/python
#$ -S /usr/bin/python
#$ -cwd
#$ -r yes
#$ -j y
#$ -l h_rt=24:00:00
#$ -t 1-50
#$ -l arch=linux-x64
#$ -l mem_free=2G

import socket
import sys
import os
import subprocess

print "Python:", sys.version
print "Host:", socket.gethostname()

#sge_task_id = 1
#if os.environ.has_key("SGE_TASK_ID"):
#	sge_task_id = os.environ["SGE_TASK_ID"]
#
#id = int(sge_task_id)-1
#
#f = open('benchmark2.txt')
#systems = []
#for line in f:
#	name = line.split()[0]
#	extra = ''
#	if len(line.split()) > 1:
#		extra = line.split()[1]
#	systems.append( [name,extra] )
#f.close()
#
#name, extra = systems[id]
#pdb = name.split('_')[0]
#lig = name.split('_')[1]
#dir = name
#pdb_file = dir+'/'+pdb+"_with_"+lig+".pdb"
#params_file = dir+'/'+lig+"_from_"+pdb+".params"
#res_file = dir+'/'+pdb+'.resfile'
#extra_params = ''
#if extra != '':
#	extra_params = dir+'/'+extra+"_from_"+pdb+".params"

pdb_file = S9G10FPP.pdb
params_file = FPP_norot.params
res_file = S9G10_Y197A.res


coupled_moves_path = "/netapp/home/anum/Rosetta/main/source/bin/coupled_moves.linuxgccrelease"
database_path = "/netapp/home/anum/Rosetta/main/database"

coupled_moves_args = [
                      coupled_moves_path,
                      "-s %s" % pdb_file,
                      "-resfile %s" % res_file,
                      "-database %s" % database_path,
                      "-extra_res_fa %s" % params_file,
                      "-mute protocols.backrub.BackrubMover",
                      "-ex1",
                      "-ex2",
                      "-overwrite",
                      "-extrachi_cutoff 0",
                      "-nstruct 20",
                      "-coupled_moves::mc_kt 0.6",
                      "-coupled_moves::ntrials 1000",
                      "-coupled_moves::initial_repack false",
                      "-coupled_moves::ligand_mode true",
                      "-coupled_moves::ligand_weight 1.0",
                      #	"-coupled_moves::fix_backbone false",
                      #	"-coupled_moves::bias_sampling true",
                      #	"-coupled_moves::boltzmann_kt 0.6",
                      #	"-coupled_moves::bump_check true",
                      ]

if extra_params != '':
    coupled_moves_args.append("-extra_res_fa %s" % extra_params)

print coupled_moves_args

name = pdb_file

outfile = open(name+'.log', 'w')
process = subprocess.Popen(coupled_moves_args, stdout=outfile, stderr=subprocess.STDOUT, close_fds = True)
returncode = process.wait()
outfile.close()
