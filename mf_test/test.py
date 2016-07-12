import freeling
import inspect
import os
import subprocess

FREELINGDIR = '/usr/local/'
DATA = FREELINGDIR + 'share/freeling/'
LANGUAGE = 'es'



freeling.util_init_locale('default')
option = freeling.maco_options(LANGUAGE)
option.set_data_files( "",
                      DATA + "common/punct.dat",
                      DATA + LANGUAGE + "/dicc.src",
                      DATA + LANGUAGE + "/afixos.dat",
                      "",
                      DATA + LANGUAGE + "/locucions.dat",
                      DATA + LANGUAGE + "/np.dat",
                      DATA + LANGUAGE + "/quantities.dat",
                      DATA + LANGUAGE + "/probabilitats.dat");

morfo = freeling.maco(option)
tokenizer = freeling.tokenizer(DATA + LANGUAGE + '/tokenizer.dat')
splitter = freeling.splitter(DATA + LANGUAGE + '/splitter.dat')
sid = splitter.open_session()
tagger = freeling.hmm_tagger(DATA + LANGUAGE + '/tagger.dat', True, 2)
senses = freeling.senses(DATA + LANGUAGE + '/senses.dat')
parser = freeling.chart_parser(DATA + LANGUAGE + '/chunker/grammar-chunk.dat')
depen = freeling.dep_txala(DATA + LANGUAGE + '/dep_txala/dependences.dat', parser.get_start_symbol())
morfo.set_active_options(False, True, True, True,  # select which among created
                   True, True, False, True,  # submodules are to be used.
                   True, True, True, True ); # default: all created submodules are used


phrase = 'El gato come pescado. Pero a Don Jaime no le gustan los gatos.'
tokens = tokenizer.tokenize(phrase)
splitted_phrase = splitter.split(sid, tokens, False)
mf_analysis = morfo.analyze(splitted_phrase)
mf_analysis = tagger.analyze(mf_analysis)
mf_analysis = parser.analyze(mf_analysis)
# definicion de comando y archivo .r
command = 'Rscript'
path2script = 'prueba.r'

# mf_analysis = depen.analyze(mf_analysis)
arrayPhrase=[]

for item in mf_analysis:
    words = item.get_words()
    for word in words:
        print "-------------------------------------------------"
        analysis = word.get_analysis()
        lemma = word.get_lemma()
        tag = word.get_tag()
        form = word.get_form()
        arrayPhrase.append(str(form))
        print  "form="+str(form)+" tag="+str(tag)+ " lemma=" + str(lemma)
        print "analysis: "
        for an in analysis:
            print "prob=" + str(an.get_prob()) + " tag=" + str(an.get_tag())
#cerrar archivo auxiliar entrada.txt


import subprocess

# Define command and arguments
command = 'php'
path2script = 'script.php'


# Build subprocess command
cmd = [command, path2script]+arrayPhrase

# check_output will run the command and store to result

x = subprocess.check_output(cmd, universal_newlines=True)
print x


# Define command and arguments
command = 'Rscript'
path2script = 'script.r'

# Build subprocess command
cmd = [command, path2script]+arrayPhrase

# check_output will run the command and store to result

x = subprocess.check_output(cmd, universal_newlines=True)

print x