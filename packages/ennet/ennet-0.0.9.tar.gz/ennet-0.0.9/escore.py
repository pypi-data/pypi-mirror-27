from argparse import ArgumentParser 
import sys

def esArgs():
    parser = ArgumentParser(usage='python escore.py -sm [path/to/somatic mutations file] -ep [path/to/enhancer-promoter interactions file] -out [path/to/outprefix]', description='function: generates E score matrix.')
    parser.add_argument('-sm', required=True, help='Path to tab-separated somatic mutations file containing chr, start and end fields.')
    parser.add_argument('-ep', required=True, help='Path to tab-separated enhancer-promoter interactions file containing chr, start, end and gene name fields.')
    parser.add_argument('-o', required=True, help='outprefix, out file path + outprefix')
    return parser.parse_args()

def snpcount(enhancer,snp):
    snp_pos=[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
    snp_counts_dict={}
    enhancer_snp_count_dict={}
    chr_dict={1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,14:14,15:15,16:16,17:17,18:18,19:19,20:20,21:21,22:22}
    snp_file=open(snp,'r')
    line=snp_file.readline()
    while line:
        li=line.split('\t')
        li[0]=li[0].lstrip('chr')
        if li[0]=='X':
            if li[1] in snp_pos[-2]:
                snp_pos[-2][li[1]]+=1
            else:
                snp_pos[-2][li[1]]=1
        elif li[0]=='Y':
            if li[1] in snp_pos[-1]:
                snp_pos[-1][li[1]]+=1
            else:
                snp_pos[-1][li[1]]=1
        elif li[0]=='M':
            if li[1] in snp_pos[-3]:
                snp_pos[-3][li[1]]+=1
            else:
                snp_pos[-3][li[1]]=1
        elif int(li[0]) in chr_dict:
            snp_chr=int(li[0])
            if li[1] in snp_pos[snp_chr]:
                snp_pos[snp_chr][li[1]]+=1
            else:
                snp_pos[snp_chr][li[1]]=1
        else:
	    pass
        line=snp_file.readline()
    enhancer_file=open(enhancer,'r')
    line=enhancer_file.readline()
    while line:
        line=line.rstrip('\n')
        li=line.split('\t')
        enh_chr=li[0].lstrip('chr')
        if enh_chr=='X':
            enh_chr_num=-2
        elif enh_chr=='Y':
            enh_chr_num=-1
        elif enh_chr=='M':
            enh_chr_num=-3
        else:
            enh_chr_num=int(enh_chr)
        enh_stt=int(li[1])
        enh_end=int(li[2])
        i=enh_stt
        count=0
        while i <= enh_end:
            if not (str(i) in snp_pos[enh_chr_num]):
                i+=1
            else:
                count+=snp_pos[enh_chr_num][str(i)]
                i+=1
        enhancer_snp_count_dict[line]=str(count)
        if li[3] in snp_counts_dict:
            snp_counts_dict[li[3]] += count
        else:
            snp_counts_dict[li[3]] = count
        line=enhancer_file.readline()
    return snp_counts_dict,enhancer_snp_count_dict      #gene,enhancer snp counts

def runEscore(args):
    geneCount=open(args.o+"_gene_snp_count.txt",'w')
    enhancerCount=open(args.o+"_enhancer_snp_count.txt",'w')
    gene_snp_count,enhancer_snp_count=snpcount(args.ep,args.sm)
    for key in gene_snp_count:
        geneCount.write(key+'\t'+str(gene_snp_count[key])+'\n')
    for key in enhancer_snp_count:
        enhancerCount.write(key+'\t'+str(enhancer_snp_count[key])+'\n')

if __name__ == '__main__':
    runEscore(esArgs())
