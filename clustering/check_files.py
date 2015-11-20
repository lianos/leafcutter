import sys
import gzip

by_chrom = {}
libs, libChroms = {}, {}
for lib in sys.argv[2:]:
    sys.stderr.write("checking %s... "%lib)
    foutName = lib+'.sorted.gz'
    libs[lib] = 0
    libChroms[lib] = []
    counted = {}
    for ln in open(lib):
        chrom, start, end, dot, count, strand = ln.split()
        libs[lib] += 1
        if chrom in counted: continue
        counted[chrom] = ''

        if chrom not in by_chrom:
            by_chrom[chrom] = []
        by_chrom[chrom].append(lib)
        libChroms[lib].append(chrom)
    sys.stderr.write("%d junctions\n"%libs[lib])


failed_junc = []
for lib in libChroms:
    if len(libChroms[lib]) < max([len(x) for x in libChroms.values()])/1:
        failed_junc.append("rm "+lib)
    
if len(failed_junc) > 0:
    sys.stderr.write("Consider re-running without the following junc files:\n"+"\n".join(failed_junc))

try: fout = open(sys.argv[1])
except: pass
else:
    sys.stderr.write("%s exists..rm it to write\n"%sys.argv[1])
    exit()

fout = open(sys.argv[1],'w')

use_chroms = []
for chrom in by_chrom:    
    if len(by_chrom[chrom]) != len(libs):
        continue
    fout.write(chrom+'\n')
    use_chroms.append(chrom)

sys.stderr.write("Using %s\n"%(" ".join(use_chroms)))