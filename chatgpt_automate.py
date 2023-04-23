import itertools
import os
import subprocess
import os
# Define the possible values for each property
wmodels = ['BM25', 'DFR', 'DLH', 'DFRee','DPH']
trecquerytags_processes = ['TOP','NUM','TITLE']
trecquerytags_skips = ['DESC','NARR']
termpipelines = ['Stopwords', 'PorterStemmer', 'Stopwords,PorterStemmer']
fieldtags_processes = ['TITLE', 'ELSE']
tokenizers = ['EnglishTokeniser', 'GalicianTokeniser']

# Read the Terrier properties file
with open('terrier.properties') as f:
    lines = f.readlines()

# Generate all possible combinations of the properties
combinations = list(itertools.product(wmodels, trecquerytags_processes, trecquerytags_skips, termpipelines, fieldtags_processes, tokenizers))

# Generate a new properties file, execute indexing and retrieval for each combination
for i, combination in enumerate(combinations):
    new_lines = []
    for line in lines:
        if line.startswith('querying.default.controls='):
            to_replace = line.split(',')
            result = [y for y in to_replace if 'wmodel' in y]
            if len(result)>0 :
                result_splitted = result[0].split('=')
                result_resplitted =result_splitted[1].split(':')
                result_resplitted[1] = combination[0]
                w_model  =':'.join(result_resplitted)
                result_splitted[1] = w_model
                quering_default = '='.join(result_splitted)
                to_replace[0]=quering_default
                new_lines.append(','.join(to_replace))





        elif line.startswith('TrecQueryTags.process='):
            new_lines.append('TrecQueryTags.process={}\n'.format(combination[1]))
        elif line.startswith('TrecQueryTags.skip='):
            new_lines.append('TrecQueryTags.skip={}\n'.format(combination[2]))
        elif line.startswith('termpipelines='):
            new_lines.append('termpipelines={}\n'.format(combination[3]))
        elif line.startswith('FieldTags.process='):
            new_lines.append('FieldTags.process={}\n'.format(combination[4]))
        elif line.startswith('querying.tokeniser='):
            pass
       #     new_lines.append('querying.tokeniser={}\n'.format(combination[5]))
        elif line.startswith('indexer.meta.forward.keys='):
            pass
         #   new_lines.append('indexer.meta.forward.keys=docno\n')
        elif line.startswith('indexer.meta.forward.keylens='):
            pass
        #    new_lines.append('indexer.meta.forward.keylens=12\n')
        elif line.startswith('indexer.meta.forward.keylens.names='):
            pass
        #    new_lines.append('indexer.meta.forward.keylens.names=docno\n')
        elif line.startswith('indexer.meta.reverse.keylens='):
            pass
        #    new_lines.append('indexer.meta.reverse.keylens=12\n')
        elif line.startswith('indexer.meta.reverse.keylens.names='):
            pass
         #   new_lines.append('indexer.meta.reverse.keylens.names=docno\n')
        else:
            new_lines.append(line)
    index_folder = f'./index_{i}'
    new_lines.append(f'terrier.index.path={index_folder }/')
    with open('terrier_{}.properties'.format(i), 'w') as f:
        f.writelines(new_lines)

    if not os.path.exists(f"{index_folder }"):
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(f"{index_folder}")
    #subprocess.run(['terrier', 'indexing', '-Dterrier.index.path=index_{}'.format(i), '-p', 'terrier_{}.properties'.format(i)])
    #subprocess.run(['terrier', 'batchretrieve', '-Dterrier.index.path=index_{}'.format(i), '-Dtrec.results.file=results_{}.txt'.format(i), '-p', 'terrier_{}.properties'.format(i)])
    #subprocess.run(['trec_eval', '-q', '-c', '-M1000', '-m', 'map', 'qrels.txt', 'results_{}.txt'.format(i)], stdout=open('eval_{}.txt'.format(i), 'w'))

# Collect the evaluation results for each combination and print them to the console
# for i, combination in enumerate(combinations):
#     with open('eval_{}.txt'.format(i)) as f:
#         lines = f.readlines()
#     for line in lines:
#         if line.startswith('map'):
#             map_score = line.split()[2]
#             print('Combination {}: wmodel={}, TrecQueryTags.process={}, TrecQueryTags.skip={}, termpipelines={}, FieldTags.process={}, MAP={}'.format(i, combination[0], combination[1], combination[2], combination[3], combination[4], map_score))
